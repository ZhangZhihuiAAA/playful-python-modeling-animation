import turtle


WIDTH = 1000
HEIGHT = 800
MARGIN = 50
SLEEP_MS = 20

AX_COEFFICIENT = -0.003
AY_COEFFICIENT = -0.002
START_X, START_Y = 100, 200

done = False


def set_done():
    global done
    done = True


turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
turtle.tracer(0, 0)
turtle.title("Lissajous figures")

turtle.listen()
turtle.onkeypress(set_done, "space")

m = turtle.Turtle()
m.shape("circle")
m.penup()
m.goto(START_X, START_Y)
m.pendown()

vx, vy = 0, 0

def tick():
    if not done:
        global vx, vy

        m.goto(m.xcor() + vx, m.ycor() + vy)

        vx += m.xcor() * AX_COEFFICIENT
        vy += m.ycor() * AY_COEFFICIENT

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()