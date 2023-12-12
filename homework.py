from dataclasses import dataclass, asdict


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
    M_IN_H = 60
    S_IN_M = 60
    LEN_STEP = 0.65
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'''Метод для получения затраченных калорий
                                  в {type(self).__name__}.''')

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
            * (self.duration * self.M_IN_H)
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029
    S_IN_H_RATIO = round((1 * 1000 / 3600), 3)
    CM_IN_M = 100
    height: float

    def height_in_metres(self):
        """Получить высоту в метрах"""
        return self.height / self.CM_IN_M

    def duration_in_minutes(self):
        """Получить длительность в минутах"""
        return self.duration * self.M_IN_H

    def mean_speed_m_s(self):
        """Получить среднюю сокрость в м/с"""
        return self.get_mean_speed() * self.S_IN_H_RATIO

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки 'Ходьба'"""
        return (
            (
                self.WEIGHT_MULTIPLIER_1
                * self.weight
                + (
                    self.mean_speed_m_s()**2
                    / self.height_in_metres()
                )
                * self.WEIGHT_MULTIPLIER_2
                * self.weight)
            * self.duration_in_minutes())


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    MEAN_SPEED_OFFSET = 1.1
    WEIGHT_MULTIPLIER = 2
    length_pool: float
    count_pool: float

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


def read_package(workout_type: str, data: list[float]) -> Training:
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
