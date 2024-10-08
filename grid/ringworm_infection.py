import turtle
from enum import Enum
from random import randint
from dataclasses import dataclass


H = 41
W = 41
SLEEP_MS = 20
CELL_SIZE = 15  # pixels
SHAPE_SIZE = CELL_SIZE / 20  # turtle size


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


class Status(Enum):
    HEALTHY = 1
    INFECTED = 2
    IMMUNE = 3


@dataclass
class Cell:
    shape: turtle.Turtle
    status: Status
    duration: int

    @classmethod
    def create(cls, x, y):
        p = turtle.Turtle()
        p.penup()
        p.shape("circle")
        p.shapesize(SHAPE_SIZE)
        p.goto(x, y)
        p.color("white")
        return cls(p, Status.HEALTHY, 0)

    def update_status(self, status, duration):
        self.status = status
        self.duration = duration

        colors = {
            Status.HEALTHY: "white",
            Status.INFECTED: "red",
            Status.IMMUNE: "blue",
        }
        self.shape.color(colors[status])

    def update(self):
        self.duration = max(0, self.duration - 1)
        if self.duration == 0:
            if self.status == Status.IMMUNE:
                self.update_status(Status.HEALTHY, 0)
            elif self.status == Status.INFECTED:
                self.update_status(Status.IMMUNE, 4)


@dataclass
class WorldState:
    cells: list

    def spread_from(self, x, y):
        r = []
        for xn in range(max(0, x - 1), min(x + 2, W)):
            for yn in range(max(0, y - 1), min(y + 2, H)):
                neighbor = self.cells[xn][yn]
                if neighbor.status == Status.HEALTHY and randint(0, 1) == 1:
                    r.append(neighbor)
        return r

    def update(self):
        for x in range(W):
            for y in range(H):
                self.cells[x][y].update()

        to_infect = []
        for x in range(W):
            for y in range(H):
                if self.cells[x][y].status == Status.INFECTED:
                    to_infect += self.spread_from(x, y)

        for c in to_infect:
            c.update_status(Status.INFECTED, 6)

    @classmethod
    def setup(cls):
        cells = [[Cell.create(x, y) for y in range(H)] for x in range(W)]
        cells[W // 2][H // 2].update_status(Status.INFECTED, 6)  # (W // 2, H // 2) is the central cell
        return cls(cells)


def setup_screen(title):
    turtle.setup(W * CELL_SIZE, H * CELL_SIZE)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, W, H)


setup_screen("Ringworm infection")
sim_state = SimState.setup()
world_state = WorldState.setup()


def tick():
    if not sim_state.done:
        world_state.update()
        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()