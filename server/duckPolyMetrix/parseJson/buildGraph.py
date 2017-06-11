
def buildInhritedGraph(classesList, classesQueryDic):
	for c in classesList:
		for inherited in c.inheritedList:
			if not inherited in classesQueryDic:
				print "inherited classes not found"
				continue
			c.addParentClass(classesQueryDic[inherited])
			classesQueryDic[inherited].addChildClass(c)
	rootList = []

	for c in classesList:
		if not c.inheritedList:
			print c.name+" doesn't has parent"
			rootList.append(c)

	return rootList