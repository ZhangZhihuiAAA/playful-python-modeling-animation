import turtle
from random import choices

W = 30
H = 20
CELL_SIZE = 20
SHAPE_SIZE = CELL_SIZE / 20
DAYS = 20


def setup_screen(title):
    turtle.setup(W * CELL_SIZE, H * CELL_SIZE)
    # turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, -H / 2, DAYS, H / 2)


setup_screen("Markovian weather")


def next_day(state):
    rules = {
        "sunny": (("sunny", "rainy", "cloudy"), (0.6, 0.1, 0.3)),
        "cloudy": (("cloudy", "sunny", "rainy"), (0.5, 0.3, 0.2)),
        "rainy": (("rainy", "sunny", "cloudy"), (0.4, 0.3, 0.3)),
    }
    states, weights = rules[state]
    return choices(states, weights)[0]


state = "sunny"
colors = {"sunny": "gold", "cloudy": "gray", "rainy": "black"}

for day in range(DAYS):
    drawer = turtle.Turtle()
    drawer.penup()
    drawer.shape("circle")
    drawer.shapesize(SHAPE_SIZE)
    drawer.forward(day)
    drawer.color("black", colors[state])
    state = next_day(state)

turtle.update()
turtle.done()