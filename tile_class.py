"""
    Project: Puzzle Slider Game -- Tile class
    This is the class of the active tiles in the play area

    0715 modified: the tiles no longer draw frames of themselves, so loading
    can be faster
"""
import turtle

from myturtle_class import MyTurtle      # helper class


class Tile(MyTurtle):
    """
    A Tile is a square piece which players can move. If the player clicks on a
    tile adjacent to the blank tile horizontally or vertically, then it will
    swap with the blank one.
    """

    def __init__(self, my_game, shape, index, pos_index, cors):
        """
        Create a Tile instance that appears at a given position with a given
        shape, knows which Game it belongs to, and keeps records of it's
        original unscrambled-status index and current position index. Draw
        the frame it resides in, show the tile, and then register Tile.swap()
        method to mouse click on it
        Params -- my_game: a Game instance, the puzzle game it belongs to
                  shape: a string, the image file name of the tile
                  index: an int, the original unscrambled-status index
                  pos_index: an int, the current position index
                  cors: a tuple(contains 2 floats), the coordinates (x, y)
                        which represents a position
        Return -- None
        """

        super().__init__(cors)           # the tile is a MyTurtle at 'cors'
        self._ts = turtle.getscreen()    # get the screen
        self.game = my_game              # know which Game it belongs to
        self.index, self.pos_index = index, pos_index
        if 'blank' in shape:        # mark the blank tile index in the list
            self.game.set_blank_index(pos_index)
        # self.draw_frame(my_game.get_tile_size())
        self._ts.register_shape(shape)
        self.shape(shape)
        self.showturtle()           # appear!
        self.onclick(self.swap)     # register mouse click on it

    def __str__(self):
        """When printing, indicate the Tile's index & position index. """

        return "This is the {}-th Tile now at {}-th position!".format(
            self.index, self.pos_index)

    def get_index(self):
        return self.index

    def get_pos_index(self):
        return self.pos_index

    def update_pos_index(self, new_pos_index):
        """Update the position index to a new one (int). """

        self.pos_index = new_pos_index

    def draw_frame(self, size):
        """
        Draw the square frame that the tile resides in
        Params -- size: a float, the size of the tile, also the side length
        Return -- None
        """

        cors = self.pos()
        self.goto(cors[0] - size / 2.0, cors[1] + size / 2.0)      # left top
        self.create_frame((size, size))  # MyTurtle is able to draw rectangle
        self.goto(cors)                  # back to the center

    def swap(self, x, y):
        """
        Perform tile swap according to the tile that player clicks on. If the
        player clicks on a tile adjacent to the blank tile horizontally or
        vertically, then swap it with the blank one. Then tell its game to
        update number of moves and do the following work accordingly. No need
        to use (x, y) here, because the tile itself know its position
        Params -- x: a float, the x coordinate where the player clicks
                  y: a float, the y coordinate where the player clicks
        Return -- None
        """

        blank_tile = self.game.get_blank_tile()
        dist = self.distance(blank_tile.pos())
        # check whether the clicked tile is exactly 1 tile away to the blank
        if dist == self.game.get_tile_size() + self.game.get_tile_interval():
            self.exchange_position(blank_tile)
            self.game.update_moves()        # tell the Game to update status

    def exchange_position(self, other):
        """
        Exchange position with another Tile instance, update their position
        index as well
        Params -- other: a Tile instance
        Return -- None
        """

        cors = other.pos()
        other.goto(self.pos())
        self.goto(cors)
        self.pos_index, other.pos_index = other.pos_index, self.pos_index
