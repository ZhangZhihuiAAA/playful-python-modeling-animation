import turtle
from random import uniform, randint
from dataclasses import dataclass


H = 30  # grass patch size
W = 50
SLEEP_MS = 100

GRASS_GROWTH= 0.04  # units per step
RABBITS = 100
WOLVES = 10

MIN_DELIVERY_FAT = 0.7  # needed to deliver an offspring
NEWBORN_FAT = 0.5
D = 3


# fine-tunable parameters of rabbits and wolves
@dataclass
class RabbitConfig:
    fat_use: float = 0.20
    max_age: int = 10
    delivery_age : int = 3
    delivery_p = 0.6
    fat_factor = 1
    shape: str = "turtle"
    color: str = "rosy brown"


@dataclass
class WolfConfig:
    fat_use: float = 0.04
    max_age: int = 17
    delivery_age: int = 4
    delivery_p = 0.4
    fat_factor = 0.6
    shape: str = "classic"
    color: str = "black"


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
class Shape:
    drawer: turtle.Turtle

    def update(self, fat, is_alive):
        if not is_alive:
            self.drawer.hideturtle()
        else:
            self.drawer.shapesize(fat)

    def move(self, coord):
        self.drawer.goto(coord[0], coord[1])

    @classmethod
    def create(cls, shape, color, size, coord):
        r = turtle.Turtle()
        r.shape(shape)
        r.color(color)
        r.shapesize(size)
        r.penup()
        r.goto(coord[0], coord[1])
        r.right(90)
        return cls(r)


@dataclass
class Grass:
    shape: Shape
    amount: float

    def grow(self):
        self.amount = min(self.amount + GRASS_GROWTH, 1)
        self.shape.update(self.amount, True)

    def eaten(self, needed_amount):
        eaten_amount = min(needed_amount, self.amount)
        self.amount -= eaten_amount
        return eaten_amount

    @classmethod
    def create(cls, coord):
        amount = uniform(0, 1)
        color = "lawn green"
        return cls(Shape.create("circle", color, amount, coord), amount)


@dataclass
class Animal:
    shape: Shape
    fat: float
    age: int
    cfg: object

    def is_alive(self):
        return self.fat > 0 and self.age <= self.cfg.max_age

    def eaten(self, needed_amount):
        # A rabbit escapes (zero is returned) if its fat reserve exceeds 
        # the hunting wolf’s needs. Otherwise, all the fat is consumed.
        eaten_amount = 0 if self.fat > needed_amount else self.fat
        self.fat -= eaten_amount
        self.shape.update(self.fat, self.is_alive())
        return eaten_amount

    def update_fat(self, food):
        self.fat = max(0, self.fat - self.cfg.fat_use)
        self.age += 1

        if self.is_alive() and food:
            food_needed = (1.0 - self.fat) / self.cfg.fat_factor
            if (r := food.eaten(food_needed)) > 0:
                self.fat += r * self.cfg.fat_factor
        self.shape.update(self.fat, self.is_alive())

    def move_to(self, coord):
        self.shape.move(coord)
        return self

    @classmethod
    def create_full(cls, cfg, age, fat, coord):
        shape = Shape.create(cfg.shape, cfg.color, fat, coord)
        return cls(shape, fat, age, cfg)

    @classmethod
    def create_newborn(cls, cfg, coord):
        return cls.create_full(cfg, 0, NEWBORN_FAT, coord)

    def deliver_at(self, coord):
        fat_enough = self.fat >= MIN_DELIVERY_FAT
        old_enough = self.age >= self.cfg.delivery_age
        kucky_enough = self.cfg.delivery_p >= uniform(0, 1)
        deliverable = fat_enough and old_enough and kucky_enough
        return Animal.create_newborn(self.cfg, coord) if deliverable else None

    @classmethod
    def create(cls, cfg, coord):
        age = randint(0, cfg.max_age)
        return cls.create_full(cfg, age, uniform(0, 1), coord)


@dataclass
class WorldState:
    grass: dict
    rabbits: dict
    wolves: dict
    cycle: int

    # get all non-None objects
    def animals(self, meadow):
        return list((key, value) for (key, value) in meadow.items() if value)

    def keep_alive(self, meadow):
        animals = self.animals(meadow)
        meadow.update({k: None for (k, v) in animals if not v.is_alive()})

    def move_and_deliver(self, meadow):
        for coord, v in self.animals(meadow):
            x, y = coord
            newcoord = randint(x - D, x + D) % W, randint(y - D, y + D) % H
            if not meadow[newcoord]:
                meadow[newcoord] = v.move_to(newcoord)
                meadow[coord] = v.deliver_at(coord)

    def update(self):
        self.cycle += 1
        rabbits = self.animals(self.rabbits)
        wolves = self.animals(self.wolves)
        print(f"{self.cycle}\t{len(rabbits)}\t{len(wolves)}")

        for v in self.grass.values():
            v.grow()

        for coord, v in rabbits:
            v.update_fat(self.grass[coord])

        for coord, v in wolves:
            v.update_fat(self.rabbits[coord])

        self.keep_alive(self.rabbits)
        self.keep_alive(self.wolves)

        self.move_and_deliver(self.rabbits)
        self.move_and_deliver(self.wolves)

    @classmethod
    def coords(cls, count):
        r = set()
        while len(r) < count:
            r.add((randint(0, W - 1), randint(0, H - 1)))
        return r

    @classmethod
    def setup(cls):
        coords = [(x, y) for x in range(W) for y in range(H)]

        grass = {c: Grass.create(c) for c in coords}
        rabbits = {c: None for c in coords}
        wolves = {c: None for c in coords}

        r = {c: Animal.create(RabbitConfig(), c) for c in cls.coords(RABBITS)}
        w = {c: Animal.create(WolfConfig(), c) for c in cls.coords(WOLVES)}
        rabbits.update(r)
        wolves.update(w)

        return cls(grass, rabbits, wolves, 0)


def setup_screen(title):
    turtle.setup(W * 20, H * 20)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, W, H)


setup_screen("Rabbits and wolves")
sim_state = SimState.setup()
world_state = WorldState.setup()


def tick():
    if not sim_state.done:
        world_state.update()
        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()