from ball import Ball
from PyQt6.QtCore import QPointF


def average(list_of_balls):
    sum_radius = 0
    for ball in list_of_balls:
        sum_radius += ball._radius
    average_value = sum_radius / 10
    print(average_value)


def intersection(list_of_balls):
    x = 0
    for ball in list_of_balls:
        if not ball.is_clicked(mouse_position=(QPointF(75, 0))):
            x += 1
    print(x)


def main():
    list_of_balls = [
        Ball(x=0, y=0, speed=1, default_color="red", hover_color="red", radius=radius)
        for radius in range(10, 101, 10)
    ]
    average(list_of_balls)
    intersection(list_of_balls)


if __name__ == "__main__":
    main()
