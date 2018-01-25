from abc import ABCMeta, abstractmethod


class Observer(metaclass=ABCMeta):
    """абстрактный наблюдатель для связи"""

    @abstractmethod
    def update(self, message: str) -> None:
        """получение сообщения"""
        pass


class Observable(metaclass=ABCMeta):
    """абстрактный наблюдаемый"""

    def __init__(self) -> None:
        """constructor"""
        self.observers = []  # список наблюдателей

    def register(self, observer: Observer) -> None:
        """регистрация нового наблюдателя на подписку"""
        self.observers.append(observer)

    def notify_observers(self, message: str) -> None:
        """Передача сообщения всем наблюдателям,
        подписанным на события данного объекта наблюдаемого класса"""
        for observer in self.observers:
            observer.update(message)


if __name__ == '__main__':
    pass
