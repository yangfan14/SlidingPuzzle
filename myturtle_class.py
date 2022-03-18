"""
    Project: Puzzle Slider Game -- MyTurtle class
    It is created to provide some helper methods widely used in this game.
"""

import turtle


class MyTurtle(turtle.Turtle):
    """
    MyTurtle is an improved Turtle. It is none visible, none pendown, and has
    a fastest speed. It is initialized at a specific position. It can create
    buttons and frames on the screen
    """

    def __init__(self, cors=(0, 0)):
        """
        Create a MyTurtle instance by moving an invisible turtle to a target
        position at fastest speed without leaving trace
        Params -- cors, a tuple, both elements are float, default to (0,0)
        Return -- None
        """

        super().__init__(visible=False)  # not show itself when created
        self._ts = turtle.getscreen()    # get the screen
        self.pen(pendown=False, speed=0)
        self.goto(cors)

    def __str__(self):
        """When printing, indicate its current position. """

        return "MyTurtle instance at {}".format(self.pos())

    def create_frame(self, size, pencolor='black', pensize=1):
        """
        Draw a rectangle frame given specific size, color, and pensize.
        size = (width, height)
        Params -- size, a tuple, both elements are float
                  pencolor, a string, a valid color, default to 'black'
                  pensize, an int, thickness of the frame, default to 1
        Return -- None
        """

        self.pen(pendown=True, pencolor=pencolor, pensize=pensize)
        for i in range(2):
            self.fd(size[0])
            self.rt(90)
            self.fd(size[1])
            self.rt(90)
        self.penup()      # carefully pull up the pen after drawing

    def create_button(self, shape, func):
        """
        Create a button on the screen, given button image and function/method
        bonded with the button on mouse click
        Params -- shape, a string, the button image name
                  func, a function, to be bonded with the button on click
        Return -- None
        """

        try:             # in case using button shape available in dir
            self._ts.register_shape(shape)
        except turtle.TurtleGraphicsError:
            pass
        self.shape(shape)
        self.showturtle()
        self.onclick(func)
