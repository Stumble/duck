import json
import os

from jsonClass import JClass
from jsonMethod import JMethod
import buildTree
import buildGraph
import outputJson
import outputCSV

inHeritedListAttr = 'base_list'
classesAttr = 'classes'
methodsAttr = 'methods'
fieldsAttr = 'fields'

methodRunTimeAttr = 'run-time invokes'
methodLOCAttr = 'linesOfCode'
methodParaAttr = 'parameter'
methodReturnAttr = 'return_type'
methodCallingFuncAttr = 'calling-function'

attrLinesOfCode = 'linesOfCode'
attrNumOfMethods = 'numOfMethod'
attrNumOfFields = 'numOfFields'

# example JSON file
# {
#   "classes": {
#     "class testMyOuter::testMyInner::Base": {
#       "fields": {
#         "x": "class int"
#       },
#       "methods": {},
#       "base_list": []
#     },
#     "class testMyOuter::testMyInner::Bar": {
#       "fields": {
#         "myDad": "class testMyOuter::testMyInner::Foo",
#         "hahah": "class testMyOuter::testMyInner::Foo",
#         "myDzz": "class testMyOuter::testMyInner::Foo"
#       },
#       "methods": {
#         "test(const class testMyOuter::testMyInner::Foo **const)": {
#           "linesOfCode": 8,
#           "parameter": {
#             "shit": "class testMyOuter::testMyInner::Foo"
#           },
#           "calling-function": [],
#           "run-time-invokes": 0
#         },
#         "test()": {
#           "linesOfCode": 7,
#           "parameter": {},
#           "calling-function": [],
#           "run-time-invokes": 0
#         }
#       },
#       "base_list": [
#         "class testMyOuter::testMyInner::Foo",
#         "class testMyOuter::testMyInner::Base"
#       ]
#     },
#     "class testMyOuter::testMyInner::Foo": {
#       "fields": {
#         "xx": "class int",
#         "id": "class int"
#       },
#       "methods": {
#         "print(std::string)": {
#           "linesOfCode": 5,
#           "parameter": {
#             "str": "class std::string"
#           },
#           "calling-function": [],
#           "run-time-invokes": 0
#         }
#       },
#       "base_list": []
#     }
#   }
# }

def outputResult(baseClasses, classesList, classesQueryDic, attribute, projectDir):
	print "output result:"
	print attribute
	count = 0
	#try:
	outputJson.outputFlareInheritedJson(baseClasses, attribute, projectDir+"/"+attribute+"_inherited_flare.json")
	count += 1
	outputJson.outputBundlingInheritedJson(classesList, attribute, projectDir+"/"+attribute+"_inherited_bundling.json")
	count += 1
	outputJson.outputBundlingFieldTypeJson(classesList, classesQueryDic, attribute, projectDir+"/"+attribute+"_methodHirar_bundling.json")
	count += 1
	outputJson.outputMethodHirJson(classesList, attribute, projectDir+"/"+attribute+"_methodHirar_flare.json")
	count += 1
	outputCSV.outputInheritedCSV(baseClasses, attribute, projectDir+"/"+attribute+"_inherited_flare.csv")
	#except:
	#	print "exception occurred " + str(count)



def parse(resultJson, projectDir):
        #try:
  print "start parse"
  with open(resultJson) as data_file:
    data = json.load(data_file)
    classesList = []
    classesQueryDic = {}


    classesDic = data[classesAttr]
    for className in classesDic:
      attrDic = classesDic[className]
      c = JClass(className)

      c.attrDic[attrLinesOfCode] = 0
      c.attrDic[attrNumOfMethods] = 0
      c.attrDic[attrNumOfFields] = 0

      if inHeritedListAttr in attrDic:
        for inheritedClass in attrDic[inHeritedListAttr]:
          c.addInheritedClass(inheritedClass)

      if methodsAttr in attrDic:
        methodsDic = attrDic[methodsAttr]
        for methodName in methodsDic:
          c.attrDic[attrNumOfMethods] += 1
          methodAttrDic = methodsDic[methodName]
          m = JMethod(methodName, className)
          m.attrDic[attrLinesOfCode] = 0
          if methodRunTimeAttr in methodAttrDic:
                  m.setRunTimeInvokes(methodAttrDic[methodRunTimeAttr])
          if methodLOCAttr in methodAttrDic:
                  m.setLineOfCode(methodAttrDic[methodLOCAttr])
                  m.attrDic[attrLinesOfCode] = methodAttrDic[methodLOCAttr]
                  c.attrDic[attrLinesOfCode] += methodAttrDic[methodLOCAttr]
          if methodParaAttr in methodAttrDic:
            parameterDic = methodAttrDic[methodParaAttr]
            if isinstance(parameterDic, dict):
              for paraName in parameterDic:
                m.addParameters(parameterDic[paraName])
          if methodReturnAttr in methodAttrDic:
								m.returnType = methodAttrDic[methodReturnAttr]
          if methodCallingFuncAttr in methodAttrDic:
                  callingList = methodAttrDic[methodCallingFuncAttr]
                  for callingfunc in callingList:
                          m.addCallingFunctionName(callingfunc)
          c.addMethod(m)

      if fieldsAttr in attrDic:
      	fieldsDic = attrDic[fieldsAttr]
      	for field in fieldsDic:
      		c.fieldDic[field] = fieldsDic[field]
      		c.attrDic[attrNumOfFields] += 1

      classesList.append(c)
      classesQueryDic[className] = c




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

    baseClasses = buildGraph.buildInhritedGraph(classesList, classesQueryDic)

    print "generate output json file"

    outputResult(baseClasses, classesList, classesQueryDic, attrLinesOfCode, projectDir)
    outputResult(baseClasses, classesList, classesQueryDic, attrNumOfMethods, projectDir)
    outputResult(baseClasses, classesList, classesQueryDic, attrNumOfFields, projectDir)


        #except:
#		print "exception occurred"
#		raise