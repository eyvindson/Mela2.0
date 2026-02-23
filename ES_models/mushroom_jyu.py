
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Title: Models for mushrooms, JYU -- based off of Tahvanainen, Miina, Kurttila and Salo. 2016. Modelling the yields of marketed mushroom in Picea abies stands in eastern Finland. Forest Ecology and Management. 362:79-88.

*cep_jyu.py*

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

def Mushroom_jyu(arg, oind):
    """
		Calculates mushroom yield, ecosystem service, University of Jyvaskyla. With average (i.e. 50% production) 
    """
	
    #cepyield = 0
	
    ret = 1
    
	# Basal area
    BA = arg.variables[0, oind]
	# Age
    Age = arg.variables[1, oind]
		
    # Boletus
    Boletus = math.exp(-1.9819  + 0.1778 * BA + -0.0049 * (BA * BA) + 2.0907 * (BA / (Age + 5.)))
    
	# Lactarius
    Lactarius = math.exp(2.1243 - 0.0179 * BA + 1.7435 * (BA / (Age + 5.)))
	
	# ALL_MARKETED_MUSHROOMS
    ALL_MARKETED_MUSHROOMS = math.exp(2.5987 - 0.0118 * BA + 1.5012 * (BA / (Age + 5.)))
	
	# number of berries to kg/ha
    
	
    # result (cep yield) back to SIMO
    arg.num_of_res_objs[oind] = 1

    arg.mem[0, oind] = round(Boletus,4)
    arg.mem[1, oind] = round(Lactarius,4)
    arg.mem[2, oind] = round(ALL_MARKETED_MUSHROOMS,4)
	
	
    return ret