import json
import os
from util import remove_class_prefix
from sets import Set

def outputFlareInheritedJson(rootList, matrix, outputFile):
	f = open(outputFile, 'w')

	outerDic = {}
	outerDic['name'] = 'base'
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
			raise Exception("matrix doesn't exist")
		leafDic = {}
		leafDic['name'] = remove_class_prefix(nodeClass.name)
		leafDic['size'] = nodeClass.attrDic[matrix]
		return leafDic
	else:
		nonLeafDic = {}
		nonLeafDic['name'] = remove_class_prefix(nodeClass.name)
		nonLeafDic['children'] = []
		for childClass in nodeClass.childClasses:
			childDic = getFlareInheritedJsonRec(childClass, matrix)
			nonLeafDic['children'].append(childDic)
		return nonLeafDic

def outputFlareInheritedJsonBasedOnQuery(rootList, matrix, outputFile, query):
	f = open(outputFile, 'w')

	outerDic = {}
	outerDic['name'] = 'base'
	outerDic['children'] = []

	print 'start generate json file'
	for rootClass in rootList:
		rootDic, found = getFlareInheritedJsonRecBasedOnQuery(rootClass, matrix, query)
		if found:
			outerDic['children'].append(rootDic)

	result = json.dumps(outerDic, separators=(',',':'))

	print 'generate successfully'
	f.write(result)
	f.close()

def getFlareInheritedJsonRecBasedOnQuery(nodeClass, matrix, query):
	if not nodeClass.childClasses:
		if not matrix in nodeClass.attrDic:
			raise Exception("matrix doesn't exist")
		leafDic = {}
		leafDic['name'] = remove_class_prefix(nodeClass.name)
		leafDic['size'] = nodeClass.attrDic[matrix]
		isFound = query in leafDic['name']
		print leafDic
		return leafDic, isFound
	else:
		nonLeafDic = {}
		nonLeafDic['name'] = remove_class_prefix(nodeClass.name)
		nonLeafDic['children'] = []
		nonLeafFound = False
		for childClass in nodeClass.childClasses:
			childDic, found = getFlareInheritedJsonRecBasedOnQuery(childClass, matrix,query)
			nonLeafFound = found or nonLeafFound
			if found or query in nonLeafDic['name']:
				print childDic
				nonLeafDic['children'].append(childDic)

		return nonLeafDic, nonLeafFound or query in nonLeafDic['name']

def outputBundlingInheritedJson(classList, matrix, outputFile):
	f = open(outputFile, 'w')

	outerList = []

	print 'start generate bundling inherited json file'
	for classNode in classList:
		if not matrix in classNode.attrDic:
			raise Exception("matrix doesn't exist")
		classDic = {}
		classDic['name'] = remove_class_prefix(classNode.name)
		classDic['size'] = classNode.attrDic[matrix]
		classDic['imports'] = []
		for childClass in classNode.childClasses:
			classDic['imports'].append(remove_class_prefix(childClass.name))
		outerList.append(classDic)
	result = json.dumps(outerList, separators=(',',':'))

	print 'generate successfully'
	f.write(result)
	f.close()

def outputBundlingInheritedJsonBasedOnQuery(classList, matrix, outputFile, query):
	f = open(outputFile, 'w')

	outerList = []

	queryIncludeClass = Set()

	print 'start generate bundling inherited json file'
	for classNode in classList:
		if query in classNode.name:
			for childClass in classNode.childClasses:
				queryIncludeClass.add(childClass.name)

	for classNode in classList:
		if not matrix in classNode.attrDic:
			raise Exception("matrix doesn't exist")
		classDic = {}
		classDic['name'] = remove_class_prefix(classNode.name)
		classDic['size'] = classNode.attrDic[matrix]
		classDic['imports'] = []
		for childClass in classNode.childClasses:
			if query in classNode.name or query in childClass.name:
				classDic['imports'].append(remove_class_prefix(childClass.name))
		if query in classNode.name or classNode.name in queryIncludeClass:
			outerList.append(classDic)
	result = json.dumps(outerList, separators=(',',':'))

	print 'generate successfully'
	f.write(result)
	f.close()

def outputMethodHirJson(classList, matrix, outputFile):
	f = open(outputFile, 'w')

	outerList = {}


	outerList['name'] = 'base'
	outerList['children'] = []

	print 'start generate json file'
	for classNode in classList:
		classDic = {}
		classDic['name'] = remove_class_prefix(classNode.name)
		classDic['children'] = []
		for method in classNode.methods:
			methodDic = {}
			methodDic['name'] = remove_class_prefix(method.name)
			if not matrix in method.attrDic:
				raise Exception("matrix doesn't exist")
			methodDic['size'] = method.attrDic[matrix]
			classDic['children'].append(methodDic)
		outerList['children'].append(classDic)

	result = json.dumps(outerList, separators=(',',':'))

	print 'generate successfully'
	f.write(result)
	f.close()

def outputMethodHirJsonBasedOnQuery(classList, matrix, outputFile, query):
	f = open(outputFile, 'w')

	outerList = {}


	outerList['name'] = 'base'
	outerList['children'] = []

	print 'start generate json file'
	for classNode in classList:
		foundMethod = False
		classDic = {}
		classDic['name'] = remove_class_prefix(classNode.name)
		classDic['children'] = []
		for method in classNode.methods:
			methodDic = {}
			methodDic['name'] = remove_class_prefix(method.name)
			if not matrix in method.attrDic:
				raise Exception("matrix doesn't exist")
			methodDic['size'] = method.attrDic[matrix]
			if query in method.name:
				foundMethod = True
				classDic['children'].append(methodDic)

		if foundMethod or query in classNode.name:
			outerList['children'].append(classDic)

	result = json.dumps(outerList, separators=(',',':'))

	print 'generate successfully'
	f.write(result)
	f.close()

def outputBundlingFieldTypeJson(classList, classesQueryDic, matrix, outputFile):
	f = open(outputFile, 'w')

	outerList = []
	print 'start generate json file'
	for classNode in classList:
		if not matrix in classNode.attrDic:
			raise Exception("matrix doesn't exist")
		classDic = {}
		classDic['name'] = remove_class_prefix(classNode.name)
		classDic['size'] = classNode.attrDic[matrix]
		classDic['imports'] = []
		for field in classNode.fieldDic:
			if classNode.fieldDic[field] in classesQueryDic:
				classDic['imports'].append(remove_class_prefix(classNode.fieldDic[field]))
		for method in classNode.methods:
			for p in method.parameters:
				if p in classesQueryDic:
					classDic['imports'].append(remove_class_prefix(p))
			if method.returnType and method.returnType in classesQueryDic:
				classDic['imports'].append(remove_class_prefix(method.returnType))
		outerList.append(classDic)

	result = json.dumps(outerList, separators=(',',':'))

	print 'generate successfully'
	f.write(result)
	f.close()

def outputBundlingFieldTypeJsonBasedOnQuery(classList, classesQueryDic, matrix, outputFile, query):
	f = open(outputFile, 'w')

	queryIncludeClass = Set()

	print 'start generate bundling inherited json file'
	for classNode in classList:
		if query in classNode.name:
			for childClass in classNode.childClasses:
				queryIncludeClass.add(childClass.name)

	outerList = []
	print 'start generate json file'
	for classNode in classList:
		if not matrix in classNode.attrDic:
			raise Exception("matrix doesn't exist")
		classDic = {}
		classDic['name'] = remove_class_prefix(classNode.name)
		classDic['size'] = classNode.attrDic[matrix]
		classDic['imports'] = []
		for field in classNode.fieldDic:
			if classNode.fieldDic[field] in classesQueryDic:
				classDic['imports'].append(remove_class_prefix(classNode.fieldDic[field]))
		for method in classNode.methods:
			for p in method.parameters:
				if p in classesQueryDic:
					classDic['imports'].append(remove_class_prefix(p))
			if method.returnType and method.returnType in classesQueryDic:
				classDic['imports'].append(remove_class_prefix(method.returnType))
		if query in classNode.name:
			outerList.append(classDic)

	result = json.dumps(outerList, separators=(',',':'))

	print 'generate successfully'
	f.write(result)
	f.close()	