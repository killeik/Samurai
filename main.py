"""
Samurai Game
"""

import arcade
import arcade.gui


# Constants
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Samurai"

CHARACTER_SCALING = 1.3

# How fast to move, and how fast to run the animation
MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 5

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]


class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right

        self.character_face_direction = RIGHT_FACING


        # Used for flipping between image sequences

        self.cur_texture = 0


        self.scale = CHARACTER_SCALING

        # --- Load Textures ---


        # Load textures for idle standing

        self.idle_texture_pair = load_texture_pair(f"./resources/Martial Hero 2/Frames/Idle/0.png")



        # Load textures for walking

        self.walk_textures = []

        for i in range(8):

            texture = load_texture_pair(f"./resources/Martial Hero 2/Frames/Run/{i}.png")

            self.walk_textures.append(texture)



    def update_animation(self, delta_time: float = 1 / 60):


        # Figure out if we need to flip face left or right

        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:

            self.character_face_direction = LEFT_FACING

        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:

            self.character_face_direction = RIGHT_FACING



        # Idle animation

        if self.change_x == 0 and self.change_y == 0:

            self.texture = self.idle_texture_pair[self.character_face_direction]

            return



        # Walking animation

        self.cur_texture += 1

        if self.cur_texture > 7 * UPDATES_PER_FRAME:

            self.cur_texture = 0

        frame = self.cur_texture // UPDATES_PER_FRAME

        direction = self.character_face_direction

        self.texture = self.walk_textures[frame][direction]


class MenuView(arcade.View):
    """
    Class that manages the menu view.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__()

        # Initialize UIManger to handle UI
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background color
        arcade.set_background_color(arcade.color.GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=25))
        start_button.on_click = self.on_click_start

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=25))
        settings_button.on_click = self.on_click_settings

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button)
        quit_button.on_click = self.on_click_quit

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_start(self, event):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

    def on_click_settings(self, event):
        print("Settings:", event)

    def on_click_quit(self, event):
        arcade.exit()

    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here
        self.manager.draw()


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__()
        # Sprite lists
        self.player_list = None

        # Set up the player
        self.player = None

        # Set the background color
        arcade.set_background_color(arcade.color.GRAY_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player = PlayerCharacter()

        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player.scale = CHARACTER_SCALING

        self.player_list.append(self.player)

    def on_draw(self):
        """Render the screen."""

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.coin_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player
        self.player_list.update()

        # Update the players animation

        self.player_list.update_animation()


    def on_show_view(self):
        self.setup()


def main():
    """Startup"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
