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

def outputBundlingInheritedJson(classList, matrix, outputFile):
	f = open(outputFile, 'w')

	outerList = []


	print 'start generate json file'
	for classNode in classList:
		if not matrix in classNode.attrDic:
			print matrix, classNode.attrDic
			raise Exception("matrix doesn't exist")
		classDic = {}
		classDic['name'] = classNode.name
		classDic['size'] = classNode.attrDic[matrix]
		classDic['imports'] = []
		for childClass in classNode.childClasses:
			classDic['imports'].append(childClass.name)
		outerList.append(classDic)

	result = json.dumps(outerList, separators=(',',':'))

	print 'generate successfully'
	f.write(result)
	f.close()
