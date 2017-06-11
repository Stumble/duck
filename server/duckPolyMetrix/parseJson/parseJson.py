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
methodCallingFuncAttr = 'calling-function'

attrLinesOfCode = 'linesOfCode'
attrNumOfMethods = 'numOfMethods'
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


def parse(resultJson, projectDir):
        #try:
  print "start parse"
  with open(resultJson) as data_file:
    data = json.load(data_file)
    classesList = []
    classesQueryDic = {}


    classesDic = data[classesAttr]
    print classesDic
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
                  parameterList = methodAttrDic[methodParaAttr]
                  for paraType in parameterList:
                          m.addParameters(paraType)
          if methodCallingFuncAttr in methodAttrDic:
                  callingList = methodAttrDic[methodCallingFuncAttr]
                  for callingfunc in callingList:
                          m.addCallingFunctionName(callingfunc)
          c.addMethod(m)

      if fieldsAttr in attrDic:
      	fieldsDic = attrDic[fieldsAttr]
      	print fieldsDic
      	for field in fieldsDic:
      		c.fieldDic[field] = fieldsDic[field]
      		c.attrDic[attrNumOfFields] += 1

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

    baseClasses = buildGraph.buildInhritedGraph(classesList, classesQueryDic)

    print "generate output json file"
    outputJson.outputFlareInheritedJson(baseClasses, attrLinesOfCode, projectDir+"/"+attrLinesOfCode+"_inherited_flare.json")
    outputJson.outputBundlingInheritedJson(classesList, attrLinesOfCode, projectDir+"/"+attrLinesOfCode+"_inherited_bundling.json")
    outputJson.outputBundlingFieldTypeJson(classesList, classesQueryDic, attrLinesOfCode, projectDir+"/"+attrLinesOfCode+"_feild_bundling.json")
    outputJson.outputMethodHirJson(classesList, attrLinesOfCode, projectDir+"/"+attrLinesOfCode+"_methodHirar_flare.json")
    outputCSV.outputInheritedCSV(baseClasses, attrLinesOfCode, projectDir+"/"+attrLinesOfCode+"_inherited_flare.csv")

    print baseClasses


        #except:
#		print "exception occurred"
#		raise