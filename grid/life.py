import turtle
from random import randint
from dataclasses import dataclass


H = 41
W = 41
SLEEP_MS = 20
CELL_SIZE = 10
SHAPE_SIZE = CELL_SIZE / 20


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
class CellShape:
    shape: turtle.Turtle

    @classmethod
    def create(cls, x, y):
        p = turtle.Turtle()
        p.penup()
        p.shape("circle")
        p.shapesize(SHAPE_SIZE)
        p.goto(x, y)
        p.hideturtle()
        return cls(p)

    def update(self, show):
        if show:
            self.shape.showturtle()
        else:
            self.shape.hideturtle()


@dataclass
class WorldState:
    shapes: list
    current: list
    next: list

    def neighbors_count(self, x, y):
        n_neighbors = -int(self.current[x][y])
        for xn in range(x - 1, x + 2):
            for yn in range(y - 1, y + 2):
                n_neighbors += int(self.current[xn % W][yn % H])
        return n_neighbors

    def next_status(self, x, y):
        n_neighbors = self.neighbors_count(x, y)

        if not self.current[x][y] and n_neighbors == 3:
            return True
        if self.current[x][y] and (n_neighbors < 2 or n_neighbors > 3):
            return False

        return self.current[x][y]

    def update(self):
        for x in range(W):
            for y in range(H):
                self.shapes[x][y].update(self.current[x][y])
                self.next[x][y] = self.next_status(x, y)

        self.current, self.next = self.next, self.current

    @classmethod
    def setup(cls, population):
        shapes = [[CellShape.create(x, y) for y in range(H)] for x in range(W)]
        current = [[False for _ in range(H)] for _ in range(W)]
        next = [[False for _ in range(H)] for _ in range(W)]

        for x, y in population:
            current[x][y] = True

        return cls(shapes, current, next)


def setup_screen(title):
    turtle.setup(W * CELL_SIZE, H * CELL_SIZE)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, W, H)


setup_screen("Life")
sim_state = SimState.setup()
world_config = [(randint(0, W - 1), randint(0, H - 1)) for _ in range(200)]
world_state = WorldState.setup(world_config)


def tick():
    if not sim_state.done:
        world_state.update()
        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()