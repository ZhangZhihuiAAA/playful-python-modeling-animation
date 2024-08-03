import turtle
import math
import itertools
from random import uniform
from dataclasses import dataclass


WIDTH = 1200  # canvas width
HEIGHT = 800  # canvas height
V = 10        # molecule speed
R = 10        # molecule radius
MARGIN = 50   # additional space for the drawing canvas
SLEEP_MS = 20
VIS_SLEEP_MS = 40
N =  30       # number of molecules in our vessel
COLOR_ITER = itertools.cycle(["red", "green", "blue", "black", "yellow", "pink", "purple", "cyan"])

right_wall = WIDTH / 2 - R
top_wall = HEIGHT / 2 - R


@dataclass
class SimState:
    done: bool

    def set_done(self):
        self.done = True

    @classmethod
    def setup(cls):
        r = cls(False)
        turtle.listen()
        turtle.onkeypress(r.set_done, "space")
        return r


@dataclass
class Molecule:
    m: turtle.Turtle
    vx: float
    vy: float

    def move(self):
        self.m.goto(self.m.xcor() + self.vx, self.m.ycor() + self.vy)
        
        if abs(self.m.xcor()) > right_wall:
            self.vx *= -1
        
        if abs(self.m.ycor()) > top_wall:
            self.vy *= -1

    @classmethod
    def create(cls):
        m = turtle.Turtle()
        m.shape("circle")
        m.color(next(COLOR_ITER))
        m.penup()
        m.goto(uniform(-right_wall, right_wall), uniform(-top_wall, top_wall))
        angle = uniform(0, 2 * math.pi)
        return cls(m, V * math.cos(angle), V * math.sin(angle))


def setup_screen(title):
    turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
    turtle.tracer(0, 0)                # turn off turtle animation
    turtle.title(title)  # set the main window title


def draw_vessel():
    m = turtle.Turtle()
    m.hideturtle()
    m.penup()
    m.goto(-WIDTH / 2, -HEIGHT / 2)
    m.pendown()
    m.sety(HEIGHT / 2)
    m.setx(WIDTH / 2)
    m.sety(-HEIGHT / 2)
    m.setx(-WIDTH / 2)


sim_state = SimState.setup()
setup_screen("Ideal gas")
draw_vessel()
molecules = [Molecule.create() for _ in range(N)]


def tick_draw():
    if not sim_state.done:
        turtle.update()
        turtle.ontimer(tick_draw, VIS_SLEEP_MS)


def tick():
    if not sim_state.done:
        for m in molecules:
            m.move()
        turtle.ontimer(tick, SLEEP_MS)


tick()
tick_draw()
turtle.done()