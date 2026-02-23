
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Title: Hazel grouse HSI model JYU.

*hazel_grouse_jyu.py*

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

def Hazel_grouse_jyu(arg, oind):
    """
		Calculates habitat suitability index for hazel grouse, University of Jyvaskyla.
    """
   	
    ret = 1
	
	# total volume
    V = arg.variables[0, oind]
	# spruce volume
    V_spruce = arg.variables[1, oind]
	# pendula birch volume
    V_penbirch = arg.variables[2, oind]
	# pubescens birch volume
    V_pubbirch = arg.variables[3, oind]
	# aspen volume
    V_aspen = arg.variables[4, oind]
	# deciduous volume
    V_aspen = arg.variables[5, oind]

	# age
    Age = arg.variables[6, oind]
		
    # volume of deciduous trees     
    voldec = V_penbirch + V_pubbirch + V_aspen
    
    propdec = probspr = 0
    if V > 0:
		# share of deciduous trees of total volume, %
        propdec = (voldec / V) * 100.
        # share of spruce trees of total volume, %
        probspr = (V_spruce / V) * 100.
	
    # hazel grouse
    wagehaz = 0.1 * Age - 2.
    if Age <= 20.:
		wagehaz = 0
    elif (Age > 30. and Age <= 60.):
		wagehaz = 1
    elif Age > 60.:
		wagehaz = -0.012 * Age + 1.72
	
    wdechaz = 0.066 * propdec - 0.33
    if propdec <= 5.:
		wdechaz = 0
    elif (propdec > 20. and propdec <= 40.):
		wdechaz = 1
    elif (propdec > 40. and propdec <= 60.):
		wdechaz = -0.05 * propdec + 3
    elif propdec > 60.:
		wdechaz = 0
		
    wsprucehaz = 0.2 * probspr - 4.
    if probspr <= 20.:
		wsprucehaz = 0
    elif probspr > 25.:
		wsprucehaz = 1.
			
    result = wagehaz * wdechaz * wsprucehaz
    if result < 0:
        result = 0
	
    # result (diameter growth of tree) back to SIMO
    arg.num_of_res_objs[oind] = 1
		
    arg.mem[0, oind] = round(result,2)
	
    return ret
