"""
    Project: Puzzle Slider Game -- Game class
    It is the main functional part of the project
"""

import turtle
import math                          # calculate sqrt, floor integer
import os                            # get puzzle file names
import random                        # shuffle the tiles
import time                          # linger the messages
from datetime import datetime        # get date&time when logging error
from configs import *                # configuration of the Game
from myturtle_class import MyTurtle  # helper class - improved turtle
from tile_class import Tile          # helper class - the tiles


class Game:
    """
    This is the class that our slider puzzle game belongs to. Players input
    their name and set the maximum number of moves they will use, then use the
    mouse to play. They can slide pieces vertically or horizontally on a board
    to establish an end result that matches a solution. They can also select
    to auto-unscramble the pieces, load new puzzles, or quit the game. All the
    UI elements and works behind the scene are implemented by methods of this
    class. Methods are ordered mainly by the operating process of the game.
    __str__ method is not created because it makes little sense here
    """

    def __init__(self):
        """
        Create a slider puzzle game. Load the UI elements, and register mouse
        click (look through the codes for detail steps)
        Params -- None
        Return -- None
        """

        self.ts = turtle.Screen()          # the main window of the game
        self.ts.title(WINDOW_TITLE)        # set the window title
        self.ts.setup(WINDOW_SIZE[0], WINDOW_SIZE[1])  # set the window size
        turtle.hideturtle()
        self.player_name = 'Unknown Player'    # default player_name
        self.max_move_num = 50                 # default maximum move number
        self.leaders = []                      # game performance leaders
        self.info_dict = {}           # information dictionary of the puzzle
        self.tile_interval = 2        # set the interval between 2 tiles
        self.player_moves = 0         # initialize to 0
        self.all_tiles = []           # list of the tiles
        self.blank_index = 0          # the position index of the blank tile
        self.thumb_t = MyTurtle(CORS_DICT['thumbnail'])  # thumbnail turtle
        self.moves_t = MyTurtle(CORS_DICT['move_counter'])  # moves counter
        self.pen_t = MyTurtle()       # the turtle pen to do other things
        self.play()

    def play(self):
        """
        The main driver of the game
        Params -- None
        Return -- None
        """

        self.show_msg('splash')  # show splash screen, linger 2 sec
        self.player_name = self.get_player_name()
        self.max_move_num = self.get_max_move_num()
        self.load_frames()
        self.load_buttons()
        self.leaders = self.read_leaderboard_file()
        self.show_leaderboard()
        self.load_new_puzzle()
        self.init_status_area()
        turtle.mainloop()

    def show_msg(self, name, seconds=2):
        """
        Show splash, error, win...messages for some seconds (default to 2)
        Params -- name, a string, the name of the message
                  seconds, an int, number of seconds the message will linger
        Return -- None
        """

        image = IMAGE_DICT[name]                 # get the image file name
        self.ts.register_shape(image)
        msg_t = turtle.Turtle(shape=image)
        time.sleep(seconds)
        msg_t.hideturtle()

    def get_player_name(self):
        """
        Get the player name through a pop-up window so players can input.
        If player press cancel (get None) or only space, give default name
        Params -- None
        Return -- a string, the player name
        """

        name = self.ts.textinput('Puzzle Slide Game', 'Your Name:')
        if (name is None) or (name.strip() == ''):
            return 'Unknown Player'            # default name
        return name.strip()

    def get_max_move_num(self):
        """
        Let the player select the number of moves they can have to unscramble
        the puzzle (5 - 200). If player press cancel (get None), give default
        number 50. If input a float, get the integer part
        Params -- None
        Return -- an int, the maximum move number the player sets
        """

        num = self.ts.numinput('Puzzle Slide Game - Moves',
                               'Enter the number of moves (chances) you want'
                               + ' (5-200)?', 50, minval=5, maxval=200)
        if num is None:
            return 50                    # default number
        elif isinstance(num, float):
            return math.floor(num)
        return num

    def load_frames(self):
        """
        Draw the frames on the screen. FRAME_DICT data format -- key: frame
        name, value: [left-top coordinate, (width, height), color, thickness].
        self.pen_t is a MyTurtle instance, so it can create_frame
        Params -- None
        Return -- None
        """

        for each in FRAME_DICT.values():
            self.pen_t.goto(each[0])
            self.pen_t.create_frame(each[1], each[2], each[3])

    def load_buttons(self):
        """
        Create the buttons on the screen. BUTTON_DICT data format -- key:
        'function/method name', value: [button position coordinates, shape
        image name]
        Params -- None
        Return -- None
        """

        for key, value in BUTTON_DICT.items():
            func = eval('self.' + key)
            MyTurtle(value[0]).create_button(value[1], func)

    def read_leaderboard_file(self):
        """
        Get game leaders list from leaderboard file. If failing to open the
        file, show error image and log the error, return []
        Params -- None
        Return -- a list, if not empty, each element is a 2-element list:
                  [number of moves used to win(int), player name(str)]
        """

        leaders = []
        try:
            with open('leaderboard.txt', 'r') as f_leaders:
                for line in f_leaders:  # line format -- num of moves: name
                    line = line.split(':')
                    leaders.append([int(line[0].strip()), line[1].strip()])
        except IOError:
            self.show_msg('leaderboard_err')
            name = 'Could not open leaderboard.txt.'
            location = 'Game.read_leaderboard_file()'
            self.log_error(name, location)
        return leaders

    def show_leaderboard(self):
        """
        Show game leaders on the leaderboard line by line, with a 'Leaders'
        as the title
        Params -- None
        Return -- None
        """

        self.pen_t.goto(CORS_DICT['leaders_text'])
        self.pen_t.pencolor('blue')
        self.pen_t.write("Leaders: ", font=FONT_DICT['leader_title'])
        self.pen_t.setheading(270)            # head down
        self.pen_t.fd(50)                     # line spacing
        for moves, name in self.leaders:
            line = '{:4d} : {}'.format(moves, name[:16])  # format the length
            self.pen_t.write(line, font=FONT_DICT['leader_list'])
            self.pen_t.fd(35)                 # line spacing

    def load_new_puzzle(self, selection='mario.puz'):
        """
        Load a new puzzle according to user selection (default is mario).
        This includes updating puzzle information dictionary, player move
        counter, tiles, and thumbnail image
        Params -- selection: a string, the file name of puzzle selected,
                             default is 'mario.puz'
        Return -- None
        """

        self.read_new_puzzle_file(selection)  # update the info_dict
        self.player_moves = 0  # reset the moves count to 0
        self.moves_t.clear()  # clear the moves counter shown
        self.clear_tiles()  # clear current tiles
        self.generate_tiles()  # load new tiles
        self.show_thumbnail(self.info_dict['thumbnail'])

    def read_new_puzzle_file(self, selection):
        """
        Read a new puzzle file according to user selection, then validate
        the file data (see Game.validate_puzzle_file())
        Params -- selection: a string, the file name of puzzle selected
        Return -- None. Just update info_dict or raise error
        """

        new_info_dict = {}
        with open(selection, 'r') as f:
            for line in f:
                info_list = line.split(':')
                new_info_dict[info_list[0].strip()] = info_list[1].strip()
        self.validate_puzzle_file(new_info_dict)

    def validate_puzzle_file(self, new_info_dict):
        """
        Check if the puzzle file data is good (no malformed data). If good,
        update the puzzle information dictionary (info_dict); otherwise raise
        ValueError and leave the info_dict untouched
        Params -- new_info_dict: a dictionary, data read from the .puz file
        Return -- None. Just update info_dict or raise error
        """

        if not (new_info_dict.keys() > FILE_KEYS):  # check necessary keys
            raise ValueError
        size = float(new_info_dict['size'])
        nums = int(new_info_dict['number'])
        if ((nums not in VALID_NUMS) or (size > SIZE_BOUND[1]) or
                (size < SIZE_BOUND[0])):  # validate numbers and size
            raise ValueError
        # '1', '2', '3'... '(nums)' should be in the dict keys
        for i in range(1, nums + 1):
            if str(i) not in new_info_dict:
                raise ValueError
        self.info_dict = new_info_dict  # update self.info_dict 'safely'

    def clear_tiles(self):
        """
        Clear current tiles and their drawings (the frames they reside in),
        reset the self.all_tiles to []
        Params -- None
        Return -- None
        """

        for each in self.all_tiles:
            each.clear()
            each.hideturtle()
        self.all_tiles = []

    def generate_tiles(self):
        """
        Create the tiles in a scrambled status
        Params -- None
        Return -- None. Update the self.all_tiles list
        """

        position_list = self.generate_positions()  # unscramble ordered list
        index = list(range(int(self.info_dict['number'])))
        random.shuffle(index)  # index list is scrambled now
        for i in range(len(index)):
            # format: Tile(game, tile image, ori-index, pos_index, cors)
            # the original index[i]-th tile appears at i-th position
            new_tile = Tile(self, self.info_dict[str(index[i] + 1)],
                            index[i], i, position_list[i])
            self.all_tiles.append(new_tile)

    def generate_positions(self):
        """
        Generate position grids for the tiles, such that the tiles are center
        aligned in the play area, each pair of horizontal or vertical
        neighbors keep a specific interval (self.tile_interval). The returned
        list is ordered from left-top to right_bottom row after row, which is
        matched with the unscrambled version order in the .puz files
        Params -- None
        Return -- a list, each element is a tuple (x, y) which is the
                  coordinates of a position (will be the center of a tile)
        """

        position_list = []
        n = int(math.sqrt(int(self.info_dict['number'])))  # n rows/columns
        size = self.get_tile_size()
        gap = size + self.tile_interval  # distance between 2 positions

        # calculate the left top tile coordinates (x_0, y_0)
        # FRAME_DICT['play_area'][0]: left top coordinates (x, y) of play area
        # FRAME_DICT['play_area'][1]: size of play area, (width, height)
        x_0 = FRAME_DICT['play_area'][0][0] + \
              (FRAME_DICT['play_area'][1][0] - (n - 1) * gap) / 2.0
        y_0 = FRAME_DICT['play_area'][0][1] - \
              (FRAME_DICT['play_area'][1][1] - (n - 1) * gap) / 2.0

        # generate and append coordinates row by row
        for i in range(n):
            x = x_0
            for j in range(n):
                position_list.append((x, y_0))
                x += gap
            y_0 -= gap
        return position_list

    def show_thumbnail(self, thumb_image):
        """
        Show (or update when loading new file) the thumbnail image
        Params -- thumb_image, a string, the name of thumbnail image
        Return -- None
        """

        self.ts.register_shape(thumb_image)
        self.thumb_t.shape(thumb_image)
        if not self.thumb_t.isvisible():  # not visible only when game starts
            self.thumb_t.showturtle()

    def init_status_area(self):
        """
        Write the title of status area which shows number of player moves
        Params -- None
        Return -- None
        """

        self.pen_t.goto(CORS_DICT['move_title'])
        self.pen_t.pencolor('black')
        self.pen_t.write("Player Move: ", font=FONT_DICT['status_area'])

    def update_moves(self):
        """
        Add 1 to the number of player moves, and update it on status area.
        Check if the player wins or loses now, to respond accordingly
        Params -- None
        Return -- None
        """

        self.player_moves += 1
        self.moves_t.clear()
        self.moves_t.write(str(self.player_moves),
                           font=FONT_DICT['status_area'])
        self.check_success()

    def check_success(self):
        """
        Check game status. If the tiles are unscrambled, then player wins, so
        update leaderboard file, show win image, and exit game; elif the tiles
        are not unscrambled and the number of player moves reaches maximum,
        then player loses, so show lose image, and exit game; otherwise do
        nothing, game continues
        Params -- None
        Return -- None
        """

        if self.is_unscrambled():
            self.update_leaderboard()
            self.show_msg('win')
            self.close_window()
        else:
            if self.player_moves == self.max_move_num:
                self.show_msg('lose')
                self.close_window()

    def is_unscrambled(self):
        """
        Check whether the tiles are unscrambled by comparing their original
        unscrambled index with their current position index. If all match,
        then they are unscrambled
        Params -- None
        Return -- Boolean, True if the tiles are unscrambled, False otherwise
        """

        for each in self.all_tiles:
            if each.get_index() != each.get_pos_index():
                return False
        return True

    def update_leaderboard(self):
        """
        Update game leaders, and write to the leaderboard file. The leaders
        list is already sorted in an ascending order according to number of
        moves (score) each 'leader' used, so just compare the new player_move
        with scores linearly, then insert or append it to the proper index.
        (For tied scores, the earlier player should be granted a higher
        position). It makes little sense to keep a record of all game winners,
        so only write no more than MAX_LEADERS to the file
        Params -- None
        Return -- None
        """

        i = 0
        # find the proper score position of current player
        # self.leaders[i][0]: the score of the i-th leader
        while (i < len(self.leaders)) \
                and (self.player_moves >= self.leaders[i][0]):
            i += 1
        if i == len(self.leaders):
            self.leaders.append([self.player_moves, self.player_name])
        else:
            self.leaders.insert(i, [self.player_moves, self.player_name])

        with open('leaderboard.txt', 'w') as f_leaders:
            for i in range(min(len(self.leaders), MAX_LEADERS)):
                f_leaders.write(str(self.leaders[i][0]) + ':'
                                + self.leaders[i][1] + '\n')

    def reset(self, x, y):
        """
        Auto-unscramble the puzzle, which means the tiles goto their original
        unscrambled position, and update their position index. It has
        parameters x & y because it's bonded with mouse click
        Params -- x: a float, the x coordinate where the player clicks
                  y: a float, the y coordinate where the player clicks
        Return -- None. Modifies the all_tiles list
        """

        position_list = self.generate_positions()
        for i in range(int(self.info_dict['number'])):
            self.all_tiles[i].goto(
                position_list[self.all_tiles[i].get_index()])
            # reset their position index to unscrambled index
            self.all_tiles[i].update_pos_index(self.all_tiles[i].get_index())

    def get_new_selection(self, x, y):
        """
        Get a new puzzle selection from the user. If the user attempts to load
        a non-existent file, or a .puz file that has malformed data, show the
        error image and log the error. It has parameters x & y because it's
        bonded with mouse click
        Params -- x: a float, the x coordinate where the player clicks
                  y: a float, the y coordinate where the player clicks
        Return -- None
        """

        puz_list = self.get_puz_list()
        title = 'Load Puzzle'
        prompt = ('Enter the name of the puzzle you wish to load.'
                  + ' Choices are:\n' + '\n'.join(puz_list))
        selection = self.ts.textinput(title, prompt)

        if selection is not None:   # it is None if user press cancel
            selection = selection.strip()
            try:
                self.load_new_puzzle(selection)
            except IOError:
                self.show_msg('file_err')
                self.log_error("File '{}' does not exist.".format(selection),
                               'Game.get_new_selection()')
            except:
                self.show_msg('file_err')
                self.log_error('Malformed puzzle file: {}'.format(selection),
                               'Game.load_new_puzzle()')

    def get_puz_list(self):
        """
        Get the .puz file list in the directory, if more then 10 files
        available, show file_warning image and only get the first 10
        Params -- None
        Return -- a list, each element is a .puz file name
        """

        file_list = os.listdir('.')
        puz_list = []
        for file_name in file_list:
            if file_name.endswith('.puz'):
                puz_list.append(file_name)
        if len(puz_list) > 10:
            self.show_msg('file_warning')
        return puz_list[:10]       # load first 10 if more than 10 files

    def quit_game(self, x, y):
        """
        Show quit image and exit the game (when user press quit button).
        It has parameters x & y because it's bonded with mouse click
        Params -- x: a float, the x coordinate where the player clicks
                  y: a float, the y coordinate where the player clicks
        Return -- None
        """

        self.show_msg('quit')
        self.close_window()

    def close_window(self):
        """
        When the game exits, show credit image, then terminate the program
        Params -- None
        Return -- None
        """

        self.show_msg('credit')
        self.ts.clearscreen()
        self.ts.bye()

    def log_error(self, name, location):
        """
        Log errors to error file ('puzzle_log.err') in a specific format:
        'Sat Dec  4 21:57:17 2021:  Error: Malformed puzzle file:
        malformed_mario.puz  LOCATION: Game.load_new_puzzle()'
        Params -- name: a string, brief description of the error
                  location: a string, the method position of the error
        Return -- None. Just append information to the error file
        """

        now_time = datetime.now().strftime('%c') + ':'  # current date & time
        name = '  Error: ' + name
        location = '  LOCATION: ' + location
        with open('puzzle_log.err', 'a') as f:
            f.write(now_time + name + location + '\n')

    def get_tile_size(self):
        """Return the tile size (float). """

        return float(self.info_dict['size'])

    def get_tile_interval(self):
        """Return the tile interval (float). """

        return self.tile_interval

    def set_blank_index(self, index):
        """Update the blank_index to a new index(int). """

        self.blank_index = index

    def get_blank_tile(self):
        """return the blank Tile (a Tile instance). """

        return self.all_tiles[self.blank_index]



