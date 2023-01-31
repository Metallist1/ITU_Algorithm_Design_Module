from abc import abstractmethod

from RedScareSolutions.Helpers.singleton import SingletonABCMeta


class ProblemInterface(metaclass=SingletonABCMeta):

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def get_result(self): raise NotImplementedError
