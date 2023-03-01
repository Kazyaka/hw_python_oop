from typing import Iterable


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        """Объявление свойств класса и передача в них значений."""
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Сообщение о тренировке по показателям."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    M_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message: InfoMessage = InfoMessage(self.__class__.__name__,
                                                self.duration,
                                                self.get_distance(),
                                                self.get_mean_speed(),
                                                self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        calories: float = (
            (
                (
                    self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.get_mean_speed()
                )
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight / self.M_IN_KM
            * self.duration * self.M_IN_H)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 0.029
    KMH_IN_MSEC = 0.278
    SM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Вычисление потраченных калорий от ходьбы"""
        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                           * self.weight
                           + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                            / self.height * self.SM_IN_M)
                           * self.CALORIES_MEAN_SPEED_SHIFT
                           * self.weight)) * (self.duration * self.M_IN_H)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    COEF_SW_SPEED = 1.1
    COEF_SW_WEIGHT = 2
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance: float = self.length_pool * self.count_pool
        speed = distance / self.M_IN_KM / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить значение потраченных калорий."""
        summ_coef: float = self.get_mean_speed() + self.COEF_SW_SPEED
        calories = (
            summ_coef * self.COEF_SW_WEIGHT * self.weight * self.duration
        )
        return calories


def read_package(workout_type: str, data: Iterable[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_dict: dict[Training] = {'SWM': Swimming,
                                 'RUN': Running,
                                 'WLK': SportsWalking}
    return type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: Iterable[tuple[str, Iterable[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
