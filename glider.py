"""
Platformer Game

python -m arcade.examples.platform_tutorial.02_draw_sprites
"""
from turtledemo.nim import SCREENWIDTH

import arcade
from pyglet.event import EVENT_HANDLE_STATE
from pyglet.graphics import Batch

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"
GRAVITY = 0.02
JUMP_SPEED = 0
VENT_JUMP = 3
FLOOR_Y = 60


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        # Separate variable that holds the player sprite
        self.glider = arcade.Sprite(arcade.load_texture("glider_right.png"), scale=0.5)
        self.glider.append_texture(arcade.load_texture("glider_left.png"))

        self.vents = arcade.SpriteList(use_spatial_hash=True)
        self.obstacles = arcade.SpriteList()
        self.coins = arcade.SpriteList(use_spatial_hash=True)

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        self.floor = arcade.SpriteSolidColor(WINDOW_WIDTH,
                                             1,
                                             WINDOW_WIDTH / 2,
                                             FLOOR_Y,
                                             arcade.color.BLACK)
        self.obstacles.append(self.floor)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.glider, walls=None, gravity_constant=GRAVITY
        )

        self.cur_key_press = None
        self.currently_over_vent = False
        self.glider_direction = 'right'
        self.vent_count = None
        self.level = None
        self.lives = None
        self.score = None
        self.level_constraints = self.load_level_constraints()

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.glider_direction = 'right'
        self.glider.set_texture(0)
        self.glider.change_x = 3
        self.glider.change_y = 0
        self.cur_key_press = None
        self.currently_over_vent = False
        self.vent_count = 0
        self.level = 1
        self.lives = 3
        self.score = 0

    def on_update(self, delta_time: float) -> bool | None:
        """Movement and Game Logic"""

        # Move the player using our physics engine
        self.physics_engine.update()

        if self.cur_key_press == arcade.key.LEFT:
            self.glider.center_x -= self.glider.change_x * 0.9  # apply brakes
            self.vent_count += 1
            if self.vent_count == 4:
                self.vent_count = 0
                if self.glider_direction == 'left':
                    self.glider_direction = 'right'
                    self.glider.set_texture(0)
                else:
                    self.glider_direction = 'left'
                    self.glider.set_texture(1)

        still_over_vent = False
        for vent in self.vents:
            if abs(vent.center_x - self.glider.center_x) < vent.width:
                self.glider.change_y = VENT_JUMP
                self.currently_over_vent = True
                still_over_vent = True
                break

        # If we get off the vent
        if self.currently_over_vent and not still_over_vent:
            self.currently_over_vent = False
            self.glider.change_y = 0

        if self.glider.center_x >= WINDOW_WIDTH:
            self.handle_new_level()

        coin_hit_list = arcade.check_for_collision_with_list(self.glider, self.coins)

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        obstacles_hit = arcade.check_for_collision_with_list(self.glider, self.obstacles)
        if obstacles_hit:
            self.lose_life()

    def handle_new_level(self):
        if self.level == len(self.level_constraints):
            self.you_won()
            return
        self.level += 1
        self.setup_level()

    def you_won(self):
        you_won_view = YouWonView()
        self.window.show_view(you_won_view)

    def lose_life(self):
        if self.lives == 0:
            return
        self.lives -= 1

        if self.lives == 0:
            self.game_over()
        else:
            self.setup_level()

    def game_over(self):
        game_over_view = GameOverView()
        self.window.show_view(game_over_view)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw vents
        self.vents.draw()
        self.obstacles.draw()
        self.coins.draw()

        # Draw our sprites
        arcade.draw_sprite(self.glider)

        batch = Batch()
        text = arcade.Text(f"Level: {self.level} Lives: {self.lives} Score: {self.score}",
                           WINDOW_WIDTH - 10,
                           40,
                           batch=batch,
                           color=arcade.color.BLACK,
                           font_size=18,
                           anchor_x='right')
        batch.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.LEFT and self.currently_over_vent:
            self.cur_key_press = arcade.key.LEFT
            if self.glider_direction == 'right':
                self.glider_direction = 'left'
                self.glider.set_texture(1)
        elif symbol == arcade.key.UP:
            self.glider.change_y = JUMP_SPEED
        elif symbol == arcade.key.ESCAPE:
            self.setup()
            self.setup_level()

    def on_key_release(self, symbol: int, modifiers: int) -> EVENT_HANDLE_STATE:
        self.cur_key_press = None
        if symbol == arcade.key.LEFT:
            self.glider_direction = 'right'
            self.glider.set_texture(0)

    def setup_level(self):
        self.glider.center_x = 0
        self.glider.change_y = 0
        self.obstacles.clear()
        self.obstacles.append(self.floor)
        self.vents.clear()
        self.coins.clear()
        data = self.level_constraints[self.level - 1]
        self.glider.center_y = data["glider_y"]
        for x in data["vent_x"]:
            v = arcade.Sprite("vent.png", scale=0.3)
            v.center_x = x
            v.center_y = 60
            self.vents.append(v)
        for x, y in data["coin_xy"]:
            coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.25)
            coin.center_x = x
            coin.center_y = y
            self.coins.append(coin)
        for x, y, w, h in data["shelf_xywh"]:
            shelf = arcade.SpriteSolidColor(w, h, x, y, arcade.color.WHITE)
            self.obstacles.append(shelf)

    def load_level_constraints(self):
        return [
            {
                "glider_y": 500,
                "vent_x": [650, 950],
                "coin_xy": [(384, 300), (640, 350), (900, 500)],
                "shelf_xywh": []
            },
            {
                "glider_y": 500,
                "vent_x": [300, 850],
                "coin_xy": [(384, 300), (640, 350), (900, 500)],
                "shelf_xywh": [(800, 400, SCREENWIDTH / 2, 4)]
            },
        ]


class GameOverView(arcade.View):
    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.window.background_color = arcade.csscolor.DARK_SLATE_BLUE

    def on_draw(self):
        """ Draw this view """
        self.clear()
        batch = Batch()
        text_1 = arcade.Text("Game Over",
                             self.window.width / 2,
                             self.window.height / 2,
                             batch=batch,
                             color=arcade.color.WHITE,
                             font_size=50,
                             anchor_x='center')

        text_2 = arcade.Text("Press any Key to Restart",
                             self.window.width / 2,
                             self.window.height / 2 - 75,
                             batch=batch,
                             color=arcade.color.WHITE,
                             font_size=50,
                             anchor_x='center')

        batch.draw()

    def on_key_press(self, symbol, modifiers):
        """ If the user presses the mouse button, start the game. """
        start_view = GameView()
        start_view.setup()
        start_view.setup_level()
        self.window.show_view(start_view)


class YouWonView(arcade.View):
    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.window.background_color = arcade.csscolor.DARK_SLATE_BLUE

    def on_draw(self):
        """ Draw this view """
        self.clear()
        batch = Batch()
        text_1 = arcade.Text("You Made It!",
                             self.window.width / 2,
                             self.window.height / 2,
                             batch=batch,
                             color=arcade.color.WHITE,
                             font_size=50,
                             anchor_x='center')

        batch.draw()

    def on_key_press(self, symbol, modifiers):
        """ If the user presses the mouse button, start the game. """
        start_view = GameView()
        start_view.setup()
        start_view.setup_level()
        self.window.show_view(start_view)


def main():
    """ Main function """
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    start_view = GameView()
    start_view.setup()
    start_view.setup_level()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
