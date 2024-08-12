import turtle
from enum import Enum
from random import randint, uniform
from dataclasses import dataclass


H = 41
W = 41
SLEEP_MS = 20
CELL_SIZE = 10
SHAPE_SIZE = CELL_SIZE / 20

IMMUNE_DURATION = 14
INFECTED_DURATION = 7
P_INHABIT = 0.3  # probability for a cell to be inhabited
P_INFECT = 0.5   # probability for a cell to be infected by a neighbor


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

    def x(self):
        return int(self.shape.xcor())

    def y(self):
        return int(self.shape.ycor())

    @classmethod
    def populate(cls, x, y):
        if uniform(0, 1) > P_INHABIT and not (x == W // 2 and y == H // 2):
            return None
        p = turtle.Turtle()
        p.penup()
        p.shape("circle")
        p.shapesize(SHAPE_SIZE)
        p.goto(x, y)
        p.color("green")
        return cls(p, Status.HEALTHY, 0)

    def update_status(self, status, duration):
        self.status = status
        self.duration = duration

        status_colors = {
            Status.HEALTHY: "green",
            Status.INFECTED: "red",
            Status.IMMUNE: "blue",
        }
        self.shape.color(status_colors[status])

    def update(self):
        self.duration = max(0, self.duration - 1)
        if self.duration == 0:
            if self.status == Status.IMMUNE:
                self.update_status(Status.HEALTHY, 0)
            elif self.status == Status.INFECTED:
                self.update_status(Status.IMMUNE, IMMUNE_DURATION)

    def moved_to(self, x, y):
        self.shape.goto(x, y)
        return self


@dataclass
class WorldState:
    cells: list

    def spread_from(self, x, y):
        r = []
        for xn in range(x - 1, x + 2):
            for yn in range (y - 1, y + 2):
                cell = self.cells[xn % W][yn % H]
                is_healthy = cell and cell.status == Status.HEALTHY
                if is_healthy and uniform(0, 1) <= P_INFECT:
                    r.append(cell)
        return r

    def move(self, people):
        new_x = randint(people.x() - 1, people.x() + 1) % W
        new_y = randint(people.y() - 1, people.y() + 1) % H

        if not self.cells[new_x][new_y]:
            self.cells[people.x()][people.y()] = None
            self.cells[new_x][new_y] = people.moved_to(new_x, new_y)

    def print_stats(self, people):
        n_healthy = len([p for p in people if p.status == Status.HEALTHY])
        n_infected = len([p for p in people if p.status == Status.INFECTED])
        n_immune = len([p for p in people if p.status == Status.IMMUNE])
        print(f"{n_healthy}\t{n_infected}\t{n_immune}")

    def update(self):
        to_infect = []
        people = sum(([v for v in self.cells[x] if v] for x in range(W)), [])
        self.print_stats(people)

        for p in people:
            p.update()
            self.move(p)

            if p.status == Status.INFECTED:
                to_infect += self.spread_from(p.x(), p.y())

        for c in to_infect:
            c.update_status(Status.INFECTED, INFECTED_DURATION)

    @classmethod
    def setup(cls):
        cells = [[Cell.populate(x, y) for y in range(H)] for x in range(W)]
        cells[W // 2][H // 2].update_status(Status.INFECTED, INFECTED_DURATION)
        return cls(cells)


def setup_screen(title):
    turtle.setup(W * CELL_SIZE, H * CELL_SIZE)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, W, H)


setup_screen("Spread of disease")
sim_state = SimState.setup()
world_state = WorldState.setup()


def tick():
    if not sim_state.done:
        world_state.update()
        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()