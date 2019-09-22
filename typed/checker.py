from toolz import curry
import numpy as np

class Type:
    pass

def incorrect_type(expected_type, real_type, real_value):
    raise TypeError('{} of type {} does not conform to {}'.format())

class Numpy(Type):
    @curry
    def __init__(self, dtype=None, shape=None):
        self.shape = shape
        self.dtype = dtype
    def check(self, value):
        if not isinstance(value, np.ndarray):
            raise Exception('{} is not numpy array'.format(value.__repr__()))
        if self.shape:
            if not self.shape == value.shape:
                raise TypeError('Shape {} does not conform to expected type {}'.format(value.shape, self.shape))
        if self.dtype:
            if not self.dtype == value.dtype:
                raise TypeError('Type {} does not conform to expected type {}'.format(value.dtype, self.dtype))
    def __getitem__(self, shape):
        if not isinstance(shape, tuple):
            return Numpy(self.dtype, (shape, ))
        return Numpy(self.dtype, shape)
    def __call__(self, dtype):
        return Numpy(dtype, self.shape)
    def __repr__(self):
        if self.shape:
            shape_str = '[{}]'.format(', '.join(str(x) for x in self.shape))
        else:
            shape_str = ''
        if self.dtype:
            dtype_str = '({})'.format(self.dtype)
        else:
            dtype_str = ''
        return 'numpy{}{}'.format(dtype_str, shape_str)
    def __str__(self):
        return self.__repr__()

def incorrect_arg_type(arg_value, arg_name, arg_type, signature):
    message = '{} does not conform to "{}" in {}'.format(arg_value.__repr__(), arg_name, signature)
    return TypeError(message)

def check_type(arg_name, arg_type, arg_value, signature):
    if isinstance(arg_type, Type):
        try:
            arg_type.check(arg_value)
        except TypeError as e:
            raise incorrect_arg_type(arg_value, arg_name, arg_type, signature) from TypeError(str(e))
    elif not isinstance(arg_value, arg_type):

        message += signature
        raise TypeError(message)

def typed(f):
    import inspect
    signature = inspect.signature(f)
    parameters = signature.parameters

    def wrapper(*args, **kwargs):
        signature = inspect.signature(f)
        try:
            signature.bind(*args, **kwargs).arguments
        except TypeError as e:
            raise TypeError(str(e) + ' for a function with signature: ' + str(signature))
        for arg_value, parameter in zip(args, parameters.values()):
            arg_name = parameter.name
            arg_type = parameter.annotation
            check_type(arg_name, arg_type, arg_value, f.__name__ + str(signature))
        for keyword, arg_value in kwargs.items():
            parameter = parameters[keyword]
            arg_name = parameter.name
            arg_type = parameter.annotation
            check_type(arg_name, arg_type, arg_value, f.__name__ + str(signature))


        return f(*args, **kwargs)

    return wrapper
