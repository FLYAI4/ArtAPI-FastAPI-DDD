from abc import ABC, abstractmethod


class DBManager(ABC):
    @abstractmethod
    def get_session(self):
        pass
