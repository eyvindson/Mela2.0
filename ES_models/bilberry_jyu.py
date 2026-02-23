
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Title: Models for bilberry, JYU.

*bilberry_jyu.py*

Each model definition must be of the form:
    def model_name(arg, oind)
in which
    arg - contains all the data being passed between the simulator
          and the prediction model
    oind - is the index number for the object for which the prediction is
           being made

The arg data object has the following structure:
    arg.variables[variable_index, object_index]
        - the values of the explaining variables of the model. 
          The number and order of these must match with the variable 
          declarations in the variables section of the model definition in
          the model xml file
    arg.parameters[parameter_index]
        - the model parameter values. The order in which these are used must 
          match the order given in the parameters section of the model xml
          file
    arg.num_of_res_objs[object_index]
      - number of result objects. This is always 1 unless the prediction
        model really creates new objects; e.g. in stem distribution models
        each diameter or height class is a new object
    arg.mem[variable_index, result_index]
      - stores the model results. Again the results must be stored here
        in the same order as defined in the result/variables section of
        the model xml file
    arg.errors[object_index] 
        - for storing possible error messages. Before actually 
          evaluating the model, you should test for error situations and
          set error messages detailing why the model can't be evalueated and
          then exit
When getting or setting the attribute values of arg, oind is always used for
the object_index; e.g. the value of the first explaining variable of the 
model is accessed by arg.variables[0][oind]. As can be seen from the example
indices always start from 0.

The model must return an integer as its return value. 1 if there were no
errors and 0 if errors occurred.
"""

import math

def Bilberry_jyu(arg, oind):
    """
		Calculates bilberry yield, ecosystem service, University of Jyvaskyla.  
    """
	# altitude
    # ALT = 135.
	
    bilberry = 0
    ret = 1
	        
	# site
    SC = arg.variables[0, oind]
	# main species
    MAIN_SP = arg.variables[1, oind]
	# temperature sum
    TS = arg.variables[2, oind]
	# basal area
    BA = arg.variables[3, oind]
	# Age
    Age = arg.variables[4, oind]
	# proportion of Scots pine
    BA_propSp = arg.variables[5, oind] / 100.
	# proportion of Norway spruce
    BA_propNs = arg.variables[6, oind] / 100.
	# proportion of birch
    BA_propb = arg.variables[7, oind] / 100.
	#  basal area of other deciduous species
    BA_od = arg.variables[8, oind]
	#  altitude
    ALT = arg.variables[9, oind]
    #if BA > 100:
    #    import pdb;pdb.set_trace()
    # proportion of deciduous
    BA_propdec = (BA_od / BA) + BA_propb 
	
    # check if mixed species stand
    mixed = 0
    if (BA_propSp < 0.80 and BA_propNs < 0.80 and BA_propdec < 0.80):
		mixed = 1
	
    # BILBERRY
    # if pine or deciduous main species or mixed
    if (MAIN_SP in [1,3,4,5,6,7,8,9] or mixed == 1):
	
        # model parameters for coverage
        a0 = -3.8470
        a1 = -2.1815
        a2 = -0.4809
        a3 = -0.4807
        a4 = -1.5053
        a5 = 0.1209
        a6 = -0.4770
        a7= -0.2588
        a8 = 0 #-1.4715
        a9 = 0.0029
        a10 = 0.0080
        a11 = -0.0021
        a12 = 0.0947
        a13 = -0.1916
        # model parameters for yield
        a14 = -0.6781
        a15 = 0.1422
        a16 = 0.2398
        a17 = -0.2812
        a18 = 0
        a19 = 0
		
        if MAIN_SP == 1:
            a6 = 0
        elif (MAIN_SP != 1 and SC == 2):
            a5 = 0;
	
        #site OMT
        if SC == 2: 
            a1 = a3 = a4 = 0
        #site MT
        elif SC == 3: 
            a1 = a2 = a3 = a4 = 0
        #site VT
        elif SC == 4: 
            a1 = a2 = a4 = 0
		#site CT
        elif SC == 5: 
            a1 = a2 = a3 = 0
        #site OMaT
        else: 
            a2 = a3 = a4 = 0
        try:
            bilberrypinebirchcov = 100. * (1 / (1 + math.exp(-(a0 + a1 + a2 + a3 +a4 + a5 + a6 + a7 + a8 +a9 * ALT + a10 * Age + a11 * (Age * Age / 100.) + a12 * BA + a13 * (BA * BA / 100.)))))
        except OverflowError:
            import pdb;pdb.set_trace();
        bilberrypinebirchyield = math.exp(a14 + a15 + a16 * bilberrypinebirchcov + a17 * ((bilberrypinebirchcov * bilberrypinebirchcov) / 100.))
        # number of berries to kg/ha
        bilberrypinebirchyield = bilberrypinebirchyield * 0.8 * 10000. * 0.35 / 1000.
		
    # if spruce main species or mixed	
    if (MAIN_SP in [2] or mixed == 1):
	
        #model parameters for coverage
        a0 = -3.8470 
        a1 = -2.1815
        a2 = -0.4809
        a3 = -0.4807
        a4 = -1.5053
        a5 = 0
        a6 = 0
        a7= -0.2588
        a8 = 0 #-1.4715
        a9 = 0.0029
        a10 = 0.0080
        a11 = -0.0021
        a12 = 0.0947
        a13 = -0.1916
        #model parameters for yield
        a14 = -4.7474
        a15 = 0.5450
        a16 = 0.3635
        a17 = -0.4798
        a18 = 0.3742
        a19 = -1.3447
	
        #site OMT
        if SC == 2: 
            a1 = a3 = a4 = 0
        #site MT
        elif SC == 3: 
            a1 = a2 = a3 = a4 = 0
        #site VT
        elif SC == 4: 
            a1 = a2 = a4 = 0
        #site CT
        elif SC == 5: 
            a1 = a2 = a3 = 0
        #site OMaT
        else: 
            a2 = a3 = a4 = 0
		
        bilberrysprucecov = 100. * (1 / (1 + math.exp(-(a0 + a1 + a2 + a3 +a4 + a5 + a6 + a7 + a8 +a9 * ALT + a10 * Age + a11 * (Age * Age / 100.) + a12 * BA + a13 * (BA * BA / 100.)))))
        bilberryspruceyield= math.exp(a14 + a15 + a16 * bilberrysprucecov + a17 * (bilberrysprucecov * bilberrysprucecov / 100.) + a18 * BA + a19 * (BA * BA / 100.))
        # number of berries to kg/ha
        bilberryspruceyield = bilberryspruceyield * 0.8 * 10000. * 0.35 / 1000.
	
    if (MAIN_SP in [1,3,4,5,6,7,8,9] and mixed == 0):
		bilberry = bilberrypinebirchyield 
    elif (MAIN_SP == 2 and mixed == 0):
		bilberry = bilberryspruceyield 
    elif mixed == 1:
		bilberry = bilberrypinebirchyield * BA_propSp + bilberrypinebirchyield * BA_propdec + bilberryspruceyield * BA_propNs		
    	
    # result (bilberry yield) back to SIMO
    arg.num_of_res_objs[oind] = 1
    
    arg.mem[0, oind] = round(bilberry,4)
    
    return ret