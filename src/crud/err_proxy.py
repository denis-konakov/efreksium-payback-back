class ErrorHandleProxy:
    def __init__(self, obj):
        self.__value = obj
    def __getattribute__(self, item):
        r = self.__value.__getattribute__(item)
        return ErrorHandleProxy(r)
    def __call__(self, *args, **kwargs):
        try:
            return self.__value(*args, **kwargs), None
        except Exception as e:
            return None, e

class CRUDBase:
    @classmethod
    def handled(cls):
        return ErrorHandleProxy(cls)
