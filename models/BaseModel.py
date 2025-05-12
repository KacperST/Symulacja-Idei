import abc

class BaseModel(abc.ABC):

    @abc.abstractmethod
    def step(self):
        pass

    @abc.abstractmethod
    def is_unanimous(self):
        pass