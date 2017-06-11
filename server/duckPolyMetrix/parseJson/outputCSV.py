
def outputInheritedCSV(rootList, matrix, outputFile):
	f = open(outputFile, 'w')

	strList = []

	print 'start generate json file'
	for rootClass in rootList:
		rootList, cumulative = getFlareInheritedCSVRec(rootClass, matrix)
		print rootList
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
			print matrix, nodeClass.attrDic
			raise Exception("matrix doesn't exist")
		return [nodeClass.name+","+str(nodeClass.attrDic[matrix])], nodeClass.attrDic[matrix]
	else:
		strList = []
		cumulative = 0
		for childClass in nodeClass.childClasses:
			childStrList, total = getFlareInheritedCSVRec(childClass, matrix)
			print childStrList
			for strLine in childStrList:
				strList.append(nodeClass.name+"-"+strLine)
			cumulative += total
		strList.append(nodeClass.name+"-end,"+str(cumulative))
		return strList, cumulative