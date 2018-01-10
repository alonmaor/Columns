import columns_logic
import pygame
import random
import time

ROWS = 12
COLS = 6
WHITE = (255, 255, 255)
BLACK = (0, 0,0 )
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 150, 0)
PINK = (255, 50, 255)
GREY = (128, 128, 128)
PURPLE = (100, 0, 200)
DARKBLUE = (150, 0, 0)
BROWN = (100, 50, 0)
GOLD = (204, 204, 0)
COLORS = {'A': RED, 'B': BLUE, 'C': GREEN, 'D': YELLOW, 'E': ORANGE,
          'F': PINK, 'G': GREY, 'H': PURPLE, 'I': DARKBLUE, 'J': BROWN, ' ': WHITE}


class ColumnsGame:
    def __init__(self):
        self._running = True
        self._state = columns_logic.Columns(ROWS,COLS)
        self._screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
        self._width = 600
        self._height = 600
        self._current_faller = columns_logic.Faller(0, [])
        self._clock = pygame.time.Clock()
        self._clock_counter = 0
        self._events_clock = 0
        #self._land_sound = pygame.mixer.Sound('SoftDrop.OGG')

    def run(self) -> None:
        '''the entire running of the game'''
        pygame.init()

        col, faller = self._produce_col(), self._produce_faller()
        self._current_faller = columns_logic.Faller(col, faller)
        while self._running:
            self._clock.tick(30)
            self._clock_counter += 1
            self._events_clock += 1

            if self._state.is_gameover(self._current_faller):
                self._end_game()

            if self._current_faller.is_frozen():
                if self._state.get_any_matches():
                    time.sleep(0.5)
                    self._state.erase_matches()
                else:
                    col, faller = self._produce_col(), self._produce_faller()
                    self._current_faller = columns_logic.Faller(col, faller)
            else:

                #elif self._current_faller.is_landed():
                    #pygame.mixer.Sound.play(self._land_sound)

                if self._clock_counter == 15:
                    self._state.move_down(self._current_faller)
                    self._clock_counter = 0

            if self._events_clock % 2 == 0:
                self._handle_events()
            self._redraw()

        self._game_over()

    def _handle_events(self) -> None:
        '''handles events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)

        self._handle_keys()

    def _handle_keys(self) -> None:
        '''handles the keys that been pushed'''
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self._move_faller_left()

        if keys[pygame.K_RIGHT]:
            self._move_faller_right()

        if keys[pygame.K_SPACE]:
            self._rotate_faller()

    def _move_faller_left(self) -> None:
        '''moves the faller left'''
        self._state.move_left(self._current_faller)

    def _move_faller_right(self) -> None:
        '''move the faller right'''
        self._state.move_right(self._current_faller)

    def _rotate_faller(self) -> None:
        '''rotates the faller'''
        self._state.rotate(self._current_faller)
                           
    def _resize_surface(self, size: (int, int)) -> None:
        '''resizes the surface size'''
        self._screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        self._width = size[0]
        self._height = size[1]

    def _redraw(self) -> None:
        '''redraws the surface'''
        self._screen.fill(WHITE)
        self._draw_blocks()
        self._draw_grid()
        pygame.display.flip()
        
    def _draw_grid(self) -> None:
        '''draws the grid'''
        tile_width = int(self._width/COLS)
        tile_height = int(self._height/ROWS)

        for x in range(tile_width, self._width, tile_width):
            pygame.draw.line(self._screen, BLACK, (x, 0), (x, self._height),5)
        for y in range(tile_height, self._height, tile_height):
            pygame.draw.line(self._screen, BLACK, (0, y), (self._width, y),5)

    def _draw_blocks(self) -> None:
        '''draws the blocks on the board'''
        tile_width = int(self._width/COLS)
        tile_height = int(self._height/ROWS)
        board = self._state.get_game_board()
        for col in range(0, COLS):
            for row in range(0, ROWS):
                jewel = board[col][row]
                jewel_status = jewel[1]
                if jewel_status == 'f' or jewel_status == 'fr':
                    color_letter = jewel[0]
                    pygame.draw.rect(self._screen, COLORS[color_letter],
                    pygame.Rect(col*tile_width, row*tile_height, tile_width,tile_height))
                elif jewel_status == 'l':
                    pygame.draw.rect(self._screen, BLACK,
                    pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height))
                elif jewel_status == 'm':
                    pygame.draw.rect(self._screen, GOLD,
                    pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height))
                                 
    def _produce_col(self) -> int:
        '''produces a random number from 0-5 for column'''
        return int(random.random()*6+1)-1

    def _produce_faller(self) -> list:
        '''produces a new random faller'''
        letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        faller = random.choices(letter_list, k = 3)

        return faller

    def _game_over(self) -> None:
        '''displays a game over message and ends the game'''
        self._screen.fill(pygame.Color(0,0,0))
        self._display_message('GAME OVER!')
        pygame.display.update()
        time.sleep(3)
        pygame.quit()

    def _display_message(self, message: str) -> None:
        '''displays a message on the screen'''
        text = pygame.font.Font('ka1.ttf', 50)
        text_surface, text_rect = self._text_objects(message, text)
        text_rect.center = (self._width/2, self._height/2)
        self._screen.blit(text_surface, text_rect)

    def _text_objects(self, message: str, font: pygame.font.Font) -> (pygame.Surface, pygame.Rect):
        '''creates a recrangle object with the text to display on screen'''
        text_surface = font.render(message, True, WHITE)
        return text_surface, text_surface.get_rect()

    def _end_game(self) -> None:
        self._running = False


if __name__ == '__main__':
    ColumnsGame().run()
