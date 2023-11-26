import dataclasses
import sys


@dataclasses.dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_HOUR = 60

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration, distance=self.get_distance(),
                           speed=self.get_mean_speed(), calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def get_spent_calories(self) -> float:
        return ((self.coeff_calorie_1 * self.get_mean_speed() - self.coeff_calorie_2) * self.weight /
                self.M_IN_KM * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action: int, duration: float, weight: float, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    coeff_calorie_1 = 0.035
    coeff_calorie_2 = 0.029

    def get_spent_calories(self) -> float:
        return (self.coeff_calorie_1 * self.weight + self.get_mean_speed() ** 2 //
                self.height * self.coeff_calorie_2 * self.weight) * self.duration * self.MIN_IN_HOUR


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float, length_pool: float, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    coeff_calorie_1 = 1.1
    coeff_calorie_2 = 2

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.coeff_calorie_1) * self.coeff_calorie_2 * self.weight


def read_package(workout: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    sport_types = {'SWM': Swimming,
                   'RUN': Running,
                   'WLK': SportsWalking}
    try:
        return sport_types[workout](*data)
    except KeyError:
        print('An unexpected workout type!')
        sys.exit(1)


def main(training: Training) -> None:
    """Главная функция."""
    message = training.show_training_info()
    print(message.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
