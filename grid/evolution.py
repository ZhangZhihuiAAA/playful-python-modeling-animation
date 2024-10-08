import turtle
from random import randint, choices
from dataclasses import dataclass


H = 40
W = 70
SLEEP_MS = 20
VIS_SLEEP_MS = 500
CELL_SIZE = 10  # pixels
SHAPE_SIZE = CELL_SIZE / 20  # turtle size

INITIAL_ENERGY = 120
MAX_ENERGY = 400
FISSION_ENERGY = 250
MATURITY_AGE = 200
FOOD_ENERGY = 20
MAX_WEIGHT = 32
PLANKTON_GROWTH= 4
PLANKTON_COUNT = 300
BUGS_COUNT = 50

gen_count = []  # bugs in the given generation
gen_visited = []  # unique cells visited by bugs of a generation


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


def clamp(v, min_v, max_v):
    return min(max(min_v, v), max_v)


@dataclass
class Plankton:
    shape: turtle.Turtle

    def energy(self):
        return FOOD_ENERGY if self.shape.isvisible() else 0

    def show(self, s):
        if s:
            self.shape.showturtle()
        else:
            self.shape.hideturtle()

    @classmethod
    def create(cls, x, y):
        p = turtle.Turtle()
        p.penup()
        p.color("lawn green")
        p.shape("triangle")
        p.shapesize(SHAPE_SIZE)
        p.goto(x, y)
        p.hideturtle()
        return cls(p)


@dataclass
class Bug:
    shape: turtle.Turtle
    direction_weights: list
    energy: int
    generation: int
    visited: set
    age: int = 0

    def x(self):
        return clamp(round(self.shape.xcor()), 0, W - 1)

    def y(self):
        return clamp(round(self.shape.ycor()), 0, H - 1)

    def remove(self):
        gen_visited[self.generation] += len(self.visited)
        self.shape.hideturtle()

    def eat_and_move(self, food):
        self.visited.add((self.x(), self.y()))
        self.age += 1
        self.energy -= 1

        if self.energy == 0:
            self.remove()
        else:
            self.energy = min(self.energy + food, MAX_ENERGY)
            r = choices(list(range(8)), self.direction_weights)[0]
            self.shape.left(45 * r)
            self.shape.forward(1)
            self.shape.goto(self.x(), self.y())

    def new_direction_weights(self, weights, multiplier):
        direction = randint(0, 7)
        new = list(weights)
        new[direction] = clamp(int(weights[direction] * multiplier), 1, MAX_WEIGHT)
        return new

    def fission(self):
        if self.age > MATURITY_AGE and self.energy > FISSION_ENERGY:
            self.remove()
            e = int(self.energy / 2)
            direction_weights1= self.new_direction_weights(self.direction_weights, 2)
            direction_weights2 = self.new_direction_weights(self.direction_weights, 0.5)

            return [
                Bug.create(self.x(), self.y(), direction_weights1, e, self.generation + 1),
                Bug.create(self.x(), self.y(), direction_weights2, e, self.generation + 1),
            ]
        return [self]

    @classmethod
    def create(cls, x, y, weights, energy, gen):
        if gen == len(gen_count):
            print(f"Generation: {gen}")
            gen_count.append(0)
            gen_visited.append(0)
        gen_count[gen] += 1

        p = turtle.Turtle()
        p.penup()
        p.color("blue")
        p.shape("turtle")
        p.shapesize(SHAPE_SIZE)
        p.goto(x, y)
        return cls(p, weights, energy, gen, set())

    @classmethod
    def create_random(cls):
        x = randint(0, W - 1)
        y = randint(0, H - 1)
        weights = [randint(1, MAX_WEIGHT) for _ in range(8)]
        return cls.create(x, y, weights, INITIAL_ENERGY, 0)


@dataclass
class WorldState:
    plankton: list
    bugs: list
    cycle: int = 0
    min_gen: int = 0

    def add_plankton(self, count=1):
        for _ in range(count):
            x, y = randint(0, W - 1), randint(0, H - 1)
            self.plankton[x][y].show(True)
        return self

    def update(self):
        self.cycle += 1
        self.add_plankton(PLANKTON_GROWTH)

        for b in self.bugs:
            food = self.plankton[b.x()][b.y()]
            b.eat_and_move(food.energy())
            food.show(False)

        self.bugs = [b for b in self.bugs if b.energy > 0]
        self.bugs = sum((b.fission() for b in self.bugs), [])

    def report_visits(self):
        new_min_gen = min(b.generation for b in self.bugs)
        if new_min_gen != self.min_gen:
            self.min_gen = new_min_gen
            visits = (gen_visited[i] / gen_count[i] for i in range(new_min_gen))
            print([f"{v:.2f}" for v in visits])

    @classmethod
    def setup(cls):
        bugs = [Bug.create_random() for _ in range(BUGS_COUNT)]
        plankton = [[Plankton.create(x, y) for y in range(H)] for x in range(W)]
        return cls(plankton, bugs).add_plankton(PLANKTON_COUNT)


def setup_screen(title):
    turtle.setup(W * CELL_SIZE, H * CELL_SIZE)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, W, H)


setup_screen("Evolution")
sim_state = SimState.setup()
world_state = WorldState.setup()


def tick():
    if not sim_state.done:
        world_state.update()
        turtle.ontimer(tick, SLEEP_MS)


def tick_draw():
    if not sim_state.done:
        turtle.update()
        world_state.report_visits()
        turtle.ontimer(tick_draw, VIS_SLEEP_MS)


tick()
tick_draw()
turtle.done()