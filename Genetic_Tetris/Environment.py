import random, time, pygame, sys
from pygame.locals import *
from Agent import Agent, N_GENES
import pygame
from time import sleep
#region CONSTANTS
##############################################################################
# SETTING UP GENERAL CONSTANTS
##############################################################################

# Board config
FPS          = 1000
# WINDOWWIDTH  = 650 # 500
WINDOWWIDTH  = 790
WINDOWHEIGHT = 800
BOXSIZE      = 25
BOARDWIDTH   = 10
BOARDHEIGHT  = 25
BLANK        = '.'
XMARGIN      = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN    = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5


# Timing config
# Every time the player pushes the left or right arrow key down, the falling
# piece should move one box over to the left or right, respectively. However,
# the player can also hold down the left or right arrow key to keep moving the
# falling piece. The MOVESIDEWAYSFREQ constant will set it so that every 0.15
# seconds that passes with the left or right arrow key held down, the piece
# will move another space over.
MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ     = 0.1

# Colors
#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR     = BLUE
BGCOLOR         = BLACK
TEXTCOLOR       = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS          = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS     = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)

# Each color must have light color
assert len(COLORS) == len(LIGHTCOLORS)

# Piece Templates
# The TEMPLATEWIDTH and TEMPLATEHEIGHT constants simply set how large each row
# and column for each shape’s rotation should be
TEMPLATEWIDTH  = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

# Define if the game is manual or not
MANUAL_GAME = False

#endregion

# Setting the random seed

class Environment:
    BASIC_WIDTH = 450
    BASIC_HEIGHT = 690

    def __init__(self, width =450, height = 690, next_pieces=[]) -> None:

        self.width = width
        self.height = height
        # print(f"width: {self.width} and height: {self.height}")
        self.root = pygame.Surface((width, height))
        self.box_size = self.width // 26 + (self.height // 410)*(395 // self.width) * 7
        # self.box_size = 5
        # print(f"Box Size: {self.box_size}")s
        # self.XMARGIN      = int((self.width - BOARDWIDTH * self.box_size) / 2) // 4 + 15
        self.XMARGIN      = int((self.width - BOARDWIDTH * self.box_size) / 2) // 4 + (self.box_size * 6)\
            - (self.height // 410)*(395 // self.width) * 100
        self.TOPMARGIN    = self.height - (BOARDHEIGHT * self.box_size) - (self.box_size * 6)\
            + (self.height // 410) * 150 - (self.height // 410)*(395 // self.width) * 150
            

        self.tetri = 0
        self.event_queue = []
        self.board              = self.get_blank_board()
        self.last_movedown_time = time.time()
        self.last_moveside_time = time.time()
        self.last_fall_time     = time.time()
        self.moving_down        = False # note: there is no movingUp variable
        self.moving_left        = False
        self.moving_right       = False
        self.score              = 0
        self.level, self.fall_freq   = self.calc_level_and_fall_freq(self.score)

        self.next_piece_index = 0
        self.next_pieces = next_pieces
        self.falling_piece      = self.get_new_piece()
        self.next_piece         = self.get_new_piece()
        self.total_removed_lines = 0

        self.turns = 0
        self.flag = False
        # print(self.height - (BOARDHEIGHT * self.box_size) - 50)
        
    def reset(self, new_pieces=[], agent: Agent = None):
        self.event_queue  = []
        self.board              = self.get_blank_board()
        self.last_movedown_time = time.time()
        self.last_moveside_time = time.time()
        self.last_fall_time     = time.time()
        self.moving_down        = False # note: there is no movingUp variable
        self.moving_left        = False
        self.moving_right       = False
        self.score              = 0
        self.level, self.fall_freq   = self.calc_level_and_fall_freq(self.score)
        self.next_piece_index = 0
        self.next_pieces = new_pieces
        self.falling_piece      = self.get_new_piece()
        self.next_piece         = self.get_new_piece()
        self.agent = agent
        self.turns = 0
        self.flag = False

        self.total_removed_lines = 0

    def step(self):
        # Setup variables
        # Game Loop
        if not self.flag:
            if self.agent != None:
                move = self.best_move()
                self.do_move(move)
            self.flag = True
        if (self.falling_piece == None):
            # No falling piece in play, so start a new piece at the top
            self.falling_piece = self.next_piece
            self.next_piece    = self.get_new_piece()
            self.score += 1
            self.turns += 1
            # Reset self.last_fall_time
            self.last_fall_time = time.time()

            if (not self.is_valid_position(self.board, self.falling_piece)):
                # GAME-OVER
                # Can't fit a new piece on the board, so game over.
                return False

            #if the environment has an agent
            #eval all possible moves using the agent and choose the best
            #then add to event_queue the events to lead to that move
            if self.agent != None:
                move = self.best_move()
                self.do_move(move)
        for event in self.event_queue:
            # Event handling loop
            if (event.type == KEYUP):
                if (event.key == K_LEFT or event.key == K_a):
                    self.moving_left = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    self.moving_right = False
                elif (event.key == K_DOWN or event.key == K_s):
                    self.moving_down = False

            elif event.type == KEYDOWN:
                # Moving the piece sideways
                if (event.key == K_LEFT or event.key == K_a) and \
                    self.is_valid_position(self.board, self.falling_piece, adj_X=-1):

                    self.falling_piece['x'] -= 1
                    self.moving_left         = True
                    self.moving_right        = False
                    self.last_moveside_time  = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and \
                    self.is_valid_position(self.board, self.falling_piece, adj_X=1):

                    self.falling_piece['x'] += 1
                    self.moving_right        = True
                    self.moving_left         = False
                    self.last_moveside_time  = time.time()

                # Rotating the piece (if there is room to rotate)
                elif (event.key == K_UP or event.key == K_w):
                    self.falling_piece['rotation'] = (self.falling_piece['rotation'] + 1) % len(PIECES[self.falling_piece['shape']])

                    if (not self.is_valid_position(self.board, self.falling_piece)):
                        self.falling_piece['rotation'] = (self.falling_piece['rotation'] - 1) % len(PIECES[self.falling_piece['shape']])

                elif (event.key == K_q):
                    self.falling_piece['rotation'] = (self.falling_piece['rotation'] - 1) % len(PIECES[self.falling_piece['shape']])

                    if (not self.is_valid_position(self.board, self.falling_piece)):
                        self.falling_piece['rotation'] = (self.falling_piece['rotation'] + 1) % len(PIECES[self.falling_piece['shape']])

                # Making the piece fall faster with the down key
                elif (event.key == K_DOWN or event.key == K_s):
                    self.moving_down = True

                    if (self.is_valid_position(self.board, self.falling_piece, adj_Y=1)):
                        self.falling_piece['y'] += 1

                    self.last_movedown_time = time.time()

                # Move the current piece all the way down
                elif event.key == K_SPACE:
                    self.moving_down  = False
                    self.moving_left  = False
                    self.moving_right = False

                    for i in range(1, BOARDHEIGHT):
                        if (not self.is_valid_position(self.board, self.falling_piece, adj_Y=i)):
                            break

                    self.falling_piece['y'] += i - 1

        self.event_queue.clear()
        # Handle moving the piece because of user input
        if (self.moving_left or self.moving_right) and time.time() - self.last_moveside_time > MOVESIDEWAYSFREQ:
            if self.moving_left and self.is_valid_position(self.board, self.falling_piece, adj_X=-1):
                self.falling_piece['x'] -= 1
            elif self.moving_right and self.is_valid_position(self.board, self.falling_piece, adj_X=1):
                self.falling_piece['x'] += 1

            self.last_moveside_time = time.time()

        if self.moving_down and time.time() - self.last_movedown_time > MOVEDOWNFREQ and self.is_valid_position(self.board, self.falling_piece, adj_Y=1):
            self.falling_piece['y'] += 1
            self.last_movedown_time = time.time()

        # Let the piece fall if it is time to fall
        if time.time() - self.last_fall_time > self.fall_freq:
            # See if the piece has landed
            if (not self.is_valid_position(self.board, self.falling_piece, adj_Y=1)):
                # Falling piece has landed, set it on the board
                self.add_to_board(self.board, self.falling_piece)
                num_removed_lines = self.remove_complete_lines(self.board)

                # Bonus score for complete lines at once
                # 40   pts for 1 line
                # 120  pts for 2 lines
                # 300  pts for 3 lines
                # 1200 pts for 4 lines

                if(num_removed_lines == 1):
                    self.score += 40
                elif (num_removed_lines == 2):
                    self.score += 120
                elif (num_removed_lines == 3):
                    self.score += 300
                elif (num_removed_lines == 4):
                    self.tetri += 1
                    self.score += 1200
                self.total_removed_lines += num_removed_lines
                self.level, self.fall_freq = self.calc_level_and_fall_freq(self.score)
                self.falling_piece    = None

            else:
                # Piece did not land, just move the piece down
                self.falling_piece['y'] += 1
                self.last_fall_time      = time.time()

        # Drawing everything on the screen
        self.root.fill(BGCOLOR)
        self.draw_board(self.board)
        self.draw_status(self.score, self.level)
        self.draw_next_piece(self.next_piece)

        if self.falling_piece != None:
            self.draw_piece(self.falling_piece)

        return True

    ##############################################################################
    # GAME FUNCTIONS
    ##############################################################################

    def make_text_objs(self, text, font, color):
        surf = font.render(text, True, color)

        return surf, surf.get_rect()

    def check_key_press(self):
        # Go through event queue looking for a KEYUP event.

        for event in pygame.event.get([KEYDOWN, KEYUP]):
            if event.type == KEYDOWN:
                continue
            return event.key
        return None

    def show_text_screen(self, text):
        # This function displays large text in the
        # center of the screen until a key is pressed.

        # Draw the text drop shadow
        title_surf, title_rect = self.make_text_objs(text, BIGFONT, TEXTSHADOWCOLOR)
        title_rect.center      = (int(self.width / 2), int(self.height / 2))
        self.root.blit(title_surf, title_rect)

        # Draw the text
        title_surf, title_rect = self.make_text_objs(text, BIGFONT, TEXTCOLOR)
        title_rect.center      = (int(self.width / 2) - 3, int(self.height / 2) - 3)
        self.root.blit(title_surf, title_rect)

        # Draw the additional "Press a key to play." text.
        press_key_surf, press_key_rect = self.make_text_objs('Press a key to play.', BASICFONT, TEXTCOLOR)
        press_key_rect.center = (int(self.width / 2), int(self.height / 2) + 100)
        self.root.blit(press_key_surf, press_key_rect)

        while self.check_key_press() == None:
            pygame.display.update()
            FPSCLOCK.tick()

    def calc_level_and_fall_freq(self, score):
        """ Calculate level and fall frequency
            Based on the score, return the level the player is on and
            how many seconds pass until a falling piece falls one space.

        Args:
            score: game score

        """
        level     = int(score / 400) + 1
        fall_freq = 0.27 - (level * 0.02)

        if (not MANUAL_GAME):
            fall_freq = 0.00

        return level, fall_freq

    def get_new_piece(self, ):
        """Return a random new piece in a random rotation and color"""
        if self.next_piece_index < len(self.next_pieces):
            self.next_piece_index += 1
            return dict(self.next_pieces[self.next_piece_index-1])
        shape     = random.choice(list(PIECES.keys()))
        new_piece = {'shape': shape,
                    'rotation': random.randint(0, len(PIECES[shape]) - 1),
                    'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                    'y': -2, # start it above the board (i.e. less than 0)
                    'color': random.randint(0, len(COLORS)-1)}

        return new_piece

    def add_to_board(self, board, piece):
        """Fill in the board based on piece's location, shape, and rotation"""

        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                    board[x + piece['x']][y + piece['y']] = piece['color']

    def get_blank_board(self, ):
        """Create and return a new blank board data structure"""

        board = []
        for i in range(BOARDWIDTH):
            board.append([BLANK] * BOARDHEIGHT)

        return board

    def is_on_board(self, x, y):
        """Check if the piece is on the board"""

        return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

    def is_valid_position(self, board, piece, adj_X=0, adj_Y=0):
        """Return True if the piece is within the board and not colliding"""

        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                is_above_board = y + piece['y'] + adj_Y < 0

                if is_above_board or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                    continue

                if not self.is_on_board(x + piece['x'] + adj_X, y + piece['y'] + adj_Y):
                    return False

                if board[x + piece['x'] + adj_X][y + piece['y'] + adj_Y] != BLANK:
                    return False

        return True

    def is_complete_line(self, board, y):
        """Return True if the line filled with boxes with no gaps"""

        for x in range(BOARDWIDTH):
            if board[x][y] == BLANK:
                return False

        return True

    def remove_complete_lines(self, board):
        """Remove any completed lines on the board.

        After remove any completed lines, move everything above them dowm and
        return the number of complete lines.

        """
        num_removed_lines = 0
        y = BOARDHEIGHT - 1     # Start y at the bottom of the board

        while y >= 0:
            if self.is_complete_line(board, y):
                # Remove the line and pull boxes down by one line.
                for pullDownY in range(y, 0, -1):
                    for x in range(BOARDWIDTH):
                        board[x][pullDownY] = board[x][pullDownY-1]

                # Set very top line to blank.
                for x in range(BOARDWIDTH):
                    board[x][0] = BLANK

                num_removed_lines += 1

                # Note on the next iteration of the loop, y is the same.
                # This is so that if the line that was pulled down is also
                # complete, it will be removed.
            else:
                y -= 1  # Move on to check next row up

        return num_removed_lines

    def conv_to_pixels_coords(self, boxx, boxy):
        """Convert the given xy coordinates to the screen coordinates

        Convert the given xy coordinates of the board to xy coordinates of the
        location on the screen.

        """
        return (self.XMARGIN + (boxx * self.box_size)), (self.TOPMARGIN + (boxy * self.box_size))

#region DrawStuff
    #relative number to the width
    def draw_box(self, boxx, boxy, color, pixelx=None, pixely=None):
        """Draw box

        Draw a single box (each tetromino piece has four boxes) at xy coordinates
        on the board. Or, if pixelx and pixely are specified, draw to the pixel
        coordinates stored in pixelx and pixely (this is used for the "Next" piece).

        """
        if color == BLANK:
            return

        if pixelx == None and pixely == None:
            pixelx, pixely = self.conv_to_pixels_coords(boxx, boxy)

        pygame.draw.rect(self.root, COLORS[color], (pixelx + 1, pixely + 1, self.box_size - 1, self.box_size - 1))
        pygame.draw.rect(self.root, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, self.box_size - 4, self.box_size - 4))

    def draw_board(self, board):
        """Draw board"""

        # Draw the border around the board
        pygame.draw.rect(self.root, BORDERCOLOR, (self.XMARGIN - 3, self.TOPMARGIN - 7, (BOARDWIDTH * self.box_size) + 8, (BOARDHEIGHT * self.box_size) + 8), 5)
        
        pygame.draw.rect(self.root, (11,11,11), pygame.Rect(0, 0, self.width, self.height), 2)
        # pygame.draw.rect(self.root, 'red', (0, 0, self.width, self.height), 2)
        
        # Fill the background of the board
        pygame.draw.rect(self.root, BGCOLOR, (self.XMARGIN + 1, self.TOPMARGIN, self.box_size * BOARDWIDTH, self.box_size * BOARDHEIGHT))

        # Draw the individual boxes on the board
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                self.draw_box(x, y, board[x][y])
            
    def draw_status(self, score, level):
        """Draw status"""

        # Draw the score text
        score_surf = BASICFONT.render('Score: %s' % (score), True, TEXTCOLOR)
        score_rect = score_surf.get_rect()
        # score_rect.topleft = (self.width - int(5/13 * self.width), int(8/690 * self.height))
        # score_rect.topleft = (self.width - int(7/13 * self.width), int(400/690 * self.height))
        score_rect.topleft = (self.XMARGIN - (200//self.height)*42 + (self.height//410)*(1), (200//self.height)*(self.height - 30) + (self.height//410)*(self.height - 25))
        self.root.blit(score_surf, score_rect)


        # draw the level text
        levelSurf = BASICFONT.render('Turn: %s' % (self.turns), True, TEXTCOLOR)
        levelRect = levelSurf.get_rect()
        # levelRect.topleft = (self.width - int(3/13 * self.width), int(110/690*self.height))
        # levelRect.topleft = (self.width - int(7/13 * self.width), int((400+(110-8))/690*self.height))
        levelRect.topright = (self.XMARGIN + (200//self.height)*(self.width - 50 - 3) + (self.height//410)*(300) , (200//self.height)*(self.height - 17) + (self.height//410)*(self.height - 25))
        self.root.blit(levelSurf, levelRect)

    def draw_piece(self, piece, pixelx=None, pixely=None):
        """Draw piece"""

        shape_to_draw = PIECES[piece['shape']][piece['rotation']]

        if pixelx == None and pixely == None:
            # If pixelx and pixely hasn't been specified, use the location stored
            # in the piece data structure
            pixelx, pixely = self.conv_to_pixels_coords(piece['x'], piece['y'])

        # Draw each of the boxes that make up the piece
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                if shape_to_draw[y][x] != BLANK:
                    self.draw_box(None, None, piece['color'], pixelx + (x * self.box_size), pixely + (y * self.box_size))

    def draw_next_piece(self, piece):
        """Draw next piece"""

        # draw the "next" piece
        self.draw_piece(piece, pixelx=self.width-int(3 / 13 * self.width), pixely=int(160/690*self.height))
        # self.draw_piece(piece, pixelx=self.XMARGIN + self.box_size * (BOARDWIDTH + 1), pixely=160)

#endregion
#region Stats
    ##############################################################################
    # GAME STATISTICS FUNCTIONS
    ##############################################################################
    def do_move(self, move):
        piece = dict(self.falling_piece)
        r = piece['rotation']
        while r != move['r']:
            self.event_queue.append(pygame.event.Event(KEYDOWN, {'key': K_UP}))
            self.event_queue.append(pygame.event.Event(KEYUP, {'key': K_UP}))
            r = (r + 1) % len(PIECES[piece['shape']])
        x = int(piece['x'])

        while x < move['x']:
            x += 1
            self.event_queue.append(pygame.event.Event(KEYDOWN, {"key": K_RIGHT}))
            self.event_queue.append(pygame.event.Event(KEYUP, {"key": K_RIGHT}))

        while x > move['x']:
            self.event_queue.append(pygame.event.Event(KEYDOWN, {"key": K_LEFT}))
            self.event_queue.append(pygame.event.Event(KEYUP, {"key": K_LEFT}))
            x -= 1

    def best_move(self):
        total_holes_bef, total_blocking_bloks_bef = self.calc_initial_move_info(self.board)
        best_rating = -11111111111
        best_move = {'x':0, 'r':0}
        for x in range(-TEMPLATEWIDTH, BOARDWIDTH + TEMPLATEWIDTH):
            for r in range(len(PIECES[self.falling_piece['shape']])):
                result = self.calc_move_info(self.board, dict(self.falling_piece),x, r, total_holes_bef, total_blocking_bloks_bef)
                if result[0]:
                    rating = self.agent.evaluateOption(result[1:N_GENES+1])
                    if best_rating <= rating:
                        best_rating = rating
                        best_move['x'] = x
                        best_move['r'] = r
        
        return best_move

    def calc_move_info(self, board, piece, x, r, total_holes_bef, total_blocking_bloks_bef):
        """Calculate informations based on the current play"""

        piece['rotation'] = r
        piece['y']        = 0
        piece['x']        = x

        # Check if it's a valid position
        if (not self.is_valid_position(board, piece)):
            return [False]

        # Goes down the piece while it's a valid position
        while self.is_valid_position(board, piece, adj_X=0, adj_Y=1):
            piece['y']+=1

        # Create a hypothetical board
        new_board = self.get_blank_board()
        for x2 in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                new_board[x2][y] = board[x2][y]

        # Add the piece to the new_board
        self.add_to_board(new_board, piece)

        # Calculate the sides in contact
        piece_sides, floor_sides, wall_sides = self.calc_sides_in_contact(board, piece)

        # Calculate removed lines
        num_removed_lines = self.remove_complete_lines(new_board)

        total_blocking_block = 0
        total_holes          = 0
        max_height           = 0
        bumpiness            = 0

        for x2 in range(0, BOARDWIDTH):
            b = self.calc_heuristics(new_board, x2)
            total_holes += b[0]
            total_blocking_block += b[1]
            max_height += b[2]

        new_holes           = total_holes - total_holes_bef
        new_blocking_blocks = total_blocking_block - total_blocking_bloks_bef

        b1 = self.calc_heuristics(new_board, 0)
        for x2 in range(1, BOARDWIDTH):
            b2 = self.calc_heuristics(new_board, x2)
            bumpiness += abs(b2[3] - b1[3])
            b1 = b2

        # Create a hypothetical board
        new_board = self.get_blank_board()
        for x2 in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                new_board[x2][y] = board[x2][y]
        # Add the piece to the new_board
        self.add_to_board(new_board, piece)
        left_empty_blocks, right_empty_blocks = self.calc_empty_side_blocks(new_board)
        return [True,
                max_height,
                num_removed_lines,
                new_holes,
                new_blocking_blocks,
                piece_sides,
                floor_sides,
                wall_sides,
                left_empty_blocks,
                right_empty_blocks,
                bumpiness,
            ]

    def calc_initial_move_info(self, board):
        total_holes          = 0
        total_blocking_bocks = 0

        for x2 in range(0, BOARDWIDTH):
            b = self.calc_heuristics(board, x2)

            total_holes          += b[0]
            total_blocking_bocks += b[1]

        return total_holes, total_blocking_bocks

    def calc_heuristics(self, board, x):
        """Calculate heuristics

        The heuristics are composed by: number of holes, number of blocks above
        hole and maximum height.

        """
        total_holes        = 0
        locals_holes       = 0
        blocks_above_holes = 0
        is_hole_exist      = False
        sum_heights        = 0
        max = 0

        for y in range(BOARDHEIGHT-1, -1,-1):
            if board[x][y] == BLANK:
                locals_holes += 1
            else:
                sum_heights += BOARDHEIGHT-y
                if max < BOARDHEIGHT-y:
                    max = BOARDHEIGHT-y

                if locals_holes > 0:
                    total_holes += locals_holes
                    locals_holes = 0

                if total_holes > 0:
                    blocks_above_holes += 1

        return total_holes, blocks_above_holes, sum_heights, max

    def calc_sides_in_contact(self, board, piece):
        """Calculate sides in contacts"""

        piece_sides = 0
        floor_sides = 0
        wall_sides  = 0

        for Px in range(TEMPLATEWIDTH):
            for Py in range(TEMPLATEHEIGHT):

                # Wall
                if not PIECES[piece['shape']][piece['rotation']][Py][Px] == BLANK: # Quadrant is part of the piece
                    if piece['x']+Px == 0 or piece['x']+Px == BOARDWIDTH-1:
                        wall_sides += 1

                    if piece['y']+Py == BOARDHEIGHT-1:
                        floor_sides += 1
                    else:
                    # For other parts in the template outline:
                        if Py == TEMPLATEHEIGHT-1 and not board[piece['x']+Px][piece['y']+Py+1] == BLANK:
                            piece_sides += 1

                    # the edges of the template are colored: check if there are pieces on their side
                    if Px == 0 and piece['x']+Px > 0 and not board[piece['x']+Px-1][piece['y']+Py] == BLANK:
                            piece_sides += 1

                    if Px == TEMPLATEWIDTH-1 and piece['x']+Px < BOARDWIDTH -1 and not board[piece['x']+Px+1][piece['y']+Py] == BLANK:
                            piece_sides += 1

                # Other pieces in general
                elif piece['x']+Px < BOARDWIDTH and piece['x']+Px >= 0 and piece['y']+Py < BOARDHEIGHT and not board[piece['x']+Px][piece['y']+Py] == BLANK:  #quadrante do tabuleiro colorido mas nao do template

                    # The empty quadrant of the template is colored on the board
                    if not PIECES[piece['shape']][piece['rotation']][Py-1][Px] == BLANK:
                        piece_sides += 1

                    if Px > 0 and not PIECES[piece['shape']][piece['rotation']][Py][Px-1] == BLANK:
                        piece_sides += 1

                    if Px < TEMPLATEWIDTH-1 and not PIECES[piece['shape']][piece['rotation']][Py][Px+1] == BLANK:
                        piece_sides += 1

                        #(there can be no pieces on top)

        return  piece_sides, floor_sides, wall_sides
  
    def calc_empty_side_blocks(self, board):
        """
            Calculate number of empty blocks on both left and right sides till min height, 
        """
        # calculate left side
        left_empty_rows = 0
        for y in range(BOARDHEIGHT-1, -1, -1):
            full = True
            for x in range(1, BOARDWIDTH):
                #is line not full?
                if board[x][y] == BLANK:
                    full = False
                    break;
            if full and board[0][y] == BLANK:
                left_empty_rows +=1
            else:
                break;
        #calculate right side
        right_empty_rows = 0
        for y in range(BOARDHEIGHT-1, -1, -1):
            full = True
            for x in range(0, BOARDWIDTH-1):
                #is line not full?
                if board[x][y] == BLANK:
                    full = False
                    break;
            if full and board[BOARDWIDTH-1][y] == BLANK:
                right_empty_rows +=1
            else:
                break;
        return left_empty_rows, right_empty_rows
#endregion

class GameEngine:
    def __init__(self, n_envs = 3, max_cols = 3, side_panel_width=200) -> None:
        global FPSCLOCK, BASICFONT, BIGFONT
        pygame.init()

        FPSCLOCK    = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        BIGFONT     = pygame.font.Font('freesansbold.ttf', 100)
        self.sidepanel_font     = pygame.font.Font('freesansbold.ttf', 16)
        self.cols = max_cols if max_cols < n_envs else n_envs
        self.rows = n_envs // max_cols + (n_envs % max_cols > 0)
        pygame.display.set_caption('Tetris AI')
        self.env_width = (WINDOWWIDTH - side_panel_width) // self.cols
        self.env_height = WINDOWHEIGHT // self.rows
        self.side_panel_width = side_panel_width
        self.side_panel_surf = pygame.Surface((side_panel_width, WINDOWHEIGHT))

        BASICFONT   = pygame.font.Font('freesansbold.ttf',int(34 * (self.env_width / Environment.BASIC_WIDTH)))

        self.env_panel = pygame.Surface((WINDOWWIDTH - side_panel_width, WINDOWHEIGHT))
        self.environments = [Environment(self.env_width, self.env_height) for _ in range(n_envs)]
        self.can_continue = [True for _ in range(n_envs)]
        self.side_panel_data = {}

        self.paused = False

    def reset_envs(self, new_pieces = [], agents : list[Agent] = []):
        for idx, env in enumerate(self.environments):
            env.reset(new_pieces, agents[idx] if idx < len(agents) else None)
            self.can_continue[idx] = True

    def get_new_pieces(self, n_pieces):
        pieces = []
        for i in range(n_pieces):
            shape     = random.choice(list(PIECES.keys()))
            new_piece = {'shape': shape,
                        'rotation': random.randint(0, len(PIECES[shape]) - 1),
                        'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                        'y': -2, # start it above the board (i.e. less than 0)
                        'color': random.randint(0, len(COLORS)-1)}
            pieces.append(new_piece)
        return pieces
    
    def propagate_events(self):
        for event in pygame.event.get([KEYUP, KEYDOWN, QUIT]):
            if event.type == QUIT or event.key == K_ESCAPE:
                self.terminate()
                return
            if (event.type == KEYUP and event.key == K_p):
                self.paused = not self.paused
            for env in self.environments:
                env.event_queue.append(event)

    def terminate(self):
        pygame.quit()
        sys.exit()

    def render_side_panel(self):
        # Fill the side panel surface with a color
        self.side_panel_surf.fill((11, 11, 11))

        # Render and blit custom data onto the side panel surface
        if self.side_panel_data:
            y_offset = 100  # Starting Y offset for custom data
            for key, value in self.side_panel_data.items():
                data_text = f"{key}: {value}"
                data_surf = self.sidepanel_font.render(data_text, True, (255, 255, 255))
                data_rect = data_surf.get_rect(center=(self.side_panel_width // 2, y_offset))
                self.side_panel_surf.blit(data_surf, data_rect)
                y_offset += 30  # Increment Y offset for next data
        # Blit the side panel onto the main display surface
        self.DISPLAYSURF.blit(self.side_panel_surf, (WINDOWWIDTH - self.side_panel_width, 0))

    def run_envs(self, max_turns, agents=[], has_same_pieces=True):
        if has_same_pieces:
            self.reset_envs(self.get_new_pieces(max_turns), agents)
        else:
            self.reset_envs([], agents)

        while True:
            self.env_panel.fill((0, 0, 0))  # Clear the main display surface
            found = False                   # found env that is still running
            self.propagate_events()
            if self.paused:
                continue

            for idx, env in enumerate(self.environments):
                if self.can_continue[idx]:
                    found = True
                    self.can_continue[idx] = env.step()  # Perform environment step
                    if env.turns > max_turns:
                        self.can_continue[idx] = False
                
                row = idx // self.cols
                col = idx % self.cols

                # Blit the scaled environment onto the env_panel
                self.env_panel.blit(env.root, (col * self.env_width, row * self.env_height))  

            self.DISPLAYSURF.blit(self.env_panel, (0, 0))  # Blit env_panel onto display
            self.render_side_panel()  # Render side panel
            pygame.display.update()  # Update display
            FPSCLOCK.tick(FPS)  # Cap frame rate

            if not found:
                pygame.time.delay(1500)
                break
