
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Title: Capercaillie HSI model JYU.

*capercaillie_jyu.py*

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

def Capercaillie_jyu(arg, oind):
    """
		Calculates habitat suitability index for capercaillie, University of Jyvaskyla.
    """
    	
    ret = 1
	
	# pine volume
    V_pine = arg.variables[0, oind]
	# spruce volume
    V_spruce = arg.variables[1, oind]
	# number of trees
    N = arg.variables[2, oind]
	
    # capercaillie
    wpinecap = 0.05 * V_pine - 3.
    if V_pine <= 60.:
		wpinecap = 0
    elif V_pine > 80.:
		wpinecap = 1.
	
    wsprucecap = 0.2 * V_spruce - 1
    if V_spruce <= 5.:
		wsprucecap = 0
    elif (V_spruce > 10. and V_spruce <= 20.):
		wsprucecap = 1.
    elif (V_spruce > 20. and V_spruce <= 30.):
		wsprucecap = -0.1 * V_spruce + 3.
    elif V_spruce > 30.:
		wsprucecap = 0
		
    wdensitycap = 0.01 * N - 5.
    if N <= 500.:
		wdensitycap = 0
    elif (N > 600. and N <= 800.):
		wdensitycap = 1.
    elif (N > 800. and N <= 1000.):
		wdensitycap = -0.005 * N + 5.
    elif N > 1000.:
		wdensitycap = 0
		
    result = wpinecap * wsprucecap * wdensitycap
	
    # result (diameter growth of tree) back to SIMO
    arg.num_of_res_objs[oind] = 1
	
    arg.mem[0, oind] = round(result,2)
	
    return ret
