

class JMethod(object):
	"""docstring for JMethod"""
	def __init__(self, methodName, className):
		super(JMethod, self).__init__()
		self.belongTo = className
		self.name = methodName
		self.parameters = []
		self.callingFuncNameList = []
		self.callingFunctions = []
		self.lineOfCode = 0
		self.runTimeInvokes = 0

	def addParameters(self, paraType):
		self.parameters.append(paraType)

	def addCallingFunction(self, m):
		self.callingFunctions.append(m)

	def addCallingFunctionName(self, methodName):
		self.callingFuncNameList.append(methodName)

	def setLineOfCode(self, lineofcode):
		self.lineOfCode = lineofcode

	def setRunTimeInvokes(self, runtimeinvokes):
		self.runTimeInvokes = runtimeinvokes
		