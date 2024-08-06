import turtle
import math


WIDTH = 1000
HEIGHT = 800
MARGIN = 50
SLEEP_MS = 20

R_FRAME = 160
R_COG = 50
R_PEN = 20

L = R_FRAME - R_COG
AV = 0.1

done = False


def set_done():
    global done
    done = True


turtle.setup(WIDTH + MARGIN, HEIGHT + MARGIN)
turtle.tracer(0, 0)
turtle.title("Spirograph curves")

turtle.listen()
turtle.onkeypress(set_done, "space")

pen = turtle.Turtle()
pen.shape("circle")
pen.penup()
pen.goto(L + R_PEN, 0)
pen.pendown()

angle = 0


def tick():
    if not done:
        global angle

        Angle = -R_COG * angle / L
        x_cog = L * math.cos(Angle)
        y_cog = L * math.sin(Angle)
        x_pen = x_cog + R_PEN * math.cos(angle)
        y_pen = y_cog + R_PEN * math.sin(angle)
        pen.goto(x_pen, y_pen)

        angle += AV

        turtle.update()
        turtle.ontimer(tick, SLEEP_MS)


tick()
turtle.done()
        
        