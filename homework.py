from dataclasses import dataclass, asdict, fields


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO_MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.INFO_MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    MIN_IN_H = 60
    LEN_STEP = 0.65
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        fields(self)
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Метод для получения затраченных калорий\
                                    в {self.training_type()}.')

    def training_type(self) -> str:
        """Вернуть тип тренировки"""
        return type(self).__name__

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.training_type(),
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки 'Бег'"""
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * (self.weight / self.M_IN_KM)
            * (self.duration * self.MIN_IN_H)
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029
    CM_IN_M = 100
    SEC_IN_HOUR = 3600
    M_IN_KM = 1000
    MET_PER_SEC_RATIO = round((M_IN_KM / SEC_IN_HOUR), 3)
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки 'Ходьба'"""
        return (
            (
                self.WEIGHT_MULTIPLIER_1
                * self.weight
                + (
                    (
                        self.get_mean_speed()
                        * self.MET_PER_SEC_RATIO
                    )**2
                    / (self.height / self.CM_IN_M)
                )
                * self.WEIGHT_MULTIPLIER_2
                * self.weight
            )
            * self.duration
            * self.MIN_IN_H
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    MEAN_SPEED_OFFSET = 1.1
    WEIGHT_MULTIPLIER = 2
    length_pool: float
    count_pool: int

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки 'Плавание'"""
        return (
            (
                self.get_mean_speed()
                + self.MEAN_SPEED_OFFSET
            )
            * self.WEIGHT_MULTIPLIER
            * self.weight
            * self.duration
        )

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения для тренировки 'Плавание'"""
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )


TRAININGS = {
    "SWM": Swimming,
    "RUN": Running,
    "WLK": SportsWalking
}

INVALID_TRAINING_TYPE_MESSAGE = 'Неверный тип тренировки: {workout_type}'
INVALID_DATA_MESSAGE = 'Неверная структура полученных данных ожидается: \
{expected} значений, получено: {received}'


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAININGS:
        raise ValueError(INVALID_TRAINING_TYPE_MESSAGE
                         .format(workout_type=workout_type))
    training_type = TRAININGS[workout_type]
    if (len(fields(training_type)) != len(data)):
        raise ValueError(INVALID_DATA_MESSAGE.format(
            expected=len(fields(training_type)),
            received=len(data)))
    return training_type(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
