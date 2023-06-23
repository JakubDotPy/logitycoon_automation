from abc import ABC
from abc import abstractmethod


class Interface(ABC):

    @abstractmethod
    def foo(self):
        raise NotImplementedError()
