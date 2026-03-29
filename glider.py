"""
Platformer Game

python -m arcade.examples.platform_tutorial.02_draw_sprites
"""
import arcade
from pyglet.event import EVENT_HANDLE_STATE

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"
GRAVITY = 0.02
JUMP_SPEED = 0
VENT_JUMP = 3


class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        # Separate variable that holds the player sprite
        self.glider = arcade.Sprite(arcade.load_texture("glider_right.png"), scale=0.5)
        self.glider.append_texture(arcade.load_texture("glider_left.png"))

        self.vents = arcade.SpriteList(use_spatial_hash=True)
        self.obstacles = arcade.SpriteList()
        self.coins = arcade.SpriteList(use_spatial_hash=True)

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        self.floor = arcade.SpriteSolidColor(WINDOW_WIDTH, 1, WINDOW_WIDTH/2, 60, arcade.color.BLACK)
        self.obstacles.append(self.floor)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.glider, walls=self.obstacles, gravity_constant=GRAVITY
        )

        self.cur_key_press = None
        self.currently_over_vent = False
        self.glider_direction = 'right'
        self.vent_count = None
        self.level = None
        self.lives = None
        self.score = None

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

        obstacles_hit = arcade.check_for_collision_with_list(self.glider, self.obstacles)
        coin_hit_list = arcade.check_for_collision_with_list(self.glider, self.coins)

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1
            print(f"Score: {self.score}")

        if self.physics_engine.can_jump():
            self.lose_life()

    def handle_new_level(self):
        self.level += 1
        print(f"Level {self.level}")
        self.setup_level()

    def lose_life(self):
        if self.lives == 0:
            return
        self.lives -= 1
        print(f"Lives: {self.lives}")
        if self.lives == 0:
            self.game_over()

    def game_over(self):
        print("Game Over")
        self.glider.change_x = 0

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
        self.obstacles.clear()
        self.obstacles.append(self.floor)
        self.vents.clear()

        if self.level == 1:
            self.glider.center_y = 500
            for x in 650, 950:
                v = arcade.Sprite("vent.png", scale=0.3)
                v.center_x = x
                v.center_y = 60
                self.vents.append(v)
            # Add coins to the world
            for x in range(128, 1250, 256):
                coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.25)
                coin.center_x = x
                coin.center_y = 300
                self.coins.append(coin)

        elif self.level == 2:
            for x in 300, 850:
                v = arcade.Sprite("vent.png", scale=0.3)
                v.center_x = x
                v.center_y = 60
                self.vents.append(v)
        elif self.level == 3:
            for x in 400, 850:
                v = arcade.Sprite("vent.png", scale=0.3)
                v.center_x = x
                v.center_y = 60
                self.vents.append(v)

def main():
    """Main function"""
    window = GameView()
    window.setup()
    window.setup_level()
    arcade.run()


if __name__ == "__main__":
    main()
