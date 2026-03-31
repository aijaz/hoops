"""
Glider Platformer Game

"""
import arcade
from pyglet.graphics import Batch

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
        self.floor = arcade.SpriteSolidColor(width=WINDOW_WIDTH,
                                             height=4,
                                             center_x=WINDOW_WIDTH / 2,
                                             center_y=FLOOR_Y,
                                             color=arcade.color.BLACK)
        self.floor.alpha = 0

        # add the floor to the obstacles list
        self.obstacles.append(self.floor)

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

        # The current score
        self.score = 0

        # The sprite list containing coins
        self.coins = arcade.SpriteList(use_spatial_hash=True)

        # Lose a life sound
        self.life_sound = arcade.load_sound(":resources:sounds/explosion2.wav")

        # Game Over sound
        self.game_over_sound = arcade.load_sound(":resources:sounds/gameover5.wav")

        # The current level of the game
        self.current_level = 1

        # The data for each level
        self.levels = self.get_levels()

        # create the drawings and images sprite lists
        self.drawings = arcade.SpriteList()
        self.images = arcade.SpriteList()

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

        # Draw coins
        self.coins.draw()

        # print the score
        self.print_score()

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
            self.glider.center_x -= self.glider.change_x * 0.9  # apply brakes
            # The physics engine already moved the glider to the right.
            # Move it 90% of the way back

            # swap out the texture
            self.direction_count += 1
            if self.direction_count >= 4:
                # Only swap directions when on every 4th attempt
                self.direction_count = 0
                if self.glider_direction == 'right':
                    self.glider_direction = 'left'
                    self.glider.set_texture(1)
                else:
                    self.glider_direction = 'right'
                    self.glider.set_texture(0)

        # Check for collision with coins
        coin_hit_list = arcade.check_for_collision_with_list(self.glider, self.coins)

        # Play a sound if we collect one or more coins
        if coin_hit_list:
            arcade.sound.play_sound(self.collect_coin_sound)

        # For each coin we collect, remove it from the sprite list and increase our score by 100
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 100

        # if the glider has gone off the right edge of the screen
        if self.glider.center_x >= WINDOW_WIDTH:
            self.handle_new_level()

    def lose_life(self):
        if self.lives == 0:
            return
        self.lives -= 1

        if self.lives == 0:
            # if we're down to zero lives left, call game_over()
            self.game_over()
            arcade.sound.play_sound(self.game_over_sound)
        else:
            arcade.sound.play_sound(self.life_sound)
            self.setup_level()

    def game_over(self):
        print("Game Over")

    def setup_level(self):
        # Initialize the key state variables
        self.glider.change_x = 3
        self.glider.change_y = 0
        self.currently_over_vent = False
        self.glider.center_x = 0

        # clear all sprite lists
        self.obstacles.clear()
        self.obstacles.append(self.floor)
        self.vents.clear()
        self.coins.clear()
        self.drawings.clear()
        self.images.clear()

        # load the data for the current level
        data = self.levels[self.current_level - 1]  # don't forget the -1 here!

        # now set the variables based on the data
        self.glider.center_y = data.get("glider_y", 600)  # default center_y is 600

        # create the images first, since they're in the background
        for x, y, p in data.get("shelf_xyp", []):  # if this key is not present, iterate over an empty list
            image = arcade.Sprite(p)
            image.center_x = x
            image.center_y = y
            self.images.append(image)   # append each image to the image sprite list

        # create the vents
        for x in data.get("vent_x", []):
            v = arcade.Sprite("vent.png", scale=0.3)
            v.center_x = x
            v.center_y = 60
            self.vents.append(v)  # append each vent to the vent sprite list

        # create the coins
        for x, y in data.get("coin_xy", []):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.25)
            coin.center_x = x
            coin.center_y = y
            self.coins.append(coin)  # append each coin to the coin sprite list

        for x, y, w, h in data.get("shelf_xywh", []):
            shelf = arcade.SpriteSolidColor(w, h, x, y, arcade.color.BLACK)
            self.obstacles.append(shelf)   # append each shelf to the shelf sprite list

        for x, y, w, h in data.get("drawing_xywh", []):
            drawing = arcade.SpriteSolidColor(w, h, x, y, arcade.color.BLACK)
            self.drawings.append(drawing)   # append each drawing to the drawing sprite list

    def print_score(self):
        batch = Batch()
        text = arcade.Text(f"Level: {self.current_level} Lives: {self.lives} Score: {self.score}",
                           WINDOW_WIDTH - 10,
                           40,
                           batch=batch,
                           color=arcade.color.BLACK,
                           font_size=18,
                           anchor_x='right')
        batch.draw()

    def get_levels(self):
        return [
            {
                "glider_y": 500,
                "vent_x": [650, 950],
                "coin_xy": [(384, 300), (640, 350), (900, 500)],
                "shelf_xywh": [],
                "drawings_xywh": [],
                "images_xyp": []
            },
            {
                "glider_y": 200,
                "vent_x": [150, 950],
                "coin_xy": [],
                "shelf_xywh": [],
            },
            {
                "glider_y": 500,
                "vent_x": [300, 850],
                "coin_xy": [(384, 300), (640, 350), (900, 500)],
                "shelf_xywh": [(800, 400, 400, 4)],
                "drawings_xywh": [(800, 230, 2, 340)],
            },
            {
                "glider_y": 500,
                "vent_x": [650, 950],
                "coin_xy": [(384, 300), (640, 350), (900, 500)],
                "shelf_xywh": [],
                "spinner_xywh": [(800, 300, 400, 8)]
            },
        ]

    # Update and set up the new level, or display the "you won" message
    def handle_new_level(self):
        if self.current_level == len(self.levels):
            self.you_won()
            return
        self.current_level += 1
        self.setup_level()

    def you_won(self):
        print("You won!")

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
