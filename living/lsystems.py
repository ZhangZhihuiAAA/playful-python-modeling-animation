import turtle
from dataclasses import dataclass


WIDTH = 1200
HEIGHT = 800
PEDESTRAL = 100

# a simple plant with a bud
AXIOM = "A"
RULES = {"A": "g[+A][-A]"}
ANGLE = 20
DISTANCE = 25
STEPS = 6

# the LRI plant with a bud
# AXIOM = "A"
# RULES = {"A": "AILR", "I": "g", "L": "[+g]", "R": "[-g]"}
# ANGLE = 30
# DISTANCE = 20
# STEPS = 4

# another example plant
# AXIOM = "X"  # "g"
# RULES = {"X": "g[+X]g[-X]+X", "g": "gg"}
# ANGLE = 40
# DISTANCE = 10
# STEPS = 4

# AXIOM = "X"
# RULES = {"X": "g-[[X]+X]+g[+gX]-X", "g": "gg"}
# ANGLE = 22.5
# DISTANCE = 10
# STEPS = 4

# AXIOM = "X"
# RULES = {"X": "g[+X]g[-X]+X", "g": "gg"}
# ANGLE = 25
# DISTANCE = 15
# STEPS = 4

# AXIOM = "g"
# RULES = {"g": "gg-[-g+g+g]+[+g-g-g]"}
# ANGLE = 22.5
# DISTANCE = 6
# STEPS = 4

# AXIOM = "X"
# RULES = {"X": "g[+X][-X]gX", "g": "gg"}
# ANGLE = 25.7
# DISTANCE = 3
# STEPS = 7

# AXIOM = "f"
# RULES = {"f": "f+g", "g": "f-g"}
# ANGLE = 90
# DISTANCE = 10
# STEPS = 7

# AXIOM = "g-g-g-g"
# RULES = {"g": "g-g+g+gg-g-g+g"}
# DISTANCE = 4
# ANGLE = 90
# STEPS = 3

# AXIOM = "g"
# RULES = {"g": "g[+g][-g]"}
# ANGLE = 20
# DISTANCE = 25
# STEPS = 6


def setup_screen(title):
    turtle.setup(WIDTH, HEIGHT)
    # turtle.tracer(0, 0)
    turtle.title(title)


@dataclass
class LSystem:
    script: str

    @classmethod
    def create(cls):
        r = cls(AXIOM)
        for i in range(STEPS):
            r.transform()
        return r

    def transform(self):
        self.script = "".join([self.apply_rule(c) for c in self.script])

    def apply_rule(self, c):
        return c if c not in RULES else RULES[c]

    def draw(self, drawer):
        while self.script:
            c = self.script[0]
            self.script = self.script[1:]

            if c.islower():
                drawer.forward(DISTANCE)
                turtle.update()
            elif c == "+":
                drawer.color("red")
                drawer.left(ANGLE)
            elif c == "-":
                drawer.color("green")
                drawer.right(ANGLE)
            elif c == "[":
                self.draw(drawer.clone())
            elif c == "]":
                return


setup_screen("L-systems")

drawer = turtle.Turtle()  # place at the bottom, point upward
drawer.color("blue")
drawer.hideturtle()
drawer.penup()
drawer.goto(0, -HEIGHT / 2 + PEDESTRAL)
drawer.left(90)
drawer.pendown()

LSystem.create().draw(drawer)

turtle.done()