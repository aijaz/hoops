"""
Platformer Game

python -m arcade.examples.platform_tutorial.02_draw_sprites
"""
import arcade

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"
GRAVITY = 0.1
JUMP_SPEED = 20


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



    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.glider.center_x = 150
        self.glider.center_y = 500
        self.glider_direction = 'right'
        self.glider.set_texture(0)
        self.camera = arcade.Camera2D()

    def on_update(self, delta_time: float) -> bool | None:
        """Movement and Game Logic"""

        # Move the player using our physics engine
        self.physics_engine.update()

        # Center our camera on the player
        self.glider.change_x = 3

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
            if self.glider_direction == 'left':
                self.glider_direction = 'right'
                self.glider.set_texture(0)
        elif symbol == arcade.key.LEFT:
            if self.glider_direction == 'right':
                self.glider_direction = 'left'
                self.glider.set_texture(1)
        elif symbol == arcade.key.ESCAPE:
            self.setup()



def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
