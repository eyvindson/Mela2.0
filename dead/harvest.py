#!/usr/bin/env python
# encoding: utf-8
"""
Title: harvest

Harvesting operations

*harvest.py*

Copyright (c) 2007 Simosol Oy. Distributed under the GNU General Public License 2.0.

NOTE:
    All Python operation models share the same set of input parameters. When
    implementing new operation model, remember to assign the following list
    of parameters as the function parameters:
        data - data by level
        variables - operation variable values
        parameters - operation parameter values
        par_table_val - values retrieved from a parameter table
        cash_flow_table - cash_flow structure
        cash_flow - container for returning cash flow (sum)
        results - container (numpy array) for returning operation results
        warnings - container for returning warnings
        errors - container for returning errors
"""

# Imports
from harvestdata import HarvestData
from harvestop import HarvestOperation
from constants import SIMULATIONLABEL, STANDLABEL, STRATUMLABEL, TREELABEL
from constants import DEADTREELABEL
from constants import EPSILON
from math import exp, floor, ceil
from operator import itemgetter
import random
import numpy

############################################################
##  Operation functions, callable from outside of module
############################################################

def bioenergy_thinning(data, variables, parameters, par_table_val,
                       cash_flow_table, cash_flow, results, restype,
                       warnings, errors, price_cache, stem_cache):
    """
    Bioenergy thinning. Implementation of the model is the same as in
    low_thinning, only operation name is different.
    """
    return thinning(data, variables, parameters, par_table_val,
                        cash_flow_table, cash_flow, results, restype,
                        warnings, errors, price_cache, stem_cache)

def clearcut(data, variables, parameters, par_table_val,
             cash_flow_table, cash_flow, results, restype,
             warnings, errors, price_cache, stem_cache):
    """
    Remove all trees except a number of reserve trees from a stand.
    """
    # check that operation data actually exists
    for level, ldata in data.iteritems():
        if ldata is None:
            errors.append("The level %s doesn't have data!")
            return -1
    hd = HarvestData('clearcut', data, variables, parameters,
                     par_table_val, cash_flow_table, price_cache)
    hd.set_stump_inclusion()
    hop = HarvestOperation(hd, stem_cache)
    # Iterate through all trees in the data from smallest to biggest
    for dcind in hd.cdata['removal_order']:
        hop.buck(dcind)
        props = hop.reduce_prop_for_reserve_trees(dcind, 1.0, results)
        hop.cut_dclass_trees(dcind, props)
    totrem = hop.store_harvest_results(results, cash_flow, scale=None,
                                            removedvolume=None, restype=restype)
    return 1
    
def clearcut_nature_scene(data, variables, parameters, par_table_val,
                       cash_flow_table, cash_flow, results, restype,
                       warnings, errors, price_cache, stem_cache):
    """
    Remove all trees except a number of reserve trees from a stand.
    """
    return clearcut(data, variables, parameters,
                             par_table_val, cash_flow_table,
                             cash_flow, results, restype, warnings, errors,
                             price_cache, stem_cache)

def covertree_position(data, variables, parameters, par_table_val,
                       cash_flow_table, cash_flow, results, restype,
                       warnings, errors, price_cache, stem_cache):
    """
    Remove all trees except a number of covertrees from a stand.
    """
    return seedtree_position(data, variables, parameters,
                             par_table_val, cash_flow_table,
                             cash_flow, results, restype, warnings, errors,
                             price_cache, stem_cache)

def estimate_stand_value(data, variables, parameters, par_table_val,
                         cash_flow_table, cash_flow, results, restype, warnings,
                         errors, price_cache, stem_cache):
    """
    buck each tree of a stand and calculate the total value in given currency.
    """
    # check that operation data actually exists
    for level, ldata in data.iteritems():
        if ldata is None:
            errors.append("The level %s doesn't have data!")
            return -1
    hd = HarvestData('standvalue', data, variables, parameters,
                     par_table_val, cash_flow_table, price_cache)
    hd.cdata['min_stump_diam'] = 0.0
    hd.cdata['stump_excl_num'] = 0.0
    hd.cdata['biomass_incl_prop'] = 1.0
    hd.cdata['stump_incl_prop'] = 1.0
    hop = HarvestOperation(hd, stem_cache)
    for dcind in hd.cdata['removal_order']:
        hop.buck(dcind)
        hop.cut_dclass_trees(dcind, (1.0, 1.0), trackchanges=False)
    totrem = hop.store_stand_value_results(results)
    return 1

def estimate_tree_value(data, variables, parameters, par_table_val,
                         cash_flow_table, cash_flow, results, restype, warnings,
                         errors, price_cache, stem_cache):
    """
    buck each tree of a stand and calculate the total value in given currency.
    """
    # check that operation data actually exists
    for level, ldata in data.iteritems():
        if ldata is None:
            errors.append("The level %s doesn't have data!")
            return -1
    hd = HarvestData('standvalue', data, variables, parameters,
                     par_table_val, cash_flow_table, price_cache)
    hd.cdata['min_stump_diam'] = 0.0
    hd.cdata['stump_excl_num'] = 0.0
    hd.cdata['biomass_incl_prop'] = 1.0
    hd.cdata['stump_incl_prop'] = 1.0
    hop = HarvestOperation(hd, stem_cache)
    for dcind in hd.cdata['removal_order']:
        hop.buck(dcind)
        hop.cut_dclass_trees(dcind, (1.0, 1.0), trackchanges=False)
    totrem = hop.store_tree_value_results(results)
    return 1

def first_thinning(data, variables, parameters, par_table_val,
                   cash_flow_table, cash_flow, results, restype, warnings,
                   errors, price_cache, stem_cache):
    """
    First thinning. Implementation of the model is the same as in low_thinning,
    only operation name is different
    """
    return thinning(data, variables, parameters, par_table_val,
                    cash_flow_table, cash_flow, results, restype, warnings,
                    errors, price_cache, stem_cache)

def remove_seedtrees(data, variables, parameters, par_table_val,
                     cash_flow_table, cash_flow, results, restype, warnings,
                     errors, price_cache, stem_cache):
    """
    remove the seedtrees from a stand.
    """
    # check that operation data actually exists
    for level, ldata in data.iteritems():
        if ldata is None:
            errors.append("The level %s doesn't have data!")
            return -1
    hd = HarvestData('removeseedtree', data, variables, parameters,
                     par_table_val, cash_flow_table, price_cache,
                     keepemptystrata=True)
    hop = HarvestOperation(hd, stem_cache)
    ind = hd.ind
    strata = hd.stratumdata
    for dcind in hd.cdata['removal_order']:
        tree, istratum, sp = hop.get_dclass_info(dcind)
        if strata[istratum, ind['stratum_seedtree']] == 1.0:
            hop.buck(dcind)
            hop.cut_dclass_trees(dcind, (1.0, 1.0), biomass=False)
    removedvolumemerch = hop.store_harvest_results(results, cash_flow, scale=None,
                                            removedvolume=None, biomass=False, tagmods=False)
    # Abort the operation in case accumulated volume was too small
    # NB! removedvolumemerch is the total merchantable (log+pulpwood)
    # volume removed per hectare
    if removedvolumemerch < hd.cdata['min_vol_accumulation_remove_seedtrees']:
        return -2
    return 1

def seedtree_position(data, variables, parameters, par_table_val,
                      cash_flow_table, cash_flow, results, restype, warnings,
                      errors, price_cache, stem_cache):
    """
    Remove all trees except a number of seedtrees from a stand.
    """
    # check that operation data actually exists
    for level, ldata in data.iteritems():
        if ldata is None:
            errors.append("The level %s doesn't have data!")
            return -1

    hd = HarvestData('seedtree', data, variables, parameters,
                     par_table_val, cash_flow_table, price_cache)
    hd.set_stump_inclusion()
    hop = HarvestOperation(hd, stem_cache)

    # check that seedtreespecies stratum has enough number of big trees
    # and assign seedtree numbers by tree species
    dlim = 0.9 * hd.cdata['ddom']
    hop.number_of_potential_seedtrees(dlim)

    # iteration from smallest to biggest trees
    for dcind in hd.cdata['removal_order']:
        hop.buck(dcind)
        props = hop.reduce_prop_for_seed_and_reserve_trees(dcind, 1.0, dlim, results)
        hop.cut_dclass_trees(dcind, props)
    removedvolumemerch = hop.store_harvest_results(results, cash_flow, scale=None,
                                            removedvolume=None, restype=restype)
    # Abort the operation in case accumulated volume was too small
    # NB! removedvolumemerch is the total merchantable (log+pulpwood)
    # volume removed per hectare
    if removedvolumemerch < hd.cdata['min_vol_accumulation_seedtree_position']:
        return -2
    return 1
    
def seedtree_position_nature_scene(data, variables, parameters, par_table_val,
                         cash_flow_table, cash_flow, results, restype, warnings,
                         errors, price_cache, stem_cache):
    """
    Remove all trees except a number of sheltertrees from a stand.
    """
    return seedtree_position(data, variables, parameters,
                             par_table_val, cash_flow_table,
                             cash_flow, results, restype, warnings, errors,
                             price_cache, stem_cache)

def sheltertree_position(data, variables, parameters, par_table_val,
                         cash_flow_table, cash_flow, results, restype, warnings,
                         errors, price_cache, stem_cache):
    """
    Remove all trees except a number of sheltertrees from a stand.
    """
    return seedtree_position(data, variables, parameters,
                             par_table_val, cash_flow_table,
                             cash_flow, results, restype, warnings, errors,
                             price_cache, stem_cache)
                             
def sheltertree_position_nature_scene(data, variables, parameters, par_table_val,
                         cash_flow_table, cash_flow, results, restype, warnings,
                         errors, price_cache, stem_cache):
    """
    Remove all trees except a number of sheltertrees from a stand.
    """
    return seedtree_position(data, variables, parameters,
                             par_table_val, cash_flow_table,
                             cash_flow, results, restype, warnings, errors,
                             price_cache, stem_cache)

def strip_cutting(data, variables, parameters, par_table_val,
                  cash_flow_table, cash_flow, results, restype, warnings,
                  errors, price_cache, stem_cache):
    """
    Remove all trees from narrow strip shaped stand. The trees in adjasent
    stands will seed the new tree generation of the strip cutting area.
    """
    # Assign seedtree_density to 0, add the two other parameter table values
    par_table_val = [[[0]], par_table_val[0], par_table_val[1]]
    return seedtree_position(data, variables, parameters,
                             par_table_val, cash_flow_table,
                             cash_flow, results, restype, warnings, errors,
                             price_cache, stem_cache)

def thinning(data, variables, parameters, par_table_val,
             cash_flow_table, cash_flow, results, restype, warnings, errors,
             price_cache, stem_cache):
    """
    Executes a thinning in a stand. Remove a given portion of classes from
    stand's diameter distribution, starting from the smallest or biggest ones.
    The thinning type (low or upper thinning) is defined using parameters.
    """
    # check that operation data actually exists
    for level, ldata in data.iteritems():
        if ldata is None:
            errors.append("The level %s doesn't have data!")
            return -1

    hd = HarvestData('thinning', data, variables, parameters,
                     par_table_val, cash_flow_table, price_cache)
    hd.set_track_removal()
    # Thinning based on basal area
    targetvar='BA'
    hd.set_thinning_control_param(targetvar)
    hd.set_stump_inclusion()
    hd.set_d_cut_all_below()
    hop = HarvestOperation(hd, stem_cache)
    # Buck all tree stems and remove stems from tracks
    for dcind in hd.cdata['removal_order']:
        prop = hd.cdata['track_removal']
        hop.buck(dcind)
        hop.cut_dclass_trees(dcind, (prop, prop))
    # Update BA_to_remove when stems from tracks are removed
    hd.update_to_remove()
    # remove diameter classes from both ends of the distribution
    hop.cut_from_top_and_bottom()
    #hberg = open('C:/MyTemp/temp3.txt', 'a')
    #hberg.write(str(str(hop.hdata.cdata['remove_from_above_percentage'])+'\r'))
    #hberg.close()
    # Finally store the cumulative volumes, values etc. into result data
    removedvolumemerch = hop.store_harvest_results(results, cash_flow, scale=None,
                                            removedvolume=None, restype=restype)
    # Abort the operation in case accumulated volume was too small
    # NB! removedvolumemerch is the total merchantable (log+pulpwood)
    # volume removed per hectare
    if removedvolumemerch < hd.cdata['min_vol_accumulation']:
        return -2
    return 1

def first_thinning_stem_number(data, variables, parameters,
           par_table_val, cash_flow_table, cash_flow, results, restype,
           warnings, errors, price_cache, stem_cache):
    """
    Executes a stem number based first thinning in a stand. Remove a given
    portion of classes from stand's diameter distribution, starting from the
    smallest or biggest ones.
    The thinning type (low or upper thinning) is defined using parameters.
    """
    # check that operation data actually exists
    for level, ldata in data.iteritems():
        if ldata is None:
            errors.append("The level %s doesn't have data!")
            return -1

    hd = HarvestData('first_thinning_stem_number', data, variables, parameters,
                     par_table_val, cash_flow_table, price_cache)
    hd.set_track_removal()
    # Thinning based on stem number
    targetvar='N'
    hd.set_thinning_control_param(targetvar)
    hd.set_stump_inclusion()
    hd.set_d_cut_all_below()
    hop = HarvestOperation(hd, stem_cache)
    # Buck all tree stems and remove stems from tracks
    for dcind in hd.cdata['removal_order']:
        prop = hd.cdata['track_removal']
        hop.buck(dcind)
        hop.cut_dclass_trees(dcind, (prop, prop))
    # Update N_to_remove when stems from tracks are removed
    hd.update_to_remove()
    # remove diameter classes from both ends of the distribution
    hop.cut_from_top_and_bottom()
    # Finally store the cumulative volumes, values etc. into result data
    removedvolumemerch = hop.store_harvest_results(results, cash_flow, scale=None,
                                            removedvolume=None, restype=restype)
    # Abort the operation in case accumulated volume was too small
    # NB! removedvolumemerch is the total merchantable (log+pulpwood)
    # volume removed per hectare
    if removedvolumemerch < hd.cdata['min_vol_accumulation']:
        return -2
    return 1

def thinning_with_removed_volume(data, variables, parameters,
            par_table_val, cash_flow_table, cash_flow, results, restype,
            warnings, errors, price_cache, stem_cache):
    """
    Executes a thinning in a stand. Remove a given portion of classes from
    stand's diameter distribution, starting from the smallest or biggest ones.
    The thinning type (low or upper thinning) is defined using parameters.
    """
    #Check if V_harvested or remaining_BA are given
    if data[STANDLABEL][0][13]==0 or (data[STANDLABEL][0][13]>0 and data[STANDLABEL][0][14]>0):
        # Basic low thinning. If removed volume is 0 or both removed volume and remaining
        # basal area are greater then 0, basic low_thinning is used (Remaining_upper and
        # Remaining_lower in thinning model replaced with remaining_ba)
        return thinning(data, variables, parameters, par_table_val,
                            cash_flow_table, cash_flow, results, restype,
                            warnings, errors, price_cache,
                            stem_cache)
    else:
        # check that operation data actually exists
        for level, ldata in data.iteritems():
            if ldata is None:
                errors.append("The level %s doesn't have data!")
                return -1
        hd = HarvestData('thinning_with_removed_volume', data, variables,
                         parameters, par_table_val, cash_flow_table,
                         price_cache)
        hd.set_track_removal()
        # Thinning based on volume of timber (commercially usable wood)
        targetvar='V_com'
        hd.set_thinning_control_param(targetvar)
        hd.set_stump_inclusion()
        hd.set_d_cut_all_below()
        hop = HarvestOperation(hd, stem_cache)
        # Calculate current volume
        hop.V_current = hd.get_vol_from_treelist()
        # Buck all tree stems
        for dcind in hd.cdata['removal_order']:
            hop.buck(dcind)
        # Calculate scaling factor and removed volume for results
        svol = hop.hdata.result['stratum_vol']
        scale, removedvolume = hop._set_result_scaling(svol)
        # Remove stems from tracks
        for dcind in hd.cdata['removal_order']:
            prop = hd.cdata['track_removal']
            hop.cut_dclass_trees(dcind, (prop, prop), scale=scale)
        # Update V_to_remove when stems from tracks are removed
        # NB! With wide track_width and narrow track_distance, and small
        # accumulated timber volume  the whole removed volume might be already
        # removed here! Check the thinning model parameters in the operation
        # model chain.
        cut_timber = hop.cut_timber
        hd.update_to_remove(cut_timber)
        # remove diameter classes from both ends of the distribution
        hop.cut_from_top_and_bottom(scale)
        # Finally store the cumulative volumes, values etc. into result data
        hop.store_harvest_results(results, cash_flow, scale, removedvolume, restype=restype)
        return 1

def selection_cut(data, variables, parameters, par_table_val,
                  cash_flow_table, cash_flow, results, restype,warnings,
                  errors, price_cache, stem_cache):
    """
    Basic selection cutting model derived from basic harvest model.
    """
    # check that operation data actually exists
    for level, ldata in data.iteritems():
        if ldata is None:
            errors.append("The level %s doesn't have data!")
            return -1
    hd = HarvestData('selection_cut', data, variables, parameters,
                     par_table_val, cash_flow_table, price_cache, keepemptystrata=True)
    # Stem number of under storey not included
    hd.set_track_removal_without_under_storey()
    # Thinning based on basal area
    targetvar='BA'
    hd.set_selection_cut_control_param(targetvar)
    hd.set_stump_inclusion()
    hd.set_d_cut_all_above()
    hop = HarvestOperation(hd, stem_cache)
    # Buck all tree stems and remove stems from tracks
    for dcind in hd.cdata['removal_order']:
        prop = hd.cdata['track_removal']
        hop.buck(dcind)
        hop.cut_dclass_trees(dcind, (prop, prop))
    # Update BA_to_remove when stems from tracks are removed
    hd.update_to_remove()
    if hd.cdata['slope']==0:
        # remove diameter classes evenly
        hop.cut_evenly()
    else:
        # set proportion removed from top and bottom
        hd.set_remove_from_below_and_above_percentage()
        
        # remove diameter classes from both ends of the distribution
        hop.cut_from_top_and_bottom(harvesttype='selection_cut')
        #import pdb;pdb.set_trace()
    # Finally store the cumulative volumes, values etc. into result data
    removedvolumemerch = hop.store_harvest_results(results, cash_flow, scale=None,
                                            removedvolume=None, restype=restype)
    # Abort the operation in case accumulated volume was too small
    # NB! removedvolumemerch is the total merchantable (log+pulpwood)
    # volume removed per hectare
    if removedvolumemerch < hd.cdata['min_vol_accumulation']:
        return -2
    return 1

def selection_cut_with_little_open_areas(data, variables, parameters, par_table_val,
                  cash_flow_table, cash_flow, results, restype,warnings,
                  errors, price_cache, stem_cache):
    """
    Basic selection cutting model derived from basic harvest model.
    """
    # check that operation data actually exists
    for level, ldata in data.iteritems():
        if ldata is None:
            errors.append("The level %s doesn't have data!")
            return -1
    hd = HarvestData('selection_cut', data, variables, parameters,
                     par_table_val, cash_flow_table, price_cache, keepemptystrata=True)
    # Stem number of under storey not included
    hd.set_track_removal_without_under_storey()
    # Thinning based on basal area
    targetvar='BA'
    hd.set_selection_cut_control_param(targetvar)
    hd.set_stump_inclusion()
    hd.set_d_cut_all_above()
    hop = HarvestOperation(hd, stem_cache)
    # Buck all tree stems and remove stems from tracks
    for dcind in hd.cdata['removal_order']:
        prop = hd.cdata['track_removal']
        hop.buck(dcind)
        hop.cut_dclass_trees(dcind, (prop, prop))
    # Update BA_to_remove when stems from tracks are removed
    hd.update_to_remove()
    toremove = hd.cdata['to_remove']
    if toremove > EPSILON:
        if toremove - 2 > EPSILON:
            hd.cdata['target'] = hd.cdata['target'] + 2
            # remove diameter classes evenly up to target+2
            hop.cut_evenly()
            hd.cdata['target'] = hd.cdata['target'] - 2
            hd.update_to_remove()
        if hd.cdata['slope']==0:
            # remove diameter classes evenly
            hop.cut_evenly()
        else:
            # set proportion removed from top and bottom
            hd.set_remove_from_below_and_above_percentage()
            # remove diameter classes from both ends of the distribution
            hop.cut_from_top_and_bottom(harvesttype='selection_cut')
            
    # Finally store the cumulative volumes, values etc. into result data
    removedvolumemerch = hop.store_harvest_results(results, cash_flow, scale=None,
                                            removedvolume=None, restype=restype)
    # Abort the operation in case accumulated volume was too small
    # NB! removedvolumemerch is the total merchantable (log+pulpwood)
    # volume removed per hectare
    if removedvolumemerch < hd.cdata['min_vol_accumulation']:
        return -2
    return 1

def wood_assortments_plot(data, variables, parameters, par_table_val,
                         cash_flow_table, cash_flow, results, restype,
                         warnings, errors, price_cache, stem_cache):
    """
    buck each tree of a stand and calculate the total value in given currency.
    """
    # check that operation data actually exists
    for level, ldata in data.iteritems():
        if ldata is None:
            errors.append("The level %s doesn't have data!")
            return -1

    hd = HarvestData('wood_assortments', data, variables, parameters,
                     par_table_val, cash_flow_table, price_cache)
    hd.cdata['min_stump_diam'] = 0.0
    hd.cdata['stump_excl_num'] = 0.0
    hd.cdata['biomass_incl_prop'] = 0.0
    hd.cdata['stump_incl_prop'] = 0.0
    hop = HarvestOperation(hd, stem_cache)
    for dcind in hd.cdata['removal_order']:
        hop.buck(dcind)
        hop.cut_dclass_trees(dcind, (1.0, 1.0), volres=True, biomass=False,
                             trackchanges=False)
    totrem = hop.store_wood_assortment_results(results)
    return 1

def assortment_prices(data, variables, parameters, par_table_val,
                     cash_flow_table, cash_flow, results, restype,
                     warnings, errors, price_cache, stem_cache):
    """
    assortment prices.
    """
    # use 'estimate_stand_value' harvest data parameters here
    hd = HarvestData('assortment_prices', data, variables, parameters,
                     par_table_val, cash_flow_table, price_cache)

    cf = cash_flow_table[0]
    cf_array = cf.active_array.array  # cash_flow_table
    price_region = hd.cdata['price_region']  # price_region value
    species = (1, 2, 3, 9)  # species listing
    assortments = (1, 2)  # assortment listing
    pr_index = cf.classifier_order.index('PRICE_REGION')
    sp_index = cf.classifier_order.index('SP')
    as_index = cf.classifier_order.index('assortment')

    # check that the price region is valid
    if price_region not in set(cf_array[:, pr_index]):
        try:
            msg = "no prices defined for price_region '%d'" % int(price_region)
        except:
            msg = "no price_region when setting prices"
        errors.append(msg)
        return -1

    # get species codes found in the cash flow table
    cf_species = set(numpy.unique(cf_array[:,sp_index]))

    # get assortment values found in cash flow table
    cf_assortments = set(numpy.unique(cf_array[:,as_index]))

    # check the species and assortments
    ok = True
    for sp in species:
        for assortment in assortments:
            if sp not in cf_species or assortment not in cf_assortments:
                msg = "assortment '%d' for species '%d' not "\
                      "found in cash flow table '%s'" % \
                      (int(assortment), int(sp), cf.name)
                errors.append(msg)
                ok = False
    if not ok:
        return -1

    # key locations:
    #   key = (species, assortment) tuple
    #   value = location, ie. mapping from key to result array index
    key_locs = {(1,1): 0,
                (2,1): 1,
                (3,1): 2,
                (9,1): 3,
                (1,2): 4,
                (2,2): 5,
                (3,2): 6,
                (9,2): 7}

    # collect the values for each result location
    values = [[] for key in range(max(key_locs.values()) + 1)]
    for row in cf_array:
        preg, sp, assortment, diam, length, price = row
        if preg != price_region:
            continue
        key = (sp, assortment)
        if key not in key_locs:
            continue
        loc = key_locs[key]
        values[loc].append(price)

    # calculate the mean prices and store them to result ar
    for key, loc in key_locs.items():
        prices = values[loc]
        results[loc] = sum(prices) / (1. * len(prices))

    return 1


def decay_dead_trees(data, variables, parameters, par_table_val,
                     cash_flow_table, cash_flow, results, restype,
                     warnings, errors, price_cache, stem_cache):
    """
    Decay model for dead trees, adds trees killed by the natural removal model
    to the trees to decay, and decays dead trees further
    """
    ind = {}

    # simulation
    ind['d_class_width'] = 3
    ind['max_d_class'] = 4
    ind['since_death_class_width'] = 5
    ind['max_sd_class'] = 6
    ind['bmass_coll_prop'] = 7
    
    # stand
    ind['time_step'] = 3
    ind['N_Sp'] = 4
    ind['V_Sp'] = 5
    ind['BM_Sp'] = 6
    ind['D_Sp'] = 7
    ind['density_Sp'] = 8
    ind['N_Ns'] = 9
    ind['V_Ns'] = 10
    ind['BM_Ns'] = 11
    ind['D_Ns'] = 12
    ind['density_Ns'] = 13
    ind['N_b'] = 14
    ind['V_b'] = 15
    ind['BM_b'] = 16
    ind['D_b'] = 17
    ind['density_b'] = 18

    # dead_tree
    ind['sp'] = 4
    ind['d'] = 5
    ind['since_death'] = 6
    ind['snag'] = 7
    ind['decay_class'] = 8
    ind['n'] = 9
    ind['density'] = 10
    ind['v'] = 11
    ind['bm_total'] = 12
    ind['density_ad'] = 13
    ind['v_ad'] = 14
    ind['bm_ad'] = 15

    # tree
    ind['t_sp'] = 4
    ind['t_d'] = 5
    ind['t_density'] = 6
    ind['t_v'] = 7
    ind['t_bm_total'] = 8
    ind['t_n_removed'] = 9

    time_step = data[STANDLABEL][0][ind['time_step']]
    d_width = data[SIMULATIONLABEL][0][ind['d_class_width']]
    max_d = data[SIMULATIONLABEL][0][ind['max_d_class']]
    sd_width = data[SIMULATIONLABEL][0][ind['since_death_class_width']]
    max_sd = data[SIMULATIONLABEL][0][ind['max_sd_class']]
    bmass_collect_prop = data[SIMULATIONLABEL][0][ind['bmass_coll_prop']]

    # go through each d-since_death-snag–class in the data,
    # and move trees in the since_death-classes according to since_death
    # class width and simulation time_step
    matrix = []
    for tree in data[DEADTREELABEL]:
        matrix.append(list(tree))
    tree_ind = {}
    for t_ind, tree in enumerate(matrix):
        sp = tree[ind['sp']]
        d = tree[ind['d']]
        since_death = tree[ind['since_death']]
        snag = tree[ind['snag']]
        tree_ind[(sp, d, since_death, snag)] = t_ind

    matrix.sort(reverse=True,
                key=itemgetter(ind['d'], ind['since_death']))

    # move existing dead trees between classes depending how much
    # time has passed
    for tree in matrix:
        n = tree[ind['n']]
        if n == 0.:
            # there is nothing here, no need to move
            continue
        sp = tree[ind['sp']]
        d = tree[ind['d']]
        since_death = tree[ind['since_death']]
        snag = tree[ind['snag']]
        density = tree[ind['density']]
        v = tree[ind['v']]
        bm_tot = tree[ind['bm_total']]
        
        key = (sp, d, since_death, snag)
        my_ind = tree_ind[key]

        if time_step <= sd_width:
            trans_prop = time_step / sd_width
            all_plus = None
        else:
            trans_prop = (time_step % sd_width) / sd_width
            all_plus = floor(time_step / sd_width)

        if all_plus is not None:
            # move all trees all_plus since_death classes forward
            new_sd = since_death + all_plus * sd_width
            if new_sd > max_sd:
                continue
            to_ind = tree_ind[(sp, d, new_sd, snag)]
            _move_between_since_death_classes(data[DEADTREELABEL], to_ind,
                                              my_ind, ind, 1., v, bm_tot, n, 
                                              density)
            # then move fraction of trees one since_death class forward
            my_ind = to_ind
            new_sd += sd_width
            if new_sd > max_sd:
                continue
            to_ind = tree_ind[(sp, d, new_sd, snag)]
            _move_between_since_death_classes(data[DEADTREELABEL], to_ind,
                                              my_ind, ind, trans_prop, v,
                                              bm_tot, n, density)
        else:
            # move fraction of trees one since_death class forward
            new_sd = since_death + sd_width
            if new_sd > max_sd:
                continue
            to_ind = tree_ind[(sp, d, new_sd, snag)]
            _move_between_since_death_classes(data[DEADTREELABEL], to_ind,
                                              my_ind, ind, trans_prop, v,
                                              bm_tot, n, density)
    # add the freshly killed reserve trees to the first since_death class
    # pine
    if data[STANDLABEL][0][ind['N_Sp']] > 0:
        n = data[STANDLABEL][0][ind['N_Sp']]
        sp = 1.
        d = data[STANDLABEL][0][ind['D_Sp']]
        density = data[STANDLABEL][0][ind['density_Sp']]
        v = data[STANDLABEL][0][ind['V_Sp']]/data[STANDLABEL][0][ind['N_Sp']] #reflects volume per N
        bm = data[STANDLABEL][0][ind['BM_Sp']]
        sd = 0.
        snag = 1.
        my_ind = _get_dead_tree_class_ind(sp, d, d_width, max_d, sd, sd_width,
                                          snag, tree_ind)
        n_old = data[DEADTREELABEL][my_ind][ind['n']]        
        data[DEADTREELABEL][my_ind][ind['v']] = (data[DEADTREELABEL][my_ind][ind['v']]*data[DEADTREELABEL][my_ind][ind['n']]+v*n )/(data[DEADTREELABEL][my_ind][ind['n']]+n)
        #data[DEADTREELABEL][my_ind][ind['v']] += v# (data[DEADTREELABEL][my_ind][ind['v']]*data[DEADTREELABEL][my_ind][ind['n']]+v )/(data[DEADTREELABEL][my_ind][ind['n']]+n)
        data[DEADTREELABEL][my_ind][ind['n']] += n
        #data[DEADTREELABEL][my_ind][ind['v']] += v
        curr_density = data[DEADTREELABEL][my_ind][ind['density']]
        curr_bm = data[DEADTREELABEL][my_ind][ind['bm_total']]
        new_density = (curr_density * curr_bm + density * bm)\
                      / (curr_bm + bm)
        data[DEADTREELABEL][my_ind][ind['density']] = new_density 
        
        data[DEADTREELABEL][my_ind][ind['bm_total']] += bm
        #data[DEADTREELABEL][my_ind][ind['bm_total']] = (data[DEADTREELABEL][my_ind][ind['bm_total']]*n_old+bm * n)/(n_old+n)
    # spruce
    elif data[STANDLABEL][0][ind['N_Ns']] > 0:
        n = data[STANDLABEL][0][ind['N_Ns']]
        sp = 2.
        d = data[STANDLABEL][0][ind['D_Ns']]
        density = data[STANDLABEL][0][ind['density_Ns']]
        v = data[STANDLABEL][0][ind['V_Ns']]/data[STANDLABEL][0][ind['N_Ns']]
        bm = data[STANDLABEL][0][ind['BM_Ns']]
        sd = 0.
        snag = 1.
        my_ind = _get_dead_tree_class_ind(sp, d, d_width, max_d, sd, sd_width,
                                          snag, tree_ind)
        n_old = data[DEADTREELABEL][my_ind][ind['n']]
        data[DEADTREELABEL][my_ind][ind['v']] = (data[DEADTREELABEL][my_ind][ind['v']]*data[DEADTREELABEL][my_ind][ind['n']]+v*n )/(data[DEADTREELABEL][my_ind][ind['n']]+n)
        #data[DEADTREELABEL][my_ind][ind['v']] += v# (data[DEADTREELABEL][my_ind][ind['v']]*data[DEADTREELABEL][my_ind][ind['n']]+v )/(data[DEADTREELABEL][my_ind][ind['n']]+n)
        data[DEADTREELABEL][my_ind][ind['n']] += n
        #data[DEADTREELABEL][my_ind][ind['v']] += v
        curr_density = data[DEADTREELABEL][my_ind][ind['density']]
        curr_bm = data[DEADTREELABEL][my_ind][ind['bm_total']]
        new_density = (curr_density * curr_bm + density * bm)\
                      / (curr_bm + bm)
        data[DEADTREELABEL][my_ind][ind['density']] = new_density 
        data[DEADTREELABEL][my_ind][ind['bm_total']] += bm    
        #(data[DEADTREELABEL][my_ind][ind['bm_total']]*data[DEADTREELABEL][my_ind][ind['n']]+bm * n)/(data[DEADTREELABEL][my_ind][ind['n']]+n)
    # deciduos
    elif data[STANDLABEL][0][ind['N_b']] > 0:
        n = data[STANDLABEL][0][ind['N_b']]
        sp = 3.
        d = data[STANDLABEL][0][ind['D_b']]
        density = data[STANDLABEL][0][ind['density_b']]
        v = data[STANDLABEL][0][ind['V_b']]/data[STANDLABEL][0][ind['N_b']]
        #v = data[STANDLABEL][0][ind['V_b']]
        bm = data[STANDLABEL][0][ind['BM_b']]
        sd = 0.
        snag = 1.
        my_ind = _get_dead_tree_class_ind(sp, d, d_width, max_d, sd, sd_width,
                                          snag, tree_ind)
        n_old = data[DEADTREELABEL][my_ind][ind['n']]
        data[DEADTREELABEL][my_ind][ind['v']] = (data[DEADTREELABEL][my_ind][ind['v']]*data[DEADTREELABEL][my_ind][ind['n']]+v*n )/(data[DEADTREELABEL][my_ind][ind['n']]+n)
        #data[DEADTREELABEL][my_ind][ind['v']] += v#(data[DEADTREELABEL][my_ind][ind['v']]*data[DEADTREELABEL][my_ind][ind['n']]+v )/(data[DEADTREELABEL][my_ind][ind['n']]+n)
        data[DEADTREELABEL][my_ind][ind['n']] += n
        #data[DEADTREELABEL][my_ind][ind['v']] += v
        curr_density = data[DEADTREELABEL][my_ind][ind['density']]
        curr_bm = data[DEADTREELABEL][my_ind][ind['bm_total']]
        new_density = (curr_density * curr_bm + density * bm)\
                      / (curr_bm + bm)
        data[DEADTREELABEL][my_ind][ind['density']] = new_density 
        
        data[DEADTREELABEL][my_ind][ind['bm_total']] += bm    
        #data[DEADTREELABEL][my_ind][ind['bm_total']] = (data[DEADTREELABEL][my_ind][ind['bm_total']]*n_old+bm * n)/(n_old+n)
    
    # add the freshly killed trees to the first since_death class
    for tree in data[TREELABEL]:
        n = tree[ind['t_n_removed']]
        if n == 0.0:
            continue
        sp = tree[ind['t_sp']]
        # map the sp to the sp classes used for dead trees
        if int(sp) not in (1, 2, 3):
            if sp == 8:
                sp = 1.
            else:
                sp = 3.
        d = tree[ind['t_d']]
        density = tree[ind['t_density']]
        v = tree[ind['t_v']]*(1-bmass_collect_prop)
        bm = tree[ind['t_bm_total']]*(1-bmass_collect_prop)
        sd = 0.
        snag = 1.
        
        
        
        my_ind = _get_dead_tree_class_ind(sp, d, d_width, max_d, sd, sd_width,
                                          snag, tree_ind)
        
        data[DEADTREELABEL][my_ind][ind['v']] = (data[DEADTREELABEL][my_ind][ind['v']]*data[DEADTREELABEL][my_ind][ind['n']]+v * n)/(data[DEADTREELABEL][my_ind][ind['n']]+n)
        #data[DEADTREELABEL][my_ind][ind['v']] += v * n
        n_old = data[DEADTREELABEL][my_ind][ind['n']]
        data[DEADTREELABEL][my_ind][ind['n']] += n
        
        curr_density = data[DEADTREELABEL][my_ind][ind['density']]
        curr_bm = data[DEADTREELABEL][my_ind][ind['bm_total']]
        new_density = (curr_density * curr_bm + density * bm * n)\
                      / (curr_bm + bm * n)
        data[DEADTREELABEL][my_ind][ind['density']] = new_density 
        
        #data[DEADTREELABEL][my_ind][ind['bm_total']] += bm * n
        to_write = (data[DEADTREELABEL][my_ind][ind['bm_total']]*data[DEADTREELABEL][my_ind][ind['n']]+bm * n)/(data[DEADTREELABEL][my_ind][ind['n']]+n)
        #data[DEADTREELABEL][my_ind][ind['bm_total']] += bm*n#(data[DEADTREELABEL][my_ind][ind['bm_total']]*data[DEADTREELABEL][my_ind][ind['n']]+bm * n)/(data[DEADTREELABEL][my_ind][ind['n']]+n)
        data[DEADTREELABEL][my_ind][ind['bm_total']] = (data[DEADTREELABEL][my_ind][ind['bm_total']]*n_old+bm * n)/(n_old+n)
        #hberg = open('C:/MyTemp/temp3.txt', 'a')
        #hberg.write(str(str(to_write)+'\t'+str(data[DEADTREELABEL][my_ind][ind['bm_total']])+'\r'))
        #hberg.close()
    
    # decay trees further, one diam class at a time, starting with snags, as
    # they can fall as a result of decaying, and changes the snag=0 class
    # amounts as a result
    all_classes = tree_ind.keys()
    all_classes.sort(reverse=True, key=itemgetter(3, 2, 1))
    for cls in all_classes:
        my_ind = tree_ind[cls]
        tree = data[DEADTREELABEL][my_ind]
        n = tree[ind['n']]
        if n == 0.0:
            # nothing here, so zero other values too
            tree[ind['density']] = 0.
            tree[ind['v']] = 0.
            tree[ind['bm_total']] = 0.
            tree[ind['bm_ad']] = 0.
            tree[ind['v_ad']] = 0.
            tree[ind['density_ad']] = 0.
            tree[ind['decay_class']] = 0.
            continue
            
        sp = tree[ind['sp']]
        d = tree[ind['d']]
        sd = tree[ind['since_death']]
        snag = tree[ind['snag']]
        density = tree[ind['density']]
        v = tree[ind['v']]
        bm_tot = tree[ind['bm_total']]
        res = _decay_class_Makinenym(sp, d, density, sd, v, snag, bm_tot)
        decay_class, new_snag, mass_ad, v_ad, density_ad = res
        if new_snag != snag:
            # the tree has fallen down, it'll change its class
            to_ind = _get_dead_tree_class_ind(sp, d, d_width, max_d, sd,
                                              sd_width, new_snag, tree_ind)
            # now move the biomass from snag to no snag class. That will
            # then be decayed in the snag=0 round of decaying
            _move_between_since_death_classes(data[DEADTREELABEL], to_ind,
                                              my_ind, ind, 1., v, bm_tot, n, 
                                              density)
        else:
            # delete trees when decayed density is less than 50 kg/m3
            if density_ad < 50.:
                mass_ad = 0.
                v_ad = 0.
                decay_class = 0.
                density_ad = 0.
                data[DEADTREELABEL][my_ind][ind['n']] = 0.

            data[DEADTREELABEL][my_ind][ind['decay_class']] = decay_class
            data[DEADTREELABEL][my_ind][ind['snag']] = snag
            data[DEADTREELABEL][my_ind][ind['bm_ad']] = mass_ad
            data[DEADTREELABEL][my_ind][ind['v_ad']] = v_ad
            data[DEADTREELABEL][my_ind][ind['density_ad']] = density_ad
            # mark dead tree classes as modified
            data[DEADTREELABEL][my_ind][-1] = 1.
        #if data[DEADTREELABEL][my_ind][ind['v']] > 8:
        #    import pdb;pdb.set_trace()
    return 1

def decay_dead_trees_without_tree_level(data, variables, parameters, par_table_val,
                     cash_flow_table, cash_flow, results, restype,
                     warnings, errors, price_cache, stem_cache):
    """
    Decay model for dead trees, calculates the initial value of dead trees, 
    adds reserve trees killed by the simple model to the trees to decay, and decays dead trees further
    """
    ind = {}

    # simulation
    ind['d_class_width'] = 3
    ind['max_d_class'] = 4
    ind['since_death_class_width'] = 5
    ind['max_sd_class'] = 6
    ind['bmass_coll_prop'] = 7

    # stand
    ind['time_step'] = 3
    ind['N_Sp'] = 4
    ind['V_Sp'] = 5
    ind['BM_Sp'] = 6
    ind['D_Sp'] = 7
    ind['density_Sp'] = 8
    ind['N_Ns'] = 9
    ind['V_Ns'] = 10
    ind['BM_Ns'] = 11
    ind['D_Ns'] = 12
    ind['density_Ns'] = 13
    ind['N_b'] = 14
    ind['V_b'] = 15
    ind['BM_b'] = 16
    ind['D_b'] = 17
    ind['density_b'] = 18

    # dead_tree
    ind['sp'] = 4
    ind['d'] = 5
    ind['since_death'] = 6
    ind['snag'] = 7
    ind['decay_class'] = 8
    ind['n'] = 9
    ind['density'] = 10
    ind['v'] = 11
    ind['bm_total'] = 12
    ind['density_ad'] = 13
    ind['v_ad'] = 14
    ind['bm_ad'] = 15

    time_step = data[STANDLABEL][0][ind['time_step']]
    d_width = data[SIMULATIONLABEL][0][ind['d_class_width']]
    max_d = data[SIMULATIONLABEL][0][ind['max_d_class']]
    sd_width = data[SIMULATIONLABEL][0][ind['since_death_class_width']]
    max_sd = data[SIMULATIONLABEL][0][ind['max_sd_class']]

    # go through each d-since_death-snag–class in the data,
    # and move trees in the since_death-classes according to since_death
    # class width and simulation time_step
    matrix = []
    for tree in data[DEADTREELABEL]:
        matrix.append(list(tree))
    tree_ind = {}
    for t_ind, tree in enumerate(matrix):
        sp = tree[ind['sp']]
        d = tree[ind['d']]
        since_death = tree[ind['since_death']]
        snag = tree[ind['snag']]
        tree_ind[(sp, d, since_death, snag)] = t_ind

    matrix.sort(reverse=True,
                key=itemgetter(ind['d'], ind['since_death']))

    # move existing dead trees between classes depending how much
    # time has passed
    for tree in matrix:
        n = tree[ind['n']]
        if n == 0.:
            # there is nothing here, no need to move
            continue
        sp = tree[ind['sp']]
        d = tree[ind['d']]
        since_death = tree[ind['since_death']]
        snag = tree[ind['snag']]
        density = tree[ind['density']]
        v = tree[ind['v']]
        bm_tot = tree[ind['bm_total']]
        
        key = (sp, d, since_death, snag)
        my_ind = tree_ind[key]

        if time_step <= sd_width:
            trans_prop = time_step / sd_width
            all_plus = None
        else:
            trans_prop = (time_step % sd_width) / sd_width
            all_plus = floor(time_step / sd_width)

        if all_plus is not None:
            # move all trees all_plus since_death classes forward
            new_sd = since_death + all_plus * sd_width
            if new_sd > max_sd:
                continue
            to_ind = tree_ind[(sp, d, new_sd, snag)]
            _move_between_since_death_classes(data[DEADTREELABEL], to_ind,
                                              my_ind, ind, 1., v, bm_tot, n, 
                                              density)
            # then move fraction of trees one since_death class forward
            my_ind = to_ind
            new_sd += sd_width
            if new_sd > max_sd:
                continue
            to_ind = tree_ind[(sp, d, new_sd, snag)]
            _move_between_since_death_classes(data[DEADTREELABEL], to_ind,
                                              my_ind, ind, trans_prop, v,
                                              bm_tot, n, density)
        else:
            # move fraction of trees one since_death class forward
            new_sd = since_death + sd_width
            if new_sd > max_sd:
                continue
            to_ind = tree_ind[(sp, d, new_sd, snag)]
            _move_between_since_death_classes(data[DEADTREELABEL], to_ind,
                                              my_ind, ind, trans_prop, v,
                                              bm_tot, n, density)
    # add the freshly killed reserve trees to the first since_death class
    # pine
    if data[STANDLABEL][0][ind['N_Sp']] > 0:
        n = data[STANDLABEL][0][ind['N_Sp']]
        sp = 1.
        d = data[STANDLABEL][0][ind['D_Sp']]
        density = data[STANDLABEL][0][ind['density_Sp']]
        v = data[STANDLABEL][0][ind['V_Sp']]
        v = data[STANDLABEL][0][ind['V_Sp']]/data[STANDLABEL][0][ind['N_Sp']]
        bm = data[STANDLABEL][0][ind['BM_Sp']]
        sd = 0.
        snag = 1.
        my_ind = _get_dead_tree_class_ind(sp, d, d_width, max_d, sd, sd_width,
                                          snag, tree_ind)
        n_old = data[DEADTREELABEL][my_ind][ind['n']]
        n_new = n
        curr_vol = data[DEADTREELABEL][my_ind][ind['v']]
        data[DEADTREELABEL][my_ind][ind['v']] = (data[DEADTREELABEL][my_ind][ind['v']]*data[DEADTREELABEL][my_ind][ind['n']]+v*n )/(data[DEADTREELABEL][my_ind][ind['n']]+n)
        #data[DEADTREELABEL][my_ind][ind['v']] += v# (data[DEADTREELABEL][my_ind][ind['v']]*data[DEADTREELABEL][my_ind][ind['n']]+v )/(data[DEADTREELABEL][my_ind][ind['n']]+n)
        data[DEADTREELABEL][my_ind][ind['n']] += n
        #data[DEADTREELABEL][my_ind][ind['v']] += v
        curr_density = data[DEADTREELABEL][my_ind][ind['density']]
        curr_bm = data[DEADTREELABEL][my_ind][ind['bm_total']]
        new_density = (curr_density * curr_bm + density * bm)\
                      / (curr_bm + bm)
        data[DEADTREELABEL][my_ind][ind['density']] = new_density 
        
        data[DEADTREELABEL][my_ind][ind['bm_total']] += bm
        #data[DEADTREELABEL][my_ind][ind['bm_total']] = (data[DEADTREELABEL][my_ind][ind['bm_total']]*n_old+bm * n)/(n_old+n)
        #if data[DEADTREELABEL][my_ind][ind['v']] > 8:
        #    import pdb;pdb.set_trace()
    # spruce
    elif data[STANDLABEL][0][ind['N_Ns']] > 0:
        n = data[STANDLABEL][0][ind['N_Ns']]
        sp = 2.
        d = data[STANDLABEL][0][ind['D_Ns']]
        density = data[STANDLABEL][0][ind['density_Ns']]
        v = data[STANDLABEL][0][ind['V_Ns']]/data[STANDLABEL][0][ind['N_Ns']]
        #v = data[STANDLABEL][0][ind['V_Ns']]
        bm = data[STANDLABEL][0][ind['BM_Ns']]
        sd = 0.
        snag = 1.
        my_ind = _get_dead_tree_class_ind(sp, d, d_width, max_d, sd, sd_width,
                                          snag, tree_ind)
        n_old = data[DEADTREELABEL][my_ind][ind['n']]
        data[DEADTREELABEL][my_ind][ind['v']] = (data[DEADTREELABEL][my_ind][ind['v']]*data[DEADTREELABEL][my_ind][ind['n']]+v*n )/(data[DEADTREELABEL][my_ind][ind['n']]+n)
        #data[DEADTREELABEL][my_ind][ind['v']] += v# (data[DEADTREELABEL][my_ind][ind['v']]*data[DEADTREELABEL][my_ind][ind['n']]+v )/(data[DEADTREELABEL][my_ind][ind['n']]+n)
        data[DEADTREELABEL][my_ind][ind['n']] += n
        #data[DEADTREELABEL][my_ind][ind['v']] += v
        curr_density = data[DEADTREELABEL][my_ind][ind['density']]
        curr_bm = data[DEADTREELABEL][my_ind][ind['bm_total']]
        new_density = (curr_density * curr_bm + density * bm)\
                      / (curr_bm + bm)
        data[DEADTREELABEL][my_ind][ind['density']] = new_density 
        
        data[DEADTREELABEL][my_ind][ind['bm_total']] += bm
        #data[DEADTREELABEL][my_ind][ind['bm_total']] = (data[DEADTREELABEL][my_ind][ind['bm_total']]*n_old+bm * n)/(n_old+n)
        #if data[DEADTREELABEL][my_ind][ind['v']] > 8:
        #    import pdb;pdb.set_trace()
    # deciduos
    elif data[STANDLABEL][0][ind['N_b']] > 0:
        n = data[STANDLABEL][0][ind['N_b']]
        sp = 3.
        d = data[STANDLABEL][0][ind['D_b']]
        density = data[STANDLABEL][0][ind['density_b']]
        v = data[STANDLABEL][0][ind['V_b']]/data[STANDLABEL][0][ind['N_b']]
        #v = data[STANDLABEL][0][ind['V_b']]
        bm = data[STANDLABEL][0][ind['BM_b']]
        sd = 0.
        snag = 1.
        my_ind = _get_dead_tree_class_ind(sp, d, d_width, max_d, sd, sd_width,
                                          snag, tree_ind)
        n_old = data[DEADTREELABEL][my_ind][ind['n']]
        curr_vol = data[DEADTREELABEL][my_ind][ind['v']] 
        data[DEADTREELABEL][my_ind][ind['v']] = (data[DEADTREELABEL][my_ind][ind['v']]*data[DEADTREELABEL][my_ind][ind['n']]+v*n )/(data[DEADTREELABEL][my_ind][ind['n']]+n)
        #data[DEADTREELABEL][my_ind][ind['v']] += v# (data[DEADTREELABEL][my_ind][ind['v']]*data[DEADTREELABEL][my_ind][ind['n']]+v )/(data[DEADTREELABEL][my_ind][ind['n']]+n)
        data[DEADTREELABEL][my_ind][ind['n']] += n
        #data[DEADTREELABEL][my_ind][ind['v']] += v
        curr_density = data[DEADTREELABEL][my_ind][ind['density']]
        curr_bm = data[DEADTREELABEL][my_ind][ind['bm_total']]
        #import pdb; pdb.set_trace()
        new_density = (curr_density * curr_bm + density * bm)\
                      / (curr_bm + bm)
        data[DEADTREELABEL][my_ind][ind['density']] = new_density 
        
        data[DEADTREELABEL][my_ind][ind['bm_total']] += bm
        #data[DEADTREELABEL][my_ind][ind['bm_total']] = (data[DEADTREELABEL][my_ind][ind['bm_total']]*n_old+bm * n)/(n_old+n)
        #if data[DEADTREELABEL][my_ind][ind['v']] > 8:
        #    import pdb;pdb.set_trace()

    # decay trees further, one diam class at a time, starting with snags, as
    # they can fall as a result of decaying, and changes the snag=0 class
    # amounts as a result
    all_classes = tree_ind.keys()
    all_classes.sort(reverse=True, key=itemgetter(3, 2, 1))
    for cls in all_classes:
        my_ind = tree_ind[cls]
        tree = data[DEADTREELABEL][my_ind]
        n = tree[ind['n']]
        if n == 0.0:
            # nothing here, so zero other values too
            tree[ind['density']] = 0.
            tree[ind['v']] = 0.
            tree[ind['bm_total']] = 0.
            tree[ind['bm_ad']] = 0.
            tree[ind['v_ad']] = 0.
            tree[ind['density_ad']] = 0.
            tree[ind['decay_class']] = 0.
            continue
            
        sp = tree[ind['sp']]
        d = tree[ind['d']]
        sd = tree[ind['since_death']]
        snag = tree[ind['snag']]
        density = tree[ind['density']]
        v = tree[ind['v']]
        bm_tot = tree[ind['bm_total']]
        res = _decay_class_Makinenym(sp, d, density, sd, v, snag, bm_tot)
        decay_class, new_snag, mass_ad, v_ad, density_ad = res
        if new_snag != snag:
            # the tree has fallen down, it'll change its class
            to_ind = _get_dead_tree_class_ind(sp, d, d_width, max_d, sd,
                                              sd_width, new_snag, tree_ind)
            # now move the biomass from snag to no snag class. That will
            # then be decayed in the snag=0 round of decaying
            _move_between_since_death_classes(data[DEADTREELABEL], to_ind,
                                              my_ind, ind, 1., v, bm_tot, n, 
                                              density)
        else:
            # delete trees when decayed density is less than 50 kg/m3
            if density_ad < 50.:
                mass_ad = 0.
                v_ad = 0.
                decay_class = 0.
                density_ad = 0.
                data[DEADTREELABEL][my_ind][ind['n']] = 0.

            data[DEADTREELABEL][my_ind][ind['decay_class']] = decay_class
            data[DEADTREELABEL][my_ind][ind['snag']] = snag
            data[DEADTREELABEL][my_ind][ind['bm_ad']] = mass_ad
            data[DEADTREELABEL][my_ind][ind['v_ad']] = v_ad
            data[DEADTREELABEL][my_ind][ind['density_ad']] = density_ad
            # mark dead tree classes as modified
            data[DEADTREELABEL][my_ind][-1] = 1.
        #if data[DEADTREELABEL][my_ind][ind['v']] > 8:
        #    import pdb;pdb.set_trace()

    return 1


def _get_dead_tree_class_ind(sp, d, d_width, max_d, sd, sd_width, snag,
                             tree_ind):
    """
    Determine the dead_tree class index this tree belongs to

    sp -- tree species
    d -- tree diameter
    d_width -- dead_tree diameter class width
    max_d -- dead_tree maximum diameter for the classification
    sd -- since_death of the tree
    sd_width -- since_death class width for the classification
    snag -- standing tree (1) of fallen down (0)
    tree_ind -- dictionary mapping the classifiers to data table index
    """
    # which diameter class does this diameter belong to?
    how_many = floor(d / d_width)
    d_class = d_width / 2. + how_many * d_width
    # this is the first since_death class, as these are freshly dead
    sd = sd_width / 2.
    my_key = (sp, d_class, sd, snag)
    if my_key in tree_ind:
        my_ind = tree_ind[my_key]
    else:
        # this has too big a diameter, let's place it in the last d class
        d_classes = ceil(max_d / d_width)
        d_class = d_width / 2. + (d_classes - 1.) * d_width
        my_key = (sp, d_class, sd, 1.)
        my_ind = tree_ind[my_key]
    return my_ind


def _move_between_since_death_classes(dead_trees, to_ind, my_ind, ind,
                                      trans_prop, v, bm_tot, n, density):
    """
    Move trans_prop share from my_ind since_death class to to_ind class
    for the class specified by ind
    """
    #hberg = open('C:/MyTemp/temp3.txt', 'a')
    curr_density = dead_trees[to_ind][ind['density']]
    curr_bm = dead_trees[to_ind][ind['bm_total']]
    new_density = (curr_density * curr_bm + density * bm_tot) \
                  / (curr_bm + bm_tot)
    
    curr_v = dead_trees[to_ind][ind['v']]
    n_old = dead_trees[to_ind][ind['n']]
    dead_trees[to_ind][ind['v']] += v * trans_prop
    #dead_trees[to_ind][ind['v']] = (dead_trees[to_ind][ind['v']]*n_old+ v * trans_prop *n) / (n_old+n*trans_prop)
    dead_trees[to_ind][ind['bm_total']] += bm_tot * trans_prop
    
    #hberg.write(str(dead_trees[to_ind][ind['v']])+'\t')
    #dead_trees[to_ind][ind['bm_total']] = (dead_trees[to_ind][ind['bm_total']]*n_old+ bm_tot * trans_prop *n) / (n_old+n*trans_prop)
    dead_trees[to_ind][ind['n']] += n * trans_prop
    
    dead_trees[to_ind][ind['density']] = new_density
    dead_trees[to_ind][-1] = 1.
    n_old = dead_trees[my_ind][ind['n']]
    dead_trees[my_ind][ind['n']] -= n * trans_prop
    if dead_trees[my_ind][ind['n']] == 0.:
        # all gone, zero everything
        dead_trees[my_ind][ind['density']] = 0.
        dead_trees[my_ind][ind['v']] = 0.
        dead_trees[my_ind][ind['bm_total']] = 0.
        dead_trees[my_ind][ind['bm_ad']] = 0.
        dead_trees[my_ind][ind['v_ad']] = 0.
        dead_trees[my_ind][ind['density_ad']] = 0.
        dead_trees[my_ind][ind['decay_class']] = 0.
    else:
        
        
        #hberg.write(str(str((dead_trees[my_ind][ind['bm_total']]*n_old- bm_tot * trans_prop *n) / (n_old-n*trans_prop))+'\r'))
        #hberg.close()
        #dead_trees[my_ind][ind['v']] = (dead_trees[my_ind][ind['v']]*n_old- v * trans_prop *n) / (n_old-n*trans_prop)
        dead_trees[my_ind][ind['v']] -= v * trans_prop
        dead_trees[my_ind][ind['bm_total']] -= bm_tot * trans_prop
        
        #dead_trees[my_ind][ind['bm_total']] = (dead_trees[my_ind][ind['bm_total']]*n_old- bm_tot * trans_prop *n) / (n_old-n*trans_prop)
        #except:
        #    import pdb;pdb.set_trace()
    #hberg.write(str(dead_trees[my_ind][ind['v']])+'\r')
    #if dead_trees[to_ind][ind['v']] > 8:
    #    import pdb;pdb.set_trace()
    #hberg.close()
    dead_trees[my_ind][-1] = 1.
    


def _decay_class_Makinenym(sp, d, density, since_death, v, snag,
                           bm_total):
    """
    Decay tree material, determine whether the tree is a standing dead tree,
    snag, or whether it's lying on the ground
    """
    # calculate probability that a tree remain standing as a snag after
    # death, fraction of density, volume and mass
    if sp == 1 or sp == 8:
        snag_p = exp(1.304 - 0.121 * since_death + 0.055 * d) / \
            (1 + exp(1.304 - 0.121 * since_death + 0.055 * d))
        fraction_density = 1 - pow(1 - exp(-0.072 * since_death), 5)
        fraction_v = 1 - pow(1-exp(-0.062*since_death), 5)
        fraction_mass = 1 - pow(1-exp(-0.095*since_death), 5)
    elif sp == 2:
        snag_p = exp(3.278-0.115*since_death-0.062*d) / \
            (1+exp(3.278-0.115*since_death-0.062*d))
        fraction_density = 1 - pow(1-exp(-0.066*since_death), 5)
        fraction_v = 1 - pow(1-exp(-0.058*since_death), 5)
        fraction_mass = 1 - pow(1-exp(-0.085*since_death), 5)
    else:  # deciduous species
        snag_p = exp(1.988-0.249*since_death+0.119*d) / \
            (1+exp(1.988-0.249*since_death+0.119*d))
        fraction_density = 1 - pow(1-exp(-0.177*since_death), 5)
        fraction_v = 1 - pow(1-exp(-0.113*since_death), 5)
        fraction_mass = 1 - pow(1-exp(-0.213*since_death), 5)

    if fraction_density > 1.:
        fraction_density = 1.
    if fraction_v > 1.:
        fraction_v = 1.
    if fraction_mass > 1.:
        fraction_mass = 1.
    density_ad = density * fraction_density
    v_ad = v * fraction_v
    mass_ad = bm_total * fraction_mass

    # snag or not?
    do_i_fall = random.random()
    if snag == 1.:
        if (do_i_fall > snag_p):
            snag = 0.

    # calculate decay_class
    if snag == 1.:
        if sp == 1. or sp == 8.:
            if (fraction_density >= 0.8261):
                decay_class = 1.
            elif (fraction_density >= 0.7229 and fraction_density < 0.8261):
                decay_class = 2.
            elif (fraction_density >= 0.6276 and fraction_density < 0.7229):
                decay_class = 3.
            elif (fraction_density >= 0.1 and fraction_density < 0.6276):
                decay_class = 4.
            else:
                # fraction_density < 0.1, value not given in Mäkinen et al.
                decay_class = 5.
        elif sp == 2.:
            if (fraction_density >= 0.8584):
                decay_class = 1.
            elif (fraction_density >= 0.720 and fraction_density < 0.8584):
                decay_class = 2.
            elif (fraction_density >= 0.5533 and fraction_density < 0.720):
                decay_class = 3.
            elif (fraction_density >= 0.1 and fraction_density < 0.5533):
                decay_class = 4.
            else:
                # fraction_density < 0.1, value not given in Mäkinen et al.
                decay_class = 5.
        else:
            # deciduous species
            if (fraction_density >= 0.8029):
                decay_class = 1.
            elif (fraction_density >= 0.6324 and fraction_density < 0.8029):
                decay_class = 2.
            elif (fraction_density >= 0.5379 and fraction_density < 0.6324):
                decay_class = 3.
            elif (fraction_density >= 0.3629 and fraction_density < 0.5379):
                decay_class = 4.
            else:
                # fraction_density < 0.3629
                decay_class = 5.
    else:
        # snag == 0
        if (sp == 1. or sp == 8.):
            if (fraction_density >= 0.7935):
                decay_class = 1.
            elif (fraction_density >= 0.6239 and fraction_density < 0.7935):
                decay_class = 2.
            elif (fraction_density >= 0.4263 and fraction_density < 0.6239):
                decay_class = 3.
            elif (fraction_density >= 0.2927 and fraction_density < 0.4263):
                decay_class = 4.
            else:
                # fraction_density < 0.2927
                decay_class = 5.
        elif (sp == 2.):
            if (fraction_density >= 0.8161):
                decay_class = 1.
            elif (fraction_density >= 0.6776 and fraction_density < 0.8161):
                decay_class = 2.
            elif (fraction_density >= 0.4636 and fraction_density < 0.6776):
                decay_class = 3.
            elif (fraction_density >= 0.269 and fraction_density < 0.4636):
                decay_class = 4.
            else:
                # fraction_density < 0.269
                decay_class = 5.
        else:
            # deciduous species
            if (fraction_density >= 0.8029):
                # was originally 0.8578
                # - changed to 0.8029 (same as snag = 1 for decay class 1)
                decay_class = 1.
            elif (fraction_density >= 0.6245 and fraction_density < 0.8029):
                decay_class = 2.
            elif (fraction_density >= 0.4043 and fraction_density < 0.6245):
                decay_class = 3.
            elif (fraction_density >= 0.2609 and fraction_density < 0.4043):
                decay_class = 4.
            else:
                # fraction_density < 0.2609
                decay_class = 5.

    return (decay_class, snag, mass_ad, v_ad, density_ad)


def main_sp(data, variables, parameters, par_table_val, cash_flow_table,
            cash_flow, results, restype, warnings, errors, price_cache,
            stem_cache):
    """
    calculates mains species. Main species is the growing species of stand
    - not the biggest species calculated as basal area or stem number
    """
    ind = {}
    STANDLABEL = 1
    STRATUMLABEL = 2
    ind['stand_open_area'] = 3
    ind['stratum_storey'] = 4
    ind['stratum_sp'] = 5
    ind['stratum_n'] = 6
    ind['stratum_ba'] = 7
    ind['stratum_artif_ingrowth'] = 8

    # check that strata actually exists
    if data[STANDLABEL][0][ind['stand_open_area']] == 1:
        results[0] = None
        return 1

    sppref = list(par_table_val[0][0])
    stratumdata = data[STRATUMLABEL]
    artif_ingr = False
    growing_storey = False
    artif = [s[ind['stratum_artif_ingrowth']] for s in stratumdata]
    st = [s[ind['stratum_storey']] for s in stratumdata]
    for a in artif:
        if a == 1:
            artif_ingr = True
            break
    for a in st:
        if a in [1, 5]:
            growing_storey = True
            break

    new_stratumdata = {}
    # Go through strata and pick up strata with artificial ingrowth
    # If not artificial inrowth pick up strata with storey 1 and 5
    # Sum strata with the same tree species together
    for stratum in stratumdata:
        sp = stratum[ind['stratum_sp']]
        n = stratum[ind['stratum_n']]
        ba = stratum[ind['stratum_ba']]
        artif_ingrowth = stratum[ind['stratum_artif_ingrowth']]
        storey = stratum[ind['stratum_storey']]
        stratum_sp = sp
        if artif_ingr and growing_storey:
            if stratum_sp not in new_stratumdata and artif_ingrowth and \
                    storey in [1, 5]:
                new_stratumdata[stratum_sp] = 0, 0
                o_ba, o_n = new_stratumdata[stratum_sp]
                new_stratumdata[stratum_sp] = (ba + o_ba, n + o_n)
            elif artif_ingrowth and storey in [1, 5]:
                o_ba, o_n = new_stratumdata[stratum_sp]
                new_stratumdata[stratum_sp] = (ba + o_ba, n + o_n)
        elif growing_storey:
            if stratum_sp not in new_stratumdata and storey in [1, 5]:
                new_stratumdata[stratum_sp] = 0, 0
                o_ba, o_n = new_stratumdata[stratum_sp]
                new_stratumdata[stratum_sp] = (ba + o_ba, n + o_n)
            elif storey in [1, 5]:
                o_ba, o_n = new_stratumdata[stratum_sp]
                new_stratumdata[stratum_sp] = (ba + o_ba, n + o_n)
        else:
            if stratum_sp not in new_stratumdata:
                new_stratumdata[stratum_sp] = 0, 0
                o_ba, o_n = new_stratumdata[stratum_sp]
                new_stratumdata[stratum_sp] = (ba + o_ba, n + o_n)
            else:
                o_ba, o_n = new_stratumdata[stratum_sp]
                new_stratumdata[stratum_sp] = (ba + o_ba, n + o_n)

    found = False
    # Go through strata in preference order and choose species of stratum
    # as comp_unit's main species if stratum's tree number is more than 1200
    # or stratum's basal area more than 10
    for sp in sppref:
        if sp in new_stratumdata:
            for sp_strat, ba_n_strat in new_stratumdata.iteritems():
                if sp == sp_strat:
                    if ba_n_strat[0] > 10 or ba_n_strat[1] > 1200:
                        found = True
                        results[0] = sp_strat
                        return 1
    # If any of strata has more than 1200 trees/ha or 10 m2/ha
    # go through again with lower tree number and basal area restriction
    if not found:
        for sp in sppref:
            if sp in new_stratumdata:
                for sp_strat, ba_n_strat in new_stratumdata.iteritems():
                    if sp == sp_strat:
                        if ba_n_strat[0] > 7 or ba_n_strat[1] > 800:
                            found = True
                            results[0] = sp_strat
                            return 1
    # If any of strata has more than 800 trees/ha or 7 m2/ha
    # go through again without tree number and basal area restriction
    if not found:
        for sp in sppref:
            if sp in new_stratumdata:
                for sp_strat, ba_n_strat in new_stratumdata.iteritems():
                    if sp == sp_strat:
                        if ba_n_strat[0] > 0 or ba_n_strat[1] > 0:
                            found = True
                            results[0] = sp_strat
                            return 1

    return 1
