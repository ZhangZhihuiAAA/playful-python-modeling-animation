import turtle


WIDTH = 1000
HEIGHT = 800
MARGIN = 50

V = 2.8
R = 5
R_EARTH = 150
PEDESTAL_H = 14
ACCELERATION = -1600
TURTLE_SIZE = 20
SLEEP_MS = 20

done = False
right_wall = WIDTH / 2 - R
bottom_wall = -HEIGHT / 2 + R


def set_done():
    global done
    done = True


turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
turtle.tracer(0, 0)
turtle.title("Newton's cannonball")

turtle.listen()
turtle.onkeypress(set_done, "space")

# draw the Earth
earth = turtle.Turtle()
earth.shape("circle")
earth.color("blue")
earth.shapesize(2 * R_EARTH / TURTLE_SIZE) 

m = turtle.Turtle()
m.shape("circle")
m.shapesize(2 * R / TURTLE_SIZE)
m.goto(0, R_EARTH + PEDESTAL_H + R)

vx = V
vy = 0


def tick():
    if not done:
        global vx, vy
        m.goto(m.xcor() + vx, m.ycor() + vy)

        r = m.distance((0, 0))

        if r < R_EARTH + R:
            set_done()

        ax = m.xcor() * ACCELERATION / (r ** 3)
        ay = m.ycor() * ACCELERATION / (r ** 3)

        vx += ax
        vy += ay

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()