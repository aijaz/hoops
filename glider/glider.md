# Glider

In this final project we're gonna make a game similar to the
[Glider Game from 1988](https://www.youtube.com/watch?v=X33q-GT-e5k). 

The goal of this game is to navigate your glider through a series of rooms
and have it exit the house. The force of gravity keeps pulling your glider 
towards the floor, but the vents in the floor give it a push upwards. Your
only control is the left arrow button that slows the glider when it's above 
a vent, allowing it to rise higher than it normally would. There are several
obstacles like shelves, tables, clocks, and the floor itself. Every time your
glider hits one of these obstacles, it loses one 'life.' Each room has coins
that you can collect to get more points.

# 1 Create the basic game

## 1.1 Create a new project

- Create a new project named `glider`
- Just like you did last week with the `hoops` program, 
  go to Settings -> Python Interpreter, and install the `arcade` package.
  - If you can't install the `arcade` package for any reason (like, no internet)
    then just work in the `hoops` package from last week.

## 1.2 Download the sprite images

Download the following three images into your project directory:

- [glider_left.png](../glider_left.png) ![Glider facing left](../glider_left.png)
- [glider_right.png](../glider_right.png) ![Glider facing right](../glider_right.png)
- [vent.png](../vent.png) ![Vent](../vent.png)

## 1.3 Create the first version of your app

Create a new file named `glider.py` and copy the following code to it:
```python
"""
Glider Platformer Game

"""
import arcade

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Glider"

# Setting gravity to a really small value because we want the glider to fall gently
GRAVITY = 0.02

# The amount to jump when the glider is over a vent
VENT_JUMP = 3

# How high the floor is from the base of the viewport
FLOOR_Y = 60


```
Make sure you read the comments and understand them. 

Our game will have 4 views:
- `IntroView` - A splash screen before you start the app
- `GameView` - Our main game-playing view
- `GameOverView` - A view that's displayed when you lose all your 'lives'
- `YouWonView` - A view that's displayed when you successfully complete all levels

Now create the GameView class
```python
class GameView(arcade.View):
    """
    Main game-playing view
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        # Load the default texture (image) of the glider 
        # A texture is an image file that's used to display a sprite.
        # A sprite can have many textures, but only displays one at a time.
        self.player_texture = arcade.load_texture("glider_right.png")

        # The main player sprite
        self.glider = arcade.Sprite(self.player_texture)
        
        # Position the sprite near the center of the screen
        self.glider.center_x = 600
        self.glider.center_y = 500

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        arcade.draw_sprite(self.glider)


```
As always, make sure you read the comments and understand all the code in here. 
Don't hesitate to ask any questions if you don't. 

Finally, add the main function:
```python
def main():
    """ Main function """
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    start_view = GameView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


# This is a common idiom in python
# __name__ is the name of the python module that is being run
# When the current file is run from the command 
# line, __name__ has the value "__main__"
if __name__ == "__main__":
    main()
```

Run the app. If you get any errors, ask for help. 

You should see a screen like this:
<img alt='1.png' width=696 height=430 src="1.png">

You can find the full file as it's supposed to look at the end of this step [here](1.py).

# 2 Working With Textures

## 2.1 Simplify our code

Before we start loading our second texture, let's simplify how we load our 
first texture. We can combine 2 lines of code to 1. In `GameView.__init__`
change these 7 lines
```python
        # Load the default texture (image) of the glider 
        # A texture is an image file that's used to display a sprite.
        # A sprite can have many textures, but only displays one at a time.
        self.player_texture = arcade.load_texture("glider_right.png")

        # The main player sprite
        self.glider = arcade.Sprite(self.player_texture)
```
to 
```python
        self.glider = arcade.Sprite(arcade.load_texture("glider_right.png"))
```
## 2.2 Load the second texture

Then, add the following line _after_ the one you just added above:
```python
        self.glider.append_texture(arcade.load_texture("glider_left.png"))
```

This instructs arcade to associate 2 textures with the `self.glider` sprite. 
The first texture (the one facing right) is number `0` and the second is number 
`1`.

## 2.3 Respond to key presses. 

Add the following simple implementation of `on_key_press` to the bottom
of your GameView class definition (after the `on_draw` method). 

This method relies on the variable `self.glider_direction` to keep track
of which direction the glider is pointing. 
```python
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT:
            if self.glider_direction == 'left':
                self.glider_direction = 'right'
                self.glider.set_texture(0)
        elif symbol == arcade.key.LEFT:
            if self.glider_direction == 'right':
                self.glider_direction = 'left'
                self.glider.set_texture(1)
```

## 2.4 Initialize `self.glider_direction`

Since we access `self.glider_direction` we have to make sure it always has a 
valid value. When we start the app, the glider points left, so we set this
variable in `GameView.setup`.

In `GameView.setup` change this line
```python
        pass
```
to
```python
        self.glider_direction = 'right'
```

## 2.5 Define `self.glider_direction`

Finally, add this line to the bottom of `GameView.__init__`. It will define the
`glider_direction` attribute without assigning a direction to it yet. 
```python
        self.glider_direction = None
```
Now, when you run the program the glider will change direction depending on 
which arrow key you press. 

You can find the full file as it's supposed to look at the end of this step [here](2.py).

# 3 Creating our first vent

Vents are special sprites in our game. They affect our `glider` sprite from afar.
Our glider doesn't need to collide with a vent to be affected by its presence. 
Every time our glider is above a vent it gets a vertical push. Because our vents
are special, we won't put them in the sprite list that contains sprites that 
our glider will collide with—we'll create a separate sprite list for vents.

## 3.1 Create our first vent and put it in a SpriteList

Add the following to the bottom of `GameView.__init__`
```python

        # create vents        
        self.vents = arcade.SpriteList()
        v = arcade.Sprite("vent.png")
        v.center_x = 800
        v.center_y = 60
        self.vents.append(v)
```

## 3.2 Draw our vents

Add the following to the bottom of `GameView.on_draw`
```python

        # Draw vents
        self.vents.draw()
```

You should see a screen like this:
<img alt='3.png' width=696 height=430 src="3.png">

You can find the full file as it's supposed to look at the end of this step [here](3.py).

# 4 Our First Obstacle - The Dreaded Floor

Now it's time to create the obstacles that cause us to "lose a life." The first
obstacle is the floor. If the glider touches the floor, we lose a life.

## 4.1 Create the `obstacles` sprite list and add the floor to it

Add the following code to the bottom of `GameView.__init__`. Remember - the 
x location is the location of the _center_ of the floor, so it has a value
of `WINDOW_WIDTH/2`. For now, we'll draw the floor. Later on, we'll make it
transparent. 
```python

        # create the obstacles sprite list
        self.obstacles = arcade.SpriteList()
        
        # create the floor
        floor = arcade.SpriteSolidColor(width=WINDOW_WIDTH, 
                                        height=4,
                                        center_x=WINDOW_WIDTH/2,
                                        center_y=FLOOR_Y,
                                        color=arcade.color.BLACK)
        
        # add the floor to the obstacles list
        self.obstacles.append(floor)
```

## 4.2 Draw the floor

Add the following to the bottom of `GameView.on_draw`
```python
        
        # Draw obstacles
        self.obstacles.draw()
```

You should see a screen like this:
<img alt='4.png' width=696 height=430 src="4.png">

You can find the full file as it's supposed to look at the end of this step [here](4.py).

```python
```

```python
```

```python
```

```python
```

```python
```

```python
```

```python
```

```python
```

```python
```

```python
```
