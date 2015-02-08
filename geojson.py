import json
import numpy
import scipy.stats

def loadJson(filename=""):
	json_data = open('geojson/AsthmaRates_CB00.json'+filename)
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

	for each in blockMap:
		dataDict = {}
		jsonDict = {}
		keys = each.keys()
		format = None
		for key in keys:
			if key != 'BLOCKGROUP':
				format = key
				jsonDict[each['BLOCKGROUP']] = [scipy.stats.percentileofscore(values,each[key])/100.0]
		dataDict['format'] = [format]
		dataDict['data'] = jsonDict
		jsonArray.append(dataDict)
	with open('data.json', 'w') as outfile:
		json.dump(jsonArray, outfile)


