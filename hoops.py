import math

import arcade

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "BOUNCING"


class Court(arcade.View):

    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.ALMOND
        self.ball = None
        self.sprite_list = None
        self.backboard = None
        self.floor = None
        self.sprite_list = None
        self.obstacles_sprite_list = None
        self.t = 0
        self.g = 9.8
        self.shoot = False
        self.delta_v = 5
        self.delta_theta = 2
        self.max_v = 250
        self.scored = False

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()
        self.obstacles_sprite_list.draw()
        arcade.draw_text(f"v: {self.ball.v0} theta: {self.ball.theta}",  # Text to draw
                         25,  # X position (center of screen)
                         25,  # Y position (center of screen)
                         arcade.color.BLACK,  # Text color
                         font_size=24)

    def setup(self):
        self.sprite_list = arcade.SpriteList()
        self.ball = Ball(radius=20, color=arcade.color.DARK_RED, x=40, y=100, v0=115, theta=45)
        self.sprite_list.append(self.ball)
        self.backboard = Backboard(20, 200, WINDOW_WIDTH - 20, 400, arcade.color.WHITE)
        self.floor = Floor()
        self.basket = Basket(80, 4, WINDOW_WIDTH - 30 - (80 / 2), 380, arcade.color.RED)
        self.rim = Rim(4, 4, WINDOW_WIDTH - 30 - 80 - 2, 380, arcade.color.BLACK)
        self.obstacles_sprite_list = arcade.SpriteList()
        self.obstacles_sprite_list.append(self.floor)
        self.obstacles_sprite_list.append(self.backboard)
        self.obstacles_sprite_list.append(self.basket)
        self.obstacles_sprite_list.append(self.rim)

    def on_update(self, delta_time):
        if not self.shoot:
            return

        if self.t < 0:
            self.t = 0
            self.shoot = False
            return

        self.t += 1/30
        self.ball.draw_hit_box(line_thickness=3)

        self.ball.center_x = self.ball.start_x + (self.ball.vx * self.t)
        self.ball.center_y = max(self.ball.radius + 1, self.ball.start_y + (self.ball.vy * self.t) - (0.5 * self.g * self.t**2))

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.UP:
            self.ball.theta = min(self.ball.theta + self.delta_theta, 89)
        elif symbol == arcade.key.DOWN:
            self.ball.theta = max(self.ball.theta - self.delta_theta, 1)
        if symbol == arcade.key.RIGHT:
            self.ball.v0 = min(self.ball.v0 + self.delta_v, self.max_v)
        elif symbol == arcade.key.LEFT:
            self.ball.v0 = max(self.ball.v0 - self.delta_v, 1)
        if symbol == arcade.key.SPACE and not self.shoot:
            self.shoot = True
            self.ball.vx = self.ball.v0 * math.cos(math.radians(self.ball.theta))
            self.ball.vy = self.ball.v0 * math.sin(math.radians(self.ball.theta))
        if symbol == arcade.key.R:
            self.t = -1
            self.shoot = True
            self.ball.center_x = 40
            self.ball.center_y = 100
            self.ball.start_x = 40
            self.ball.start_y = 100
            self.scored = False


class Ball(arcade.SpriteCircle):
    def __init__(self, radius, color, x, y, v0, theta):
        super().__init__(radius, color)
        self.center_x = x
        self.center_y = y
        self.v0 = v0
        self.theta = theta
        self.start_x = x
        self.start_y = y
        self.radius = radius


class Backboard(arcade.SpriteSolidColor):
    def __init__(self, width, height, x, y, c):
        super().__init__(width, height, x, y, c)


class Floor(arcade.SpriteSolidColor):
    def __init__(self):
        # super().__init__(width=200, height=4, x=20, y=4, c=arcade.color.BLACK)
        super().__init__(WINDOW_WIDTH, 2, WINDOW_WIDTH / 2, 1, arcade.color.RED)


class Basket(arcade.SpriteSolidColor):
    def __init__(self, width, height, x, y, c):
        super().__init__(width, height, x, y, c)


class Rim(arcade.SpriteSolidColor):
    def __init__(self, width, height, x, y, c):
        super().__init__(width, height, x, y, c)


def main():
    window = arcade.Window(WINDOW_WIDTH,
                           WINDOW_HEIGHT,
                           WINDOW_TITLE)
    # create the game view
    court = Court()
    court.setup()
    # show game view on screen
    window.show_view(court)
    # start the game loop
    arcade.run()


main()
