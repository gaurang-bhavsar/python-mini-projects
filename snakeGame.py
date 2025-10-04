import turtle
import time
import random

# --- 1. Setup the Screen ---
# Set the delay for the game's speed (lower is faster)
delay = 0.1 

# Score
score = 0
high_score = 0

# Set up the screen
wn = turtle.Screen()
wn.title("Classic Snake Game")
wn.bgcolor("light blue")
wn.setup(width=600, height=600)
wn.tracer(0) # Turns off the screen updates for smooth animation

# --- 2. Create the Snake Head ---
head = turtle.Turtle()
head.speed(0) # Animation speed (fastest)
head.shape("square")
head.color("black")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# --- 3. Create the Food ---
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# List to hold the snake's body segments
segments = []

# --- 4. Create the Scoreboard Pen ---
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# --- 5. Functions to Control Direction ---
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# --- 6. Keyboard Bindings ---
wn.listen()
wn.onkey(go_up, "Up")      # Arrow keys for movement
wn.onkey(go_down, "Down")
wn.onkey(go_left, "Left")
wn.onkey(go_right, "Right")
# You can also use WASD:
wn.onkey(go_up, "w")
wn.onkey(go_down, "s")
wn.onkey(go_left, "a")
wn.onkey(go_right, "d")

# --- 7. Main Game Loop ---
while True:
    wn.update() # Refresh the screen

    # Check for **Border Collision**
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1) # Pause the game
        head.goto(0, 0)
        head.direction = "stop"
        
        # Hide the segments and clear the list
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()
        
        # Reset score and delay
        score = 0
        delay = 0.1
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), 
                  align="center", font=("Courier", 24, "normal"))

    # Check for **Food Collision** (distance between head and food is less than 20 pixels)
    if head.distance(food) < 20:
        # Move the food to a random spot
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        # Add a new segment to the snake
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

        # Increase the score
        score += 10
        if score > high_score:
            high_score = score

        # Update the score display
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), 
                  align="center", font=("Courier", 24, "normal"))

    # Move the snake body segments
    # The last segment moves to the position of the second-to-last, and so on.
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 (the one right behind the head) to the head's position
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # Check for **Self-Collision** (Head collides with any body segment)
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1) # Pause the game
            head.goto(0, 0)
            head.direction = "stop"
            
            # Hide the segments and clear the list
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()

            # Reset score
            score = 0
            delay = 0.1
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), 
                      align="center", font=("Courier", 24, "normal"))

    time.sleep(delay)

wn.mainloop()
