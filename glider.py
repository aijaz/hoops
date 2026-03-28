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
GRAVITY = 0.1
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
        self.glider = arcade.Sprite(arcade.load_texture("glider_right.png"))
        self.glider.append_texture(arcade.load_texture("glider_left.png"))

        self.vents = arcade.SpriteList()
        v = arcade.Sprite("vent.png")
        v.center_x = 800
        v.center_y = 60
        self.vents.append(v)
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        self.obstacles = arcade.SpriteList()
        floor = arcade.SpriteSolidColor(WINDOW_WIDTH, 1, WINDOW_WIDTH/2, 0, arcade.color.BLACK)
        self.obstacles.append(floor)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.glider, walls=self.obstacles, gravity_constant=GRAVITY
        )

        self.camera = None
        self.cur_key_press = None



    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.glider.center_x = 150
        self.glider.center_y = 500
        self.glider_direction = 'right'
        self.glider.set_texture(0)
        self.camera = arcade.Camera2D()
        self.glider.change_x = 3
        self.glider.change_y = 0
        self.cur_key_press = None

    def on_update(self, delta_time: float) -> bool | None:
        """Movement and Game Logic"""

        # Move the player using our physics engine
        self.physics_engine.update()

        if self.cur_key_press == arcade.key.LEFT:
            self.glider.center_x -= self.glider.change_x / 2  # apply brakes

        for vent in self.vents:
            if abs(vent.center_x - self.glider.center_x) < vent.width:
                self.glider.change_y = VENT_JUMP
                break

        # Center our camera on the player - x axis only
        target_x = self.glider.center_x
        target_y = WINDOW_HEIGHT/2
        self.camera.position = (target_x, target_y)



    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # activate our camera before drawing
        self.camera.use()

        # Draw our sprites
        arcade.draw_sprite(self.glider)

        # Draw vents
        self.vents.draw()
        self.obstacles.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.RIGHT:
            self.cur_key_press = arcade.key.RIGHT
            if self.glider_direction == 'left':
                self.glider_direction = 'right'
                self.glider.set_texture(0)
        elif symbol == arcade.key.LEFT:
            self.cur_key_press = arcade.key.LEFT
            if self.glider_direction == 'right':
                self.glider_direction = 'left'
                self.glider.set_texture(1)
        elif symbol == arcade.key.UP:
            self.glider.change_y = JUMP_SPEED
        elif symbol == arcade.key.ESCAPE:
            self.setup()

    def on_key_release(self, symbol: int, modifiers: int) -> EVENT_HANDLE_STATE:
        self.cur_key_press = None


def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
