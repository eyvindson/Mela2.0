
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Title: Models for cowberry, JYU.

*cowberry_jyu.py*

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

def Cowberry_jyu(arg, oind):
    """
		Calculates cowberry yield, ecosystem service, University of Jyvaskyla.  
    """
	
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
	#  altitude
    ALT = arg.variables[5, oind]
    
	# altitude
    # ALT = 135.
	# temperature sum
    # TS = 1100.
	
    # COWBERRY	
    # model parameters for coverage
    a0 = -4.7902            
    a1 = -5.1730
    a2 = -2.5690
    a3 = -0.4216
    a4 = -0.4185
    a5 = -0.4327
    a6 = -0.7528
    a7= 0 #-0.9438
    a8 = 2.5592
    a9 = -0.0039
    a10 = 0.0106
    a11 = 0.0157
    # model parameters for yield
    a12 = 6.5404
    a13 = 0.1849    
    a14 = 0.0966
    a15 = -0.0837
    a16 = -0.4716
    a17 =  0.0071  
    a18 = -4.6264
	
    if (MAIN_SP in [2] and SC in [1,2,3]):
		a6 = 0    
    elif (MAIN_SP in [3,4,5,6,8] and SC in [1,2,3]):
		a5 = 0
    else:
		a5 = a6 = 0

    #site OMT
    if SC == 2: 
		a1 = a3 = a4 = 0
    #site VT
    elif SC == 4: 
		a1 = a2 = a3 = a4 = 0
    #site MT
    elif SC == 3: 
		a1 = a2 = a4 = 0
    #site CT
    elif SC == 5: 
		a1 = a2 = a3 = 0
    #site OMaT
    else: 
		a2 = a3 = a4 = 0
	
    if SC not in [1,2]: 
		a10 = 0
	
    cowberrycov = 100. * (1. / (1. + math.exp(-(a0 + a1 + a2 + a3 + a4 + a5 + a6 + a7 + a8 * (1000. / TS) + a9 * ALT + a10 * Age + a11 * BA))))
    cowberryyield = math.exp(a12 + a13 + a14 * cowberrycov + a15 * (math.pow(cowberrycov,2) / 100.) + a16 * (math.log(BA + 1)) + a17 * ALT + (a18 * (1000. / TS))) 
	# number of berries to kg/ha
    cowberryyield = cowberryyield * 10000. * 0.23 / 1000.
	
    # result (cowberry yield) back to SIMO
    arg.num_of_res_objs[oind] = 1
    	
    arg.mem[0, oind] = cowberryyield
	
    return ret