
def buildInhritedGraph(classesList, classesQueryDic):
	rootList = []
	for c in classesList:
		for inherited in c.inheritedList:
			if not inherited in classesQueryDic:
				print "inherited classes not found"
			else:
				c.addParentClass(classesQueryDic[inherited])
				classesQueryDic[inherited].addChildClass(c)

	for c in classesList:
		if not c.parentClassList:
			print c.name+" doesn't has parent"
			rootList.append(c)

	return rootList