import turtle
import math
import itertools
from random import uniform
from dataclasses import dataclass


WIDTH = 1200   # canvas width
HEIGHT = 800  # canvas height
V = 10        # molecule speed
R = 10        # molecule radius
MARGIN = 50   # additional space for the drawing canvas
SLEEP_MS = 20
N =  20       # number of molecules in our vessel
COLOR_ITER = itertools.cycle(["red", "green", "blue", "black", "yellow", "pink", "purple", "cyan"])

right_wall = WIDTH / 2 - R
top_wall = HEIGHT / 2 - R


@dataclass
class SimState:
    done: bool
    delta_p: float
    delta_t: int
    
    def set_done(self):
        self.done = True
    
    def pressure(self):
        area = 2 * (2 * right_wall + 2 * top_wall)
        force = self.delta_p / self.delta_t
        return force / area

    @classmethod
    def setup(cls):
        r = cls(False, 0, 0)
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
            sim_state.delta_p += abs(self.vx)
        
        if abs(self.m.ycor()) > top_wall:
            self.vy *= -1
            sim_state.delta_p += abs(self.vy)

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
    turtle.tracer(0, 0)  # turn off turtle animation
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
setup_screen("Boyle-Mariotte's law")
draw_vessel()
molecules = [Molecule.create() for _ in range(N)]


def tick():
    if not sim_state.done:
        for m in molecules:
            m.move()
        
        sim_state.delta_t += 1
        
        if sim_state.delta_t % 100 == 0:
            vol = (2 * top_wall) * (2 * right_wall)
            print(round(sim_state.pressure() * vol))
        
        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()