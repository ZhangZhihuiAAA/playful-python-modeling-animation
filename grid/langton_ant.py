import turtle
from dataclasses import dataclass


H = 81
W = 81
SLEEP_MS = 20
CELL_SIZE = 5
SHAPE_SIZE = CELL_SIZE / 20


@dataclass
class SimState:
    to_exit: bool
    paused: bool

    def exit(self):
        exit()

    def pause_resume(self):
        self.paused = not self.paused

    @classmethod
    def setup(cls):
        r = cls(False, False)
        turtle.listen()
        turtle.onkeypress(r.pause_resume, "space")
        turtle.onkeypress(r.exit, "e")
        turtle.onkeypress(r.exit, "E")
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

    def is_black(self):
        return self.shape.isvisible()

    def flip(self):
        if self.is_black():
            self.shape.hideturtle()
        else:
            self.shape.showturtle()


def make_ant(x, y):
    p = turtle.Turtle()
    p.penup()
    p.shape("turtle")
    p.shapesize(SHAPE_SIZE / 2)
    p.goto(x, y)
    p.color("red")
    return p


@dataclass
class WorldState:
    board: list
    ant: turtle.Turtle
    step: int = 0

    def update(self):
        self.step += 1
        if self.step % 1000 == 0:
            print(f"Performing step: {self.step}")

        x = round(self.ant.xcor())
        y = round(self.ant.ycor())
        turn = 90 if self.board[x][y].is_black() else -90

        self.board[x][y].flip()
        self.ant.left(turn)
        self.ant.forward(1)

    @classmethod
    def setup(cls):
        board = [[CellShape.create(x, y) for y in range(H)] for x in range(W)]
        ant = make_ant(W // 2, H // 2)
        return cls(board, ant)


def setup_screen(title):
    turtle.setup(W * CELL_SIZE, H * CELL_SIZE)
    turtle.tracer(0, 0)
    turtle.title(title)
    turtle.setworldcoordinates(0, 0, W, H)


setup_screen("Langton's ant")
sim_state = SimState.setup()
world_state = WorldState.setup()


def tick():
    if not sim_state.to_exit:
        if not sim_state.paused:
            world_state.update()
            turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()