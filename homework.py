from typing import Dict
from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    info: str = ('Тип тренировки: {training_type}; '
                 'Длительность: {duration:.3f} ч.; '
                 'Дистанция: {distance:.3f} км; '
                 'Ср. скорость: {speed:.3f} км/ч; '
                 'Потрачено ккал: {calories:.3f}.')

    def get_message(self):
        return self.info.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration_h: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration_h
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return(InfoMessage(
            type(self).__name__,
            self.duration_h,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()))


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIES_1 = 18
    COEFF_CALORIES_2 = 20

    def get_spent_calories(self):
        return(((self.COEFF_CALORIES_1 * self.get_mean_speed()
                 - self.COEFF_CALORIES_2)
                * self.weight / self.M_IN_KM * (self.duration_h * self.MIN)))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_3: float = 0.035
    COEFF_CALORIE_4: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self):
        return((self.COEFF_CALORIE_3
                * self.weight + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF_CALORIE_4 * self.weight)
               * self.duration_h * self.MIN)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_CALORIE_5: float = 1.1
    COEFF_CALORIE_6: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self):
        return((self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration_h))

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.COEFF_CALORIE_5)
                * self.COEFF_CALORIE_6 * self.weight)


def read_package(workout_type: str, data: Dict[int, str]) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_workouts = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    if workout_type not in type_workouts:
        raise ValueError('Не известная тренировка')
    else:
        return type_workouts[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
