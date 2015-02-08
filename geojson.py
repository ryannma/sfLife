import json
import numpy
import scipy.stats

def loadJson(filename):
	json_data = open('static/data/'+filename)
	data = json.load(json_data)
	json_data.close()
	return data

def json2blocks(data):
	features = data['features']
	blockMap = []
	for each in features:
		blockMap.append(each['properties'])

	jsonArray = []
	values = []
	for each in blockMap:
		dataDict = {}
		jsonDict = {}
		keys = each.keys()
		format = None
		for key in keys:
			if key != 'BLOCKGROUP':
				values.append(each[key])

	jsonDict = {}
	format = None
	returnDict = {}
	for each in blockMap:
		keys = each.keys()
		for key in keys:
			format = key
			if key != 'BLOCKGROUP':
				jsonDict[each['BLOCKGROUP']] = [scipy.stats.percentileofscore(values,each[key])/100.0]
	returnDict['data'] = jsonDict
	returnDict['format'] = [format]
	with open('static/data/SF.json', 'w') as outfile:
		json.dump(returnDict, outfile)


