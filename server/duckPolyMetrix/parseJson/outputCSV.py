import collections
import classRank
from util import remove_class_prefix

def outputInheritedCSV(rootList, matrix, outputFile):
	f = open(outputFile, 'w')

	strList = []

	print 'start generate json file'
	for rootClass in rootList:
		rootList, cumulative = getFlareInheritedCSVRec(rootClass, matrix)
		for strLine in rootList:
			strList.append(strLine)

	print 'generate successfully'
	result = ""
	for s in strList:
		f.write(s+'\n')
	f.close()



def getFlareInheritedCSVRec(nodeClass, matrix):
	if not nodeClass.childClasses:
		if not matrix in nodeClass.attrDic:
			raise Exception("matrix doesn't exist")
		return [nodeClass.name+","+str(nodeClass.attrDic[matrix])], nodeClass.attrDic[matrix]
	else:
		strList = []
		cumulative = 0
		for childClass in nodeClass.childClasses:
			childStrList, total = getFlareInheritedCSVRec(childClass, matrix)
			for strLine in childStrList:
				strList.append(nodeClass.name+"-"+strLine)
			cumulative += total
		strList.append(nodeClass.name+"-end,"+str(cumulative))
		return strList, cumulative

def outputPageRankCSV(classList, classesQueryDic, outputFile):
	f = open(outputFile, 'w')

	statisticDic = {}
	classrank = classRank.CalcPageRank()
	print 'start generate page range file'
	for classNode in classList:
		classrank.add_node(classNode.name)
		statisticDic[classNode.name] = collections.defaultdict(int)
		for field in classNode.fieldDic:
			if classNode.fieldDic[field] in classesQueryDic:
				statisticDic[classNode.name][classNode.fieldDic[field]]+=1
		for method in classNode.methods:
			for p in method.parameters:
				if p in classesQueryDic:
					statisticDic[classNode.name][p]+=1
			if method.returnType and method.returnType in classesQueryDic:
					statisticDic[classNode.name][method.returnType]+=1

	for outNode in statisticDic:
		for inNode in statisticDic[outNode]:
			classrank.add_directed_edge(outNode, inNode, statisticDic[outNode][inNode]/3)
	result = classrank.get_value()
	f.write("id,value\n")
	for className in result:
		r = remove_class_prefix(className)+","+str(result[className])
		f.write(r+'\n')

	print 'generate successfully'
	f.close()