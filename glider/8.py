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


class GameView(arcade.View):
    """
    Main game-playing view
    """

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

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.glider_direction = 'right'
        self.lives = 3
        self.setup_level()


    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        arcade.draw_sprite(self.glider)

        # Draw vents
        self.vents.draw()

        # Draw obstacles
        self.obstacles.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT:
            if self.glider_direction == 'left':
                self.glider_direction = 'right'
                self.glider.set_texture(0)
        elif symbol == arcade.key.LEFT:
            if self.glider_direction == 'right':
                self.glider_direction = 'left'
                self.glider.set_texture(1)

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

    def setup_level(self):
        # Position the sprite near the center of the screen
        self.glider.center_x = 600
        self.glider.center_y = 500
        self.glider.change_x = 3
        self.glider.change_y = 0


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
