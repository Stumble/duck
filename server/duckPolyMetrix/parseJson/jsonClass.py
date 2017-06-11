

class JClass(object):
	"""docstring for JClass"""
	def __init__(self, className):
		super(JClass, self).__init__()
		self.name = className
		self.inheritedList = []
		self.parentClassList = []
		self.methods = []
		self.childClasses = []
		self.attrDic = {}
		self.fieldDic = {}

	def addInheritedClass(self, inheritedClassName):
		self.inheritedList.append(inheritedClassName)

	def addParentClass(self, parentClass):
		self.parentClassList.append(parentClass)

	def addMethod(self, method):
		self.methods.append(method)

	def addChildClass(self, childClass):
		self.childClasses.append(childClass)

	def addAttr(self, attrKey, attrValue):
		self.attrDic[attrKey] = attrValue

	def addField(fieldName, fieldType):
		self.fieldDic[fieldName] = fieldType
		