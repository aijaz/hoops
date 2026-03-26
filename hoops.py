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

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()

    def setup(self):
        self.sprite_list = arcade.SpriteList()
        self.ball = Ball(20, 20, arcade.color.RED, 40, 100)
        self.sprite_list.append(self.ball)

    def on_update(self, delta_time):
        self.ball.center_x += self.ball.x_velocity
        if self.ball.center_x < self.ball.width/2 or self.ball.center_x > WINDOW_WIDTH - self.ball.width/2:
            self.ball.x_velocity *= -1



class Ball(arcade.SpriteSolidColor):
    def __init__(self, width, height, c, x, y):
        super().__init__(width, height, x, y, c)
        self.x_velocity = 3



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
