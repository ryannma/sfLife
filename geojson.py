import json
import scipy.stats
from math import sin, cos, sqrt, atan2, radians


def loadJson(filename):
	json_data = open('static/data/'+filename)
	data = json.load(json_data)
	json_data.close()
	return data

def firstBlockJson(data):
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

def SFRentAffordability():
	data = loadJson('SanFranciscoRentAffordability.json')
	features = data['features']
	featureMap = []
	values = []
	for each in features:
		featureDict = {}
		if each['geometry']['type'] == 'Polygon':
			featureDict['polygon'] = each['geometry']['coordinates'][0]
			income = each['properties']['MedInc_d']
			if income == None:
				featureDict['income'] = float("60000")
			else:
				featureDict['income'] = float(income.replace(',',''))
			values.append(income)
			featureMap.append(featureDict)
		else:
			polygons = each['geometry']['coordinates'][0]
			for polygon in polygons:
				featureDict['polygon'] = polygon
				income = each['properties']['MedInc_d']
				if income == None:
					featureDict['income'] = float("60000")
				else:
					featureDict['income'] = float(income.replace(',',''))
				values.append(income)
				featureMap.append(featureDict)
			values.append(income)

	for each in featureMap:
		income = each['income']
		each['income'] = 1-scipy.stats.percentileofscore(values,income)/100.0
	jsonData = parseBlocks(loadJson('AsthmaRates_CB00.json'))

	for block in jsonData:
		coord = block['center']
		for each in featureMap:
			if point_in_poly(coord[0], coord[1], each['polygon'])=="IN":
				# print "In!"
				block['income'] = each['income']
	return jsonData

def AirQuality():
	data = loadJson('AirQuality_CB00.json')
	features = data['features']
	featureMap = {}
	valueArray = []
	for each in features:
		properties = each['properties']
		featureMap[properties['BLOCKGROUP']] = properties['MAXPM25']
		valueArray.append(properties['MAXPM25'])

	for key in featureMap:
		value = featureMap[key]
		featureMap[key] = scipy.stats.percentileofscore(valueArray,value)/100.0

	return featureMap

def PopulationDensity():
	data = loadJson('PopulationDensity_CB00.json')
	features = data['features']
	featureMap = {}
	valueArray = []
	for each in features:
		properties = each['properties']
		featureMap[properties['BLOCKGROUP']] = properties['Pop_psmi']
		valueArray.append(properties['Pop_psmi'])

	for key in featureMap:
		value = featureMap[key]
		featureMap[key] = 1-scipy.stats.percentileofscore(valueArray,value)/100.0

	return featureMap

def Poverty():
	data = loadJson('Poverty_CB00.json')
	features = data['features']
	featureMap = {}
	valueArray = []
	for each in features:
		properties = each['properties']
		featureMap[properties['BLOCKGROUP']] = properties['Pover_pct']
		valueArray.append(properties['Pover_pct'])

	for key in featureMap:
		value = featureMap[key]
		featureMap[key] = 1-scipy.stats.percentileofscore(valueArray,value)/100.0

	return featureMap

def point_in_poly(x,y,poly):

   # check if point is a vertex
   if (x,y) in poly: return "IN"

   # check if point is on a boundary
   for i in range(len(poly)):
      p1 = None
      p2 = None
      if i==0:
         p1 = poly[0]
         p2 = poly[1]
      else:
         p1 = poly[i-1]
         p2 = poly[i]
      if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
         return "IN"
      
   n = len(poly)
   inside = False
   p1x,p1y = poly[0]
   for i in range(n+1):
      p2x,p2y = poly[i % n]
      if y > min(p1y,p2y):
         if y <= max(p1y,p2y):
            if x <= max(p1x,p2x):
               if p1y != p2y:
                  xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
               if p1x == p2x or x <= xints:
                  inside = not inside
      p1x,p1y = p2x,p2y

   if inside: return "IN"
   else: return "OUT"

def parseBlocks(json):
	features = json['features']
	blocksArray = []
	for each in features:
		blocksDict = {}
		blocksDict['blockid'] = each['properties']['BLOCKGROUP']
		blocksDict['center'] = polygonCentroid(each['geometry']['coordinates'][0])
		blocksArray.append(blocksDict)
	return blocksArray

def addData2():
	currJson = loadJson('SF.json')	
	poverty = Poverty()
	popDensity = PopulationDensity()
	airQuality = AirQuality()
	affordability = SFRentAffordability()
	affordabilityMap = {}
	for block in affordability:
		if 'income' in block.keys():
			affordabilityMap[block['blockid']] = block['income']
		# Couple block ids are missing income for some odd reason
		else:
			affordabilityMap[block['blockid']] = 0.5
	blockData = currJson['data']
	for key in blockData:
		blockData[key].append(poverty[key])
		blockData[key].append(popDensity[key])
		blockData[key].append(airQuality[key])
		blockData[key].append(affordabilityMap[key])
	currJson['format'].append('POVERTY')
	currJson['format'].append('POPDENSITY')
	currJson['format'].append('AIRQUALITY')
	currJson['format'].append('AFFORDABILITY')
	with open('static/data/SF.json', 'w') as outfile:
		json.dump(currJson, outfile)

def addMinLocations():
	facilities = SFHealthFacilities()
	gardens = SFGardens()
	markets = SFFarmersMarkets()
	currJson = loadJson('SF.json')	
	facilityMap = {}
	for block in facilities:
		facilityMap[block['blockid']] = block['closest']
	gardenMap = {}
	for block in gardens:
		gardenMap[block['blockid']] = block['closest']
	marketMap = {}
	for block in markets:
		marketMap[block['blockid']] = block['closest']
	blockData = currJson['data']
	for key in blockData:
		blockData[key].append(facilityMap[key])
		blockData[key].append(gardenMap[key])
		blockData[key].append(marketMap[key])
	currJson['format'].append('HEALTHFACILITY')
	currJson['format'].append('GARDEN')
	currJson['format'].append('FARMERSMARKET')
	with open('static/data/SF.json', 'w') as outfile:
		json.dump(currJson, outfile)

def SFHealthFacilities():
	jsonData = parseBlocks(loadJson('AsthmaRates_CB00.json'))
	healthFacilities = loadJson('SanFranciscoHealthFacilities.json')
	features = healthFacilities['features']
	healthCoords = []
	for each in features:
		healthCoords.append(each['geometry']['coordinates'])

	for block in jsonData:
		distanceArray = []
		coord = block['center']
		for each in healthCoords:
			distanceArray.append(distanceBetweenPoints(coord, each))
		block['closestHospital'] = min(distanceArray)

	distanceArray = []
	for block in jsonData:
		distanceArray.append(block['closestHospital'])

	for block in jsonData:
		block['closest'] = scipy.stats.percentileofscore(distanceArray,block['closestHospital'])/100.0

	return jsonData

def SFGardens():
	jsonData = parseBlocks(loadJson('AsthmaRates_CB00.json'))
	gardens = loadJson('SanFranciscoCommunityGardens.json')
	features = gardens['features']
	gardenCoords = []
	for each in features:
		gardenCoords.append(each['geometry']['coordinates'])

	for block in jsonData:
		distanceArray = []
		coord = block['center']
		for each in gardenCoords:
			distanceArray.append(distanceBetweenPoints(coord, each))
		block['closestGarden'] = min(distanceArray)

	distanceArray = []
	for block in jsonData:
		distanceArray.append(block['closestGarden'])

	for block in jsonData:
		block['closest'] = scipy.stats.percentileofscore(distanceArray,block['closestGarden'])/100.0

	return jsonData

def SFFarmersMarkets():
	jsonData = parseBlocks(loadJson('AsthmaRates_CB00.json'))
	markets = loadJson('SanFranciscoFarmersMarkets.json')
	features = markets['features']
	marketCoords = []
	for each in features:
		marketCoords.append(each['geometry']['coordinates'])

	for block in jsonData:
		distanceArray = []
		coord = block['center']
		for each in marketCoords:
			distanceArray.append(distanceBetweenPoints(coord, each))
		block['closestMarket'] = min(distanceArray)

	distanceArray = []
	for block in jsonData:
		distanceArray.append(block['closestMarket'])

	for block in jsonData:
		block['closest'] = scipy.stats.percentileofscore(distanceArray,block['closestMarket'])/100.0


	return jsonData

def distanceBetweenPoints(point1, point2):
	R = 6373.0

	lat1 = radians(point1[0])
	lon1 = radians(point1[1])
	lat2 = radians(point2[0])
	lon2 = radians(point2[1])

	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	distance = R * c
	return distance*1000

def polygonCentroid(coordinates):
	xArray = []
	yArray = []
	for each in coordinates:
		xArray.append(each[0])
		yArray.append(each[1])

	areaInnerTotal = 0
	xInnerTotal = 0
	yInnerTotal = 0
	length = len(xArray)
	for i in range(0,length-1):
		areaInnerTotal += xArray[i]*yArray[i+1]-xArray[i+1]*yArray[i]
		latterHalf = (xArray[i]*yArray[i+1] - xArray[i+1]*yArray[i])
		xInnerTotal += (xArray[i]+xArray[i+1])*latterHalf
		yInnerTotal += (yArray[i]+yArray[i+1])*latterHalf
	area = areaInnerTotal/2
	centerX = (1.0/(6.0*area))*xInnerTotal
	centerY = (1.0/(6.0*area))*yInnerTotal
	return [centerX, centerY]



