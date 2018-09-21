## this class overloads all of the operations of objects, and activates the call using the >> operator, 
## pushing the argument on the left to the first arg of the function
class fake_wrapper(object):
	def __init__(self, func, fake_object):
		self.func = func
		self.fake_object=fake_object
		self.stored_operations=[]
		self.stored_values=[]

	# these will be evaulated after function is finished
	def self_store_func(self, operation):
		self.stored_operations.append(operation)
		def store_val(rval):
			self.stored_values.append(rval)

		return store_val

	# the below are required, since >> is very low priority in order of operations
	def __mul__(self, rval):
		self.self_store_func('__mul__')(rval)
		return self

	def __add__(self, rval):
		self.self_store_func('__add__')(rval)
		return self

	def __sub__(self, rval):
		self.self_store_func('__sub__')(rval)
		return self

	def __div__(self, rval):
		self.self_store_func('__div__')(rval)
		return self

	def __truediv__(self, rval):
		self.self_store_func('__truediv__')(rval)
		return self

	def __floordiv__(self, rval):
		self.self_store_func('__floordiv__')(rval)
		return self

	def __pow__(self, rval):
		self.self_store_func('__pow__')(rval)
		return self

	def __xor__(self, rval):
		self.self_store_func('__xor__')(rval)
		return self

	def __mod__(self, rval):
		self.self_store_func('__mod__')(rval)
		return self

	def __and__(self, rval):
		self.self_store_func('__and__')(rval)
		return self

	def __or__(self, rval):
		self.self_store_func('__or__')(rval)
		return self

	def __lshift__(self, rval):
		self.self_store_func('__lshift__')(rval)
		return self

	# for nested objects
	def __getattr__(self, attr):
		return fake_wrapper(getattr(self.func, attr), self.fake_object)

	def __rrshift__(self, lval):
		first_val = self.func(*([lval]+list(self.fake_object.args)),**self.fake_object.kwargs)
		for operation, value in zip(self.stored_operations, self.stored_values):
			first_val = getattr(first_val, operation)(value)

		return first_val

	def __call__(self, *args, **kwargs):
		self.fake_object.args = args
		self.fake_object.kwargs=kwargs
		return self

## this accesses the globals environment and stores the args and kwargs of the calling function
## an object must be initially defined, but after that it has no other purpose
class fake(object):
	def __init__(self):
		self.args=None
		self.kwargs=None

	def __getattr__(self, attr):
		if attr in globals():
			return fake_wrapper(globals()[attr], self)
		else:
			return self.__getattribute__(attr)


# used to show how to access nested attributes
class example_class(object):
	@classmethod
	def test_func(cls, *args):
		print(sum(args))
		return(sum(args))

# example function
def myfunc(*args):
	print(args)


# this will be used to evaluate things
f = fake()

3 >> f.myfunc(3,4,5) 

x = 3 >> f.example_class.test_func(4,5,6) * 4 / 2 + 1 >> f.example_class.test_func(3,4)/9

print(x)