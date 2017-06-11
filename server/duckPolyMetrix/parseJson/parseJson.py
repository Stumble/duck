import json
import os

from jsonClass import JClass
from jsonMethod import JMethod
import buildTree
import outputJson
import outputCSV

inHeritedListAttr = 'base_list'
classesAttr = 'classes'
methodsAttr = 'methods'

methodRunTimeAttr = 'run-time invokes'
methodLOCAttr = 'linesOfCode'
methodParaAttr = 'parameter'
methodCallingFuncAttr = 'calling-function'

attrLinesOfCode = 'linesOfCode'
attrNumOfMethods = 'numOfMethods'

def parse(resultJson, projectDir):
	#try:
		print "start parse"
		with open(resultJson) as data_file:    
			data = json.load(data_file)
			#{u'classes': {u'foo': {u'inherited list': [u'BaseA', u'BaseB'],
			#						u'methods': {u'addAandB': {u'run-time invokes': 10,
			#													u'linesOfCode': 38, 
			#													u'parameter': [u'Int',
			#																   u'Bool',
			#																   u'String'],
			#													u'calling-function': [u'Bar.subAandB', 
			#																		  u'Pc.test']}}}, 
			#			   u'bar': {u'inherited list': [], 
			#			   			u'methods': [{u'init': {u'run-time invokes': 0, 
			#			   									u'linesOfCode': 0, 
            #     											u'calling-function':[],
			#			   									u'parameter': []}}]}}}
			classesList = []
			classesQueryDic = {}


			classesDic = data[classesAttr]
			print classesDic
			for className in classesDic:
				attrDic = classesDic[className]
				c = JClass(className)

				c.attrDic[attrLinesOfCode] = 0
				c.attrDic[attrNumOfMethods] = 0

				if inHeritedListAttr in attrDic:
					for inheritedClass in attrDic[inHeritedListAttr]:
						c.addInheritedClass(inheritedClass)

				if methodsAttr in attrDic:
					methodsDic = attrDic[methodsAttr]
					for methodName in methodsDic:
						
						c.attrDic[attrNumOfMethods] += 1						
						methodAttrDic = methodsDic[methodName]
						m = JMethod(methodName, className)
						if methodRunTimeAttr in methodAttrDic:
							m.setRunTimeInvokes(methodAttrDic[methodRunTimeAttr])
						if methodLOCAttr in methodAttrDic:
							m.setLineOfCode(methodAttrDic[methodLOCAttr])
							c.attrDic[attrLinesOfCode] += methodAttrDic[methodLOCAttr]
						if methodParaAttr in methodAttrDic:
							parameterList = methodAttrDic[methodParaAttr]
							for paraType in parameterList:
								m.addParameters(paraType)
						if methodCallingFuncAttr in methodAttrDic:
							callingList = methodAttrDic[methodCallingFuncAttr]
							for callingfunc in callingList:
								m.addCallingFunctionName(callingfunc)
						c.addMethod(m)
				classesList.append(c)
				classesQueryDic[className] = c

			print classesList



#			for c in classesList:
#				for inherited in c.inheritedList:
#					if not inherited in classesQueryDic:
#						print "inherited classes not found"
#						raise Exception("inherited classes not found")
#					c.addParentClass(classesQueryDic[inherited])
#				for m in c.methods:
#					for callingfunc in m.callingFuncNameList:
#						print callingfunc
#						className, funcName = callingfunc.split('.')
#						if not className in classesQueryDic:
#							print "calling classes not found"
#							raise Exception("calling classes not found")
#						callingClass = classesQueryDic[className]
#						for classMethod in callingClass.methods:
#							if classMethod.name == funcName:
#								m.addCallingFunction(classMethod)

			baseClasses = buildTree.buildInhritedTree(classesList, classesQueryDic)

			outputJson.outputFlareInheritedJson(baseClasses, attrLinesOfCode, projectDir+"/LOCInherited.json")
			outputCSV.outputInheritedCSV(baseClasses, attrLinesOfCode, projectDir+"/LOCInherited.csv")

			print baseClasses


	#except:
#		print "exception occurred"
#		raise