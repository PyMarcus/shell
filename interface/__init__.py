from abc import ABC, abstractmethod


class ICommand(ABC):
    @abstractmethod
    def dir(self, *args):
        raise NotImplementedError

    @abstractmethod
    def cat(self, *args):
        raise NotImplementedError

    @abstractmethod
    def edit(self, *args):
        raise NotImplementedError

    @abstractmethod
    def exit(self, *args):
        raise NotImplementedError

    @abstractmethod
    def cd(self, *args):
        raise NotImplementedError

    @abstractmethod
    def mkdir(self, *args):
        raise NotImplementedError

    @abstractmethod
    def rm_d(self, *args):
        raise NotImplementedError

    @abstractmethod
    def mv(self, *args):
        raise NotImplementedError

    @abstractmethod
    def cp(self, *args):
        raise NotImplementedError

    @abstractmethod
    def rm_a(self, *args):
        raise NotImplementedError

    @abstractmethod
    def ver(self, *args):
        raise NotImplementedError
