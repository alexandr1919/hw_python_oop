from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO_MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.INFO_MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    M_IN_H: int = 60
    S_IN_M: int = 60
    LEN_STEP: float = 0.65

    def __init__(
        self,
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

    def training_type(self) -> str:
        """Вернуть тип тренировки"""
        return self.__class__.__name__

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(
            self.training_type(),
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки 'Бег'"""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * (self.weight
                / self.M_IN_KM) * (self.duration * self.M_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MULTIPLIER: float = 0.035
    PHYSICAL_PROPERTIES_MULTIPLIER: float = 0.029
    S_IN_H_RATIO: float = 0.278
    CM_IN_M: int = 100

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.mean_speed_m_s = self.get_mean_speed() * self.S_IN_H_RATIO
        self.height_metres = self.height / self.CM_IN_M
        self.duration_minutes = self.duration * self.M_IN_H

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки 'Ходьба'"""
        return ((self.WEIGHT_MULTIPLIER * self.weight
                 + ((self.mean_speed_m_s**2) / self.height_metres)
                 * self.PHYSICAL_PROPERTIES_MULTIPLIER * self.weight)
                * self.duration_minutes)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    MEAN_SPEED_OFFSET = 1.1
    SPENT_CALORIES_MULTIPLIER = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки 'Плавание'"""
        return ((self.get_mean_speed() + self.MEAN_SPEED_OFFSET)
                * self.SPENT_CALORIES_MULTIPLIER * self.weight * self.duration)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения для тренировки 'Плавание'"""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    training = training_dict[workout_type](*data)

    return training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
