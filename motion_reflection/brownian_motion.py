import turtle
import math
from random import uniform
from dataclasses import dataclass


WIDTH = 1000
HEIGHT = 600
MIN_V = 5
MAX_V = 15
R = 10
PARTICLE_SIZE_FACTOR = 7
MOLECULE_SIZE_FACTOR = 0.5
MARGIN = 50
SLEEP_MS = 20
N = 150  # number of molecules in our vessel


@dataclass
class SimState:
    '''
    Press "space" to pause or resume simulation.
    Press "e" or "E" to exit simulation.
    '''

    paused: bool
    prev_collisions: set

    def pause_resume(self):
        self.paused = not self.paused

    def exit(self):
        exit()

    @classmethod
    def setup(cls):
        r = cls(False, set())
        turtle.listen()
        turtle.onkeypress(r.pause_resume, "space")
        turtle.onkeypress(r.exit, "e")
        turtle.onkeypress(r.exit, "E")
        return r


# make sure -max_value <= value <= max_value
def clamp(value, max_value):
    return math.copysign(min(abs(value), max_value), value)


@dataclass
class Molecule:
    m: turtle.Turtle
    r: float
    vx: float
    vy: float

    @classmethod
    def create(cls, size_factor = 1):
        m = turtle.Turtle()
        r = size_factor * R
        x = uniform(-WIDTH / 2 + r, WIDTH / 2 - r)
        y = uniform(-HEIGHT / 2 + r, HEIGHT / 2 - r)
        m.shape("circle")
        m.shapesize(size_factor)
        m.penup()
        m.goto(x, y)
        v = uniform(MIN_V, MAX_V)
        angle = uniform(0, 2 * math.pi)
        return cls(m, r, v * math.cos(angle), v * math.sin(angle))

    @property
    def mass(self):
        return math.pi * (self.r ** 2)

    def move(self):
        self.m.goto(self.m.xcor() + self.vx, self.m.ycor() + self.vy)

        if abs(self.m.xcor()) > WIDTH / 2 - self.r:
            self.vx *= -1

        if abs(self.m.ycor()) > HEIGHT / 2 - self.r:
            self.vy *= -1

        self.m.setx(clamp(self.m.xcor(), WIDTH / 2 - self.r))
        self.m.sety(clamp(self.m.ycor(), HEIGHT / 2 - self.r))


def setup_screen(title):
    turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
    turtle.tracer(0, 0)
    turtle.title(title)


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


def balls_collide(b1, b2):
    return b1.m.distance(b2.m) <= b1.r + b2.r


def process_collision(b1, b2):
    a = math.atan2(b2.m.ycor() - b1.m.ycor(), b2.m.xcor() - b1.m.xcor())
    A1p = math.atan2(b1.vy, b1.vx) - a
    A2p = math.atan2(b2.vy, b2.vx) - a

    v1 = math.sqrt(b1.vx ** 2 + b1.vy ** 2)
    v2 = math.sqrt(b2.vx ** 2 + b2.vy ** 2)

    vr1 = v1 * math.cos(A1p)
    vt1 = v1 * math.sin(A1p)

    vr2 = v2 * math.cos(A2p)
    vt2 = v2 * math.sin(A2p)

    m1, m2 = b1.mass, b2.mass
    vr1p = (vr1 * (m1 - m2) + 2 * m2 * vr2) / (m1 + m2)
    vr2p = vr1 + vr1p - vr2

    v1p = math.sqrt(vr1p ** 2 + vt1 ** 2)
    v2p = math.sqrt(vr2p ** 2 + vt2 ** 2)

    # new values for the trajectory angles
    A1pp = math.atan2(vt1, vr1p) + a
    A2pp = math.atan2(vt2, vr2p) + a

    b1.vx = v1p * math.cos(A1pp)
    b1.vy = v1p * math.sin(A1pp)

    b2.vx = v2p * math.cos(A2pp)
    b2.vy = v2p * math.sin(A2pp)


sim_state = SimState.setup()
setup_screen("Brownian motion")
draw_vessel()

molecules = [Molecule.create(MOLECULE_SIZE_FACTOR) for _ in range(N)]

particle = Molecule.create(PARTICLE_SIZE_FACTOR)
particle.vx = particle.vy = 0
particle.m.goto(0, 0)
particle.m.color("blue")
molecules.append(particle)


def tick():
    if not sim_state.paused:
        for m in molecules:
            m.move()

        collisions = set()
        for i in range(len(molecules)):
            for j in range(0, i):
                if balls_collide(molecules[i], molecules[j]):
                    collisions.add((i, j))
                    if not (i, j) in sim_state.prev_collisions:
                        process_collision(molecules[i], molecules[j])

        sim_state.prev_collisions = collisions

    turtle.update()
    turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()