from typing import List


class Car:
    def __init__(
            self,
            max_speed: int,
            max_passengers: int,
            doors: int,
            horse_power: int,
            clearence: int,
            fuel_concumption: float,
            load_capacity: int,
            fuel_tank: int,
            now_fuel_tank: float,
    ):
        self._max_speed: int = max_speed
        self._max_passengers: int = max_passengers
        self._doors: int = doors
        self._horse_power: int = horse_power
        self._clearence: int = clearence
        self._fuel_concumption: float = fuel_concumption
        self._load_capacity: int = load_capacity
        self._fuel_tank: int = fuel_tank
        self._now_fuel_tank: float = now_fuel_tank

    def get_max_travel_distance(self) -> float:
        max_travel_distance = self._now_fuel_tank / self._fuel_concumption
        return max_travel_distance

    def is_possible_to_carry(self, passenger_weights: List[float], baggage_weight: float) -> bool:
        sum_passenger_weights = sum(passenger_weights)
        sum_passenger_baggage_weights = sum_passenger_weights + baggage_weight
        return self._load_capacity > sum_passenger_baggage_weights


def is_people_get(cars: List[Car], how_many_people: int) -> bool:
    sum_max_passengers = 0
    for car in cars:
        sum_max_passengers += car._max_passengers
    return sum_max_passengers >= how_many_people


def travel_distance_to_low_car(cars: List[Car]) -> float:
    minimal_travel_dist_car = None
    for car in cars:
        if minimal_travel_dist_car is None:
            minimal_travel_dist_car = car.get_max_travel_distance()
        elif car.get_max_travel_distance() < minimal_travel_dist_car:
            minimal_travel_dist_car = car.get_max_travel_distance()
    return minimal_travel_dist_car


def main():
    cars = [
        Car(
            max_speed=100,
            max_passengers=4,
            doors=4,
            horse_power=100,
            clearence=2,
            fuel_concumption=10,
            load_capacity=6,
            fuel_tank=50,
            now_fuel_tank=50,
        ),
        Car(
            max_speed=200,
            max_passengers=4,
            doors=4,
            horse_power=150,
            clearence=2,
            fuel_concumption=15,
            load_capacity=6,
            fuel_tank=70,
            now_fuel_tank=70,
        ),
        Car(
            max_speed=300,
            max_passengers=4,
            doors=4,
            horse_power=200,
            clearence=2,
            fuel_concumption=15,
            load_capacity=5,
            fuel_tank=80,
            now_fuel_tank=80,
        ),
        Car(
            max_speed=150,
            max_passengers=4,
            doors=4,
            horse_power=100,
            clearence=2,
            fuel_concumption=10,
            load_capacity=6,
            fuel_tank=60,
            now_fuel_tank=60,
        ),
        Car(
            max_speed=400,
            max_passengers=2,
            doors=2,
            horse_power=500,
            clearence=1,
            fuel_concumption=20,
            load_capacity=3,
            fuel_tank=100,
            now_fuel_tank=100,
        ),
    ]
    print(is_people_get(cars, how_many_people=15))
    print(travel_distance_to_low_car(cars))


if __name__ == "__main__":
    main()
