import json
import os

def outputFlareInheritedJson(rootList, matrix, outputFile):
	f = open(outputFile, 'w')

	outerDic = {}
	outerDic['name'] = 'flare'
	outerDic['children'] = []

	print 'start generate json file'
	for rootClass in rootList:
		rootDic = getFlareInheritedJsonRec(rootClass, matrix)
		outerDic['children'].append(rootDic)

	result = json.dumps(outerDic, separators=(',',':'))

	print 'generate successfully'
	f.write(result)
	f.close()



def getFlareInheritedJsonRec(nodeClass, matrix):
	if not nodeClass.childClasses:
		if not matrix in nodeClass.attrDic:
			print matrix, nodeClass.attrDic
			raise Exception("matrix doesn't exist")
		leafDic = {}
		leafDic['name'] = nodeClass.name
		leafDic['size'] = nodeClass.attrDic[matrix]
		return leafDic
	else:
		nonLeafDic = {}
		nonLeafDic['name'] = nodeClass.name
		nonLeafDic['children'] = []
		for childClass in nodeClass.childClasses:
			childDic = getFlareInheritedJsonRec(childClass, matrix)
			nonLeafDic['children'].append(childDic)
		return nonLeafDic
