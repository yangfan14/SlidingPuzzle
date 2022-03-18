"""
    Project: Puzzle Slider Game -- Game configs
    This is the configuration data of the game
"""

WINDOW_TITLE = 'Sliding puzzle'
WINDOW_SIZE = (800, 800)    # (width, height)
IMAGE_DICT = {'splash': 'Resources/splash_screen.gif',
              'win': 'Resources/winner.gif',
              'lose': 'Resources/Lose.gif',
              'credit': 'Resources/credits.gif',
              'quit': 'Resources/quitmsg.gif',
              'leaderboard_err': 'Resources/leaderboard_error.gif',
              'file_warning': 'Resources/file_warning.gif',
              'file_err': 'Resources/file_error.gif'}

# each value is the position coordinates of the key
CORS_DICT = {'leaders_text': (160, 270),
             'move_title': (-320, -260),
             'move_counter': (-180, -260),
             'thumbnail': (300, 260)}

# value format: [left-top coordinate, (width, height), color, thickness]
FRAME_DICT = {'play_area': [(-350, 320), (460, 460), 'black', '6'],
              'leaderboard': [(150, 320), (200, 460), 'blue', '6'],
              'status_area': [(-350, -200), (700, 100), 'black', '6']}

# key format: 'function/method name'
# value format: [button position coordinates, shape image name]
BUTTON_DICT = {'quit_game': [(300, -250), 'Resources/quitbutton.gif'],
               'get_new_selection': [(200, -250), 'Resources/loadbutton.gif'],
               'reset': [(100, -250), 'Resources/resetbutton.gif']}

FONT_DICT = {'status_area': ('Arial', 20, 'bold'),
             'leader_title': ('Arial', 20, 'bold'),
             'leader_list': ('Arial', 15, 'bold')}
VALID_NUMS = {16, 9, 4}                      # valid tile numbers
SIZE_BOUND = (50, 110)                       # valid tile size range
FILE_KEYS = {'size', 'number', 'thumbnail'}  # necessary puzzle file keys
MAX_LEADERS = 10                             # max leaders record kept
