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

# 5 Using a Physics Engine

As we saw in our `hoops` app, it gets tedious managing all of the Newtonian physics
even for a simple game. This time we will offload this to the simple
`PhysicsEnginePlatformer` Physics Engine. 

## 5.1 Create the physics engine

Add the following code to the bottom of `GameView.__init__` 

```python

        # create the physics engine
        # don't specify any walls, because every collision is either 'fatal'
        # or a coin-collection
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.glider, walls=None, gravity_constant=GRAVITY
        )
```

## 5.2 Let the Physics Engine do its thing

The physics engine will calculate the new state of all sprites depending on all 
the forces acting upon them (including, of course, the force of gravity). Now it's 
time for us to implement `GameView.on_update`. In this method, the physics engine
will update its state. 

Add the following to the bottom of your `GameView` class.

```python

    def on_update(self, delta_time):
        """Movement and Game Logic"""

        # Move the player using our physics engine
        self.physics_engine.update()
```
As you can see, gravity is the only force acting on our glider right now, 
and the glider has no horizontal velocity, so it falls straight down, through the floor.
We'll fix this soon. 

You can find the full file as it's supposed to look at the end of this step [here](5.py).

# 6 Check for Collisions

Now it's time to start checking for collisions and introducing the concepts of
'lives' and 'game over'. 

## 6.1 Initialize the number of lives we have in this game

Add the following to the bottom of `GameView.__init__`
```python

        self.lives = None
```
Then add the following to the bottom of `GameView.setup`
```python
        self.lives = 3
```
## 6.2 Check for Collisions

Now that we have the concept of lives, we need to 'lose a life' every time
the glider collides with something. Add the following to the bottom of 
`GameView.on_update`. 
```python

        # check for collisions
        obstacles_hit = arcade.check_for_collision_with_list(self.glider, self.obstacles)
        
        # if the obstacles_hit list is not empty
        if obstacles_hit:
            self.lose_life()
```

## 6.3 Implement `lose_life`

Every time the glider collides with something the `lose_life` method is called. Now it's
time for us to implement this method. Add the following code to the bottom of the
`GameView` class:
```python

    def lose_life(self):
        if self.lives == 0:
            return
        self.lives -= 1

        if self.lives == 0:
            # if we're down to zero lives left, call game_over()
            self.game_over()
        else:
            self.setup_level()

    def game_over(self):
        print("Game Over")
```

## 6.4 Restart from the starting point

Every time we lose a life we want to start from the beginning location. Eventually,
when we have levels, we want to restart the current level but for now we just want to
make sure we restart at the beginning location. 

Find these lines in `GameView.__init__`. We're gonna move them to a new
method called `GameView.setup_level` that restarts the level
Delete thse lines.
```python

        # Position the sprite near the center of the screen
        self.glider.center_x = 600
        self.glider.center_y = 500
```
Now create a method named `setup_level`. Paste this at the bottom of your `GameView`
class
```python
    def setup_level(self):
        # Position the sprite near the center of the screen
        self.glider.center_x = 600
        self.glider.center_y = 500
        self.glider.change_x = 0
        self.glider.change_y = 0
```
## 6.5 Stop everything if the game is over

Finally, you want the game to not do anything if the game is over. Insert the following
code to the _beginning_ of `GameView.on_update`:

```python
        
        # Don't do anything if the game is over
        if self.lives == 0:
            return
```
So, after this, `GameView.on_update` should look like this:

```python
    def on_update(self, delta_time):
        """Movement and Game Logic"""

        # Don't do anything if the game is over
        if self.lives == 0:
            return

        # Move the player using our physics engine
        self.physics_engine.update()

        # check for collisions
        obstacles_hit = arcade.check_for_collision_with_list(self.glider, self.obstacles)

        # if the obstacles_hit list is not empty
        if obstacles_hit:
            self.lose_life()
```
Now that this is done, you should see that the glider falls 3 times, and then 
the game is over.

You can find the full file as it's supposed to look at the end of this step [here](6.py).

# 7 Moving Forward

We want our glider to move forward at a constant speed. This is easy to do with
our physics engine. Change `self.glider.change_x = 0` to `self.glider.change_x = 3` 
in `GameView.setup_level()`. That's it:

```python
    def setup_level(self):
        # Position the sprite near the center of the screen
        self.glider.center_x = 600
        self.glider.center_y = 500
        self.glider.change_x = 3
        self.glider.change_y = 0
```
You can find the full file as it's supposed to look at the end of this step [here](7.py).

# 8 Cleaning up the Visuals

Now let's clean up the images a bit. First, let's make the floor transparent. 
Add the following line immediately after you create self.floor in `GameView.__init__`

```python
        self.floor.alpha = 0
```
Also in init, add `, scale=0.5` to the line where you create `self.glider`. This scales the glider down, and makes it smaller. 
Similarly, add `, scale=0.3` to the line where you create the vent `v`. 
So now, the `__init__` method should look like this:

```python
    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        self.glider = arcade.Sprite(arcade.load_texture("glider_right.png"), scale=0.5)
        self.glider.append_texture(arcade.load_texture("glider_left.png"))

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.glider_direction = None

        # create vents
        self.vents = arcade.SpriteList()
        v = arcade.Sprite("vent.png", scale=0.3)
        v.center_x = 800
        v.center_y = 60
        self.vents.append(v)

        # create the obstacles sprite list
        self.obstacles = arcade.SpriteList()

        # create the floor
        floor = arcade.SpriteSolidColor(width=WINDOW_WIDTH,
                                        height=4,
                                        center_x=WINDOW_WIDTH/2,
                                        center_y=FLOOR_Y,
                                        color=arcade.color.BLACK)
        floor.alpha = 0

        # add the floor to the obstacles list
        self.obstacles.append(floor)

        # create the physics engine
        # don't specify any walls, because every collision is either 'fatal'
        # or a coin-collection
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.glider, walls=None, gravity_constant=GRAVITY
        )

        self.lives = None
```

You can find the full file as it's supposed to look at the end of this step [here](8.py).

# 9 Interacting with the Vents

Now it's time for the glider to interact with the vents. 

## 9.1 Give the glider a boost above the vents

If the glider is above a vent, its `change_y` should be set to a positive number, so it moves up. Eventually, the force of 
gravity in the physics engine will move it back down. 

Add the following to the end of `GameView.__init__`
```python

        # This variable indicates whether the glider is currently over a vent or not
        self.currently_over_vent = False
```
We also want to reset this variable in `setup_level`, so add this to the bottom of `setup_level` 
```python

        self.currently_over_vent = False
```
Then add the following to the bottom of `GliderView.on_update`
```python

        still_over_vent = False
        glider_was_over_vent_before = self.currently_over_vent
        for vent in self.vents:
            # If the glider is above the vent (the distance from the vent's center to the glider's center is 
            # less than the vent's width)
            if abs(vent.center_x - self.glider.center_x) < vent.width:
                self.currently_over_vent = True
                self.glider.change_y = VENT_JUMP  # give the glider a boost
                if not glider_was_over_vent_before:
                    # play the jump sound
                    arcade.sound.play_sound(self.jump_sound)
                still_over_vent = True
                # We don't need to check all vents. Stop after you find one that the glider is over.
                break
                
        # If we get off the vent
        if glider_was_over_vent_before and not still_over_vent:
            self.currently_over_vent = False
            self.glider.change_y = 0  # stop the glider from rising further after it leaves the vent
```
Look over that code, and make sure you understand it. Ask your instructor if you have any questions. You can see that 
the code plays a sound the first time the glider goes over a vent. Let's create that sound now. Add the following lines
to the bottom of `GameView.__init__`
```python

        # sound to be played when we collect a coin
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav") 

        # sound to be played when the glider goes over a vent
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
```

## 9.2 Slowing Down over the Vents

Now we need to allow the glider to slow down its horizontal velocity over the vents, 
allowing it to rise higher than normal. The way to do this is to press the left 
arrow key to slow down the movement to the right. We'll also make the glider
oscillate between pointing left and pointing right while it's slowing down - to
give us a visual queue about what's happening. 

Arcade only informs us when a key is pressed or released. We have to keep track of
which key is pressed. We can have more than one key pressed at a time, but for this
game there is only one key that we need to press - the left arrow key. Think 
of this key as a brake. We'll track which key is pressed in a variable 
named `current_key_press`. 

Add the following to the bottom of `GameView.__init__`:

```python

        # track what key is currently being pressed
        self.current_key_press = None

        # track which direction the glider is currently facing
        self.glider_direction = 'right'
```
Then modify `GameView.on_key_press` to look like this:
```python
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT and self.currently_over_vent:
            # only handle the press of the LEFT arrow key if the glider is over a vent
            self.current_key_press = arcade.key.LEFT
            # Only change the texture if we need to - don't do unnecessary work
            if self.glider_direction == 'right':  # pointing to the right
                self.glider_direction = 'left'
                self.glider.set_texture(1)
```
Then, immediately below that, add `on_key_release`
```python

    def on_key_release(self, symbol, modifiers):
        self.current_key_press = None
        if symbol == arcade.key.LEFT:
            # switch back to the old texture
            self.glider.set_texture(0)
            self.glider_direction = 'right'
```
Now we need to "apply the brakes." This will be done in `GameView.on_update` 
Add the following to to bottom on `GameView.on_update`
```python

        if self.current_key_press == arcade.key.LEFT:
            self.glider.center_x -= self.glider.change_x * 0.9  # apply brakes
            # The physics engine already moved the glider to the right. 
            # Move it 90% of the way back
            
            # swap out the texture
            if self.glider_direction == 'right':
                self.glider_direction = 'left'
                self.glider.set_texture(1)
            else:
                self.glider_direction = 'right'
                self.glider.set_texture(0)
```

You can find the full file as it's supposed to look at the end of this step [here](9.py).

# 10 Slowing down the oscillation

When you run the game you can see that the oscillation is really fast. This is
because we're changing the orientation of the glider in `on_update` which is called 
as often as 30 times a second. So we need to slow it down. Let's try changing the
glider_direction every 4th invocation of `on_update`.

Add the following global variable to the top of your file, under `FLOOR_Y`:
```python

# How many calls to on_update to ignore before switching directions
DIRECTION_DELAY = 4
```
Add the following to the bottom of `GameView.__init__`:
```python

        # How many calls to on_update have we skipped
        self.direction_count = 0
```
Change the following code in `on_update`
```python
            # swap out the texture
            if self.glider_direction == 'right':
                self.glider_direction = 'left'
                self.glider.set_texture(1)
            else:
                self.glider_direction = 'right'
                self.glider.set_texture(0)
```
to
```python
            # swap out the texture
            self.direction_count += 1
            if self.direction_count == 4:
                # Only swap directions when on every 4th attempt
                self.direction_count = 0
                if self.glider_direction == 'right':
                    self.glider_direction = 'left'
                    self.glider.set_texture(1)
                else:
                    self.glider_direction = 'right'
                    self.glider.set_texture(0)
```
Now the direction change is a lot slower.

You can find the full file as it's supposed to look at the end of this step [here](10.py).

```python
```

```python
```
```python
```

```python
```
