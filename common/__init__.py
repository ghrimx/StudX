# common/__init__.py

DEPARTURE = 0
ARRIVAL = 1
IN_OUT_TYPE = (
	(DEPARTURE, 'Departure'),
	(ARRIVAL, 'Arrival'),
	)	
	
def init_InOutType_dict(input_list):
	''' 
		Convert a list in a dictionary.
		The dictionany is initialized at startup and will be used for serving URL for arrival and departure.
	'''
	
	a = input_list # list containg lists of id and name arrival/departure 
	output_dict = {a[i][1]: a[i][0] for i in range(len(a))} # output dictionary e.g {'string1':int, 'string2':int}
	
	return output_dict

IN_OUT_TYPE_DICT = init_InOutType_dict(IN_OUT_TYPE)
