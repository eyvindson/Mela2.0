#!/usr/bin/env python
# -*- coding: utf-8 -*-
import y07
import numpy

# maximum likelihood parameters of the yasso07 model
ML_PARAM = numpy.array((-0.70359426736831665,
                         -5.6810555458068848,
                         -0.2613542377948761,
                         -0.02810959704220295,
                         0.48885279893875122,
                         0.019057683646678925,
                         0.96963745355606079,
                         0.98725599050521851,
                         0.0028432635590434074,
                         0.0033964612521231174,
                         1.3993703760206699e-05,
                         1.7966924133361317e-05,
                         0.01218125969171524,
                         0.0027778467629104853,
                         0.012695553712546825,
                         0.97138279676437378,
                         0.098731838166713715,
                         -0.001571640488691628,
                         0.17000000178813934,
                         -0.001500000013038516,
                         0.17000000178813934,
                         -0.001500000013038516,
                         0.17000000178813934,
                         -0.001500000013038516,
                         0.0,
                         -1.2716917991638184,
                         0.0,
                         101.82534790039062,
                         260.0,
                         -0.15269890427589417,
                         -0.00039342229138128459,
                         -0.33000001311302185,
                         0.0,
                         0.0,
                         -0.0014966174494475126,
                         0.0042703705839812756,
                         0.0,
                         0.0,
                         -1.7084113359451294,
                         0.8585553765296936,
                         -0.30680140852928162,
                         0.0,
                         0.58340001106262207,
                         1.0,
                         10299.29296875), dtype=numpy.float32)

def yasso07(args, index):
    """
    The Python frontend to the Yasso07 soil carbon Fortran-model for a maximum
    likelihood run.

    dur -- soil carbon simulation timestep length in years
    temp -- the average temperature in C
    rain -- the amount of rainfall
    amplitude -- the temperature variation amplitude within a year
    cwl_d -- coarse woody litter (cwl) diameter
    a_cwl -- initial stock of acid soluble carbon for cwl
    w_cwl -- initial stock of water soluble carbonmass for cwl
    e_cwl -- initial stock of ethanol soluble carbon for cwl
    n_cwl -- initial stock of non soluble carbon cwl
    h_cwl -- initial stock of humus carbon cwl
    a_cwl_in -- cwl infall of acid soluble carbon for the whole duration
    w_cwl_in -- cwl infall of water soluble carbon for the whole duration
    e_cwl_in -- cwl infall of ethanol soluble carbon for the whole duration
    n_cwl_in -- cwl infall of non soluble carbon for the whole duration
    fwl_d -- fine woody litter (fwl) diameter
    a_fwl -- initial stock of acid soluble carbon for fwl
    w_fwl -- initial stock of water soluble carbonmass for fwl
    e_fwl -- initial stock of ethanol soluble carbon for fwl
    n_fwl -- initial stock of non soluble carbon fwl
    h_fwl -- initial stock of humus carbon fwl
    a_fwl_in -- fwl infall of acid soluble carbon for the whole duration
    w_fwl_in -- fwl infall of water soluble carbon for the whole duration
    e_fwl_in -- fwl infall of ethanol soluble carbon for the whole duration
    n_fwl_in -- fwl infall of non soluble carbon for the whole duration
    a_nwl -- initial stock of acid soluble carbon for non woody litter
                   (nwl)
    w_nwl -- initial stock of water soluble carbonmass for nwl
    e_nwl -- initial stock of ethanol soluble carbon for nwl
    n_nwl -- initial stock of non soluble carbon nwl
    h_nwl -- initial stock of humus carbon nwl
    a_nwl_in -- nwlinfall of acid soluble carbon for the whole duration
    w_nwl_in -- nwl infall of water soluble carbon for the whole duration
    e_nwl_in -- nwl infall of ethanol soluble carbon for the whole duration
    n_nwl_in -- nwl infall of non soluble carbon for the whole duration
    """
    dur, temp, rain, amplitude, \
    cwl_d, a_cwl, w_cwl, e_cwl, n_cwl, h_cwl, \
    a_cwl_in, w_cwl_in, e_cwl_in, n_cwl_in, \
    fwl_d, a_fwl, w_fwl, e_fwl, n_fwl, h_fwl, \
    a_fwl_in, w_fwl_in, e_fwl_in, n_fwl_in, \
    a_nwl, w_nwl, e_nwl, n_nwl, h_nwl, \
    a_nwl_in, w_nwl_in, e_nwl_in, n_nwl_in = args.variables[:,index]
    na = numpy.array
    f32 = numpy.float32
    cl = na([temp, rain, amplitude], dtype=numpy.float32)
    litters = ('cwl', 'fwl', 'nwl')
    stocks = (na([a_cwl, w_cwl, e_cwl, n_cwl, h_cwl], dtype=f32),
              na([a_fwl, w_fwl, e_fwl, n_fwl, h_fwl], dtype=f32),
              na([a_nwl, w_nwl, e_nwl, n_nwl, h_nwl], dtype=f32))
    inputs = (([a_cwl_in, w_cwl_in, e_cwl_in, n_cwl_in, 0.], cwl_d),
              ([a_fwl_in, w_fwl_in, e_fwl_in, n_fwl_in, 0.], fwl_d),
              ([a_nwl_in, w_nwl_in, e_nwl_in, n_nwl_in, 0.], 0.))
    c_stock, c_flux = 0., 0.
    for ind in range(len(litters)):
        stock = stocks[ind]
        infall = na(inputs[ind][0], dtype=f32) / dur
        s_c = inputs[ind][1]
        endstate = y07.yasso.mod5c(ML_PARAM, dur, cl, stock, infall, s_c)
        if litters[ind] == 'cwl':
            a_cwl, w_cwl, e_cwl, n_cwl, h_cwl = endstate
        elif litters[ind] == 'fwl':
            a_fwl, w_fwl, e_fwl, n_fwl, h_fwl = endstate
        else:
            a_nwl, w_nwl, e_nwl, n_nwl, h_nwl = endstate
        c_stock += endstate.sum()
        c_flux +=  stock.sum() - endstate.sum()
    res = [c_stock, c_flux, a_cwl, w_cwl, e_cwl, n_cwl, h_cwl,
           a_fwl, w_fwl, e_fwl, n_fwl, h_fwl,
           a_nwl, w_nwl, e_nwl, n_nwl, h_nwl]
    args.mem[:, index] = res
    return 1
