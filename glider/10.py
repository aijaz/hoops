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

# How many calls to on_update to ignore before switching directions
DIRECTION_DELAY = 4


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
                                        center_x=WINDOW_WIDTH / 2,
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

        # This variable indicates whether the glider is currently over a vent or not
        self.currently_over_vent = False

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        # track what key is currently being pressed
        self.current_key_press = None

        # track which direction the glider is currently facing
        self.glider_direction = 'right'

        # How many calls to on_update have we skipped
        self.direction_count = 0

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
        if symbol == arcade.key.LEFT and self.currently_over_vent:
            # only handle the press of the LEFT arrow key if the glider is over a vent
            self.current_key_press = arcade.key.LEFT
            # Only change the texture if we need to - don't do unnecessary work
            if self.glider_direction == 'right':  # pointing to the right
                self.glider_direction = 'left'
                self.glider.set_texture(1)

    def on_key_release(self, symbol, modifiers):
        self.current_key_press = None
        if symbol == arcade.key.LEFT:
            # switch back to the old texture
            self.glider.set_texture(0)
            self.glider_direction = 'right'

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

        if self.current_key_press == arcade.key.LEFT:
            print(f"HERE {self.glider_direction=}")
            self.glider.center_x -= self.glider.change_x * 0.9  # apply brakes
            # The physics engine already moved the glider to the right.
            # Move it 90% of the way back

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
        self.currently_over_vent = False


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
