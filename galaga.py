import turtle
import os
# creating the window
window = turtle.Screen()
window.bgcolor("black")
window.title("Galaga")

# bd = border drawer making the boarder
bd = turtle.Turtle()
bd.speed(0)
bd.color("white")
bd.penup()
bd.setposition(-300,-300)
bd.pendown()
bd.pensize(3)
for side in range(4):
	bd.fd(600)
	bd.lt(90)
bd.hideturtle()
# border has been created

# this forms a triangle used as the pilot(the ship) for now
pilot = turtle.Turtle()
pilot.color("blue")
pilot.shape("triangle")
pilot.penup()
pilot.speed(0)
pilot.setposition(0,-250)
pilot.setheading(90)
# end formation of pilot triangle

moverate = 10			# our pilots move rate
fmr = 5				#fighter move rate
misslerate = 25			# move speed of missle

# fighter is the enemy
fighter = turtle.Turtle()
fighter.color("green")
fighter.shape("circle")
fighter.penup()
fighter.speed(0)
fighter.setposition(-200,250)

# missle for pilot
missle = turtle.Turtle()
missle.shape("triangle")
missle.color("orange")
missle.penup()
missle.speed(0)
missle.setheading(90)
missle.shapesize(0.5,0.5)
missle.hideturtle()
misslecon = "ready"	# missle condition



# functions for pilots movement

def shoot():
	global misslecon
	if misslecon == "ready":
		misslecon = "shot"
		missle.setposition(pilot.xcor(), pilot.ycor() + 10)
		missle.showturtle()
def go_up():
	if pilot.ycor() + moverate > 270:
		pilot.sety(280)
	else:
		pilot.sety(pilot.ycor() + moverate)
def go_down():
	if pilot.ycor() - moverate < -270:
		pilot.sety(-280)
	else:
		pilot.sety(pilot.ycor() - moverate)

def go_left():
	if pilot.xcor() - moverate < -280:
		pilot.setx(-280)
	else:
		pilot.setx(pilot.xcor() - moverate)
def go_right():
	if pilot.xcor() + moverate > 280:
		pilot.setx(280)
	else:
		pilot.setx(pilot.xcor() + moverate)
# hotkeys
turtle.listen()
turtle.onkeypress(shoot, "space")
turtle.onkeypress(go_up, "Up")
turtle.onkeypress(go_down, "Down")
turtle.onkeypress(go_left, "Left")
turtle.onkeypress(go_right, "Right")

# loop for game

while True:
	fighter.setx(fighter.xcor() + fmr)
	if fighter.xcor() > 280:
		fighter.sety(fighter.ycor() - 20)
		fmr = fmr * -1
	if fighter.xcor() < -280:
		fighter.sety(fighter.ycor() - 20)
		fmr = fmr * -1

	#if misslecon == "shot":
	missle.sety(missle.ycor() + misslerate)
	if missle.ycor()  > 280:
		missle.hideturtle()
		misslecon = "ready"

# allow for indefinite window
time = input()
