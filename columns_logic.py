# Name: Alon Maor, ID: 43549105


class Faller:
    '''containts all the attributes of the faller'''
    def __init__(self, col: int, jewels: list):
        '''initialized new Faller objects'''
        self._current_pos = (col, -1)
        self._faller = jewels
        self._counter = 0
        self._frozen = False
        self._landed = False

    def get_current_pos(self) -> (int, int):
        '''returns the current position of the bottom jewel of the faller'''
        return self._current_pos

    def set_current_pos(self, new_pos: (int, int)):
        '''sets the new position of the faller in the board'''
        self._current_pos = new_pos

    def get_faller(self) -> list:
        '''getter function for the current faller'''
        return self._faller

    def set_faller(self, new_faller: list) -> None:
        '''sets the values to the new faller'''
        self._faller = new_faller

    def set_counter(self) -> None:
        '''increments every time a jewel of the faller has entered the board'''
        self._counter += 1

    def get_counter(self) -> int:
        '''returns the count of how many jewel of the faller are within the board'''
        return self._counter

    def set_frozen(self) -> None:
        '''sets the faller status to frozen'''
        self._frozen = True

    def is_frozen(self) -> bool:
        '''returns whether the faller has frozen'''
        return self._frozen

    def set_landed(self) -> None:
        '''sets the faller status to landed'''
        self._landed = True

    def is_landed(self) -> None:
        '''returns whether the faller has landed'''
        return self._landed


class Columns:
    '''Class for the game of columns with all its attributes'''
    def __init__(self, rows: int, cols: int):
        '''initialized new Columns objects'''
        self._rows = rows
        self._cols = cols
        self._board_game = []
        self._any_matches = False
        for col in range(cols):
            temp = []
            for row in range(rows):
                temp.append([' ', ''])
            self._board_game.append(temp)

    def set_contents(self, content: str, row: int) -> None:
        '''Sets that initial contents requested by the user'''
        for i in range(len(content)):
            self._board_game[i][row][0] = content[i]
            if content[i] == ' ':
                self._board_game[i][row][1] = ''
            else:
                self._board_game[i][row][1] = 'fr'

    def get_any_matches(self) -> bool:
        return self._any_matches

    def get_rows(self) -> int:
        '''getter function for number of rows on the board'''
        return self._rows

    def get_cols(self) -> int:
        '''getter function for number of columns on the board'''
        return self._cols

    def get_game_board(self) -> list:
        '''a getter function for the game board'''
        return self._board_game

    def is_gameover(self, faller: Faller) -> bool:
        '''checks if there are any jewels outside of the board - if so game is over'''
        count = faller.get_counter()
        return count < 3 and faller.is_landed()

    def move_down(self, faller: Faller) -> None:
        '''Handles all the situations where the faller has moves down'''
        col, row = faller.get_current_pos()
        if row+1 < self._rows and self._board_game[col][row+1][0] == ' ':
            self._handle_drop(faller, row, col)

        elif faller.is_landed():
            if not self.is_gameover(faller):
                self._handle_frozen(faller, row, col)
                self._check_matches(faller)

        else:
            self._handle_landed(faller, row, col)

    def move_left(self, faller: Faller) -> None:
        '''moves the faller to the left'''
        col, row = faller.get_current_pos()
        if col > 0 and self._check_move(faller, -1):
            faller.set_current_pos((col-1,row))
            self._set_board(faller)
            self._handle_old_pos((col, row))

    def move_right(self, faller: Faller) -> None:
        '''moves the faller to the right'''
        col, row = faller.get_current_pos()
        if col+1 < self._cols and self._check_move(faller, 1):
            faller.set_current_pos((col+1,row))
            self._set_board(faller)
            self._handle_old_pos((col, row))

    def rotate(self, faller: Faller) -> None:
        '''rotates the jewels in the faller'''
        current_faller = faller.get_faller()
        temp = current_faller.pop()
        current_faller.insert(0,temp)
        faller.set_faller(current_faller)
        self._set_board(faller)

    def erase_matches(self) -> None:
        for col in range(self._cols):
            for row in range(self._rows):
                if self._board_game[col][row][1] == 'm':
                    self._handle_erase(col, row)
                    row -= 1

        self._any_matches = False

    def _handle_drop(self, faller: Faller, row: int, col: int) -> None:
        '''handles the drop of the faller'''
        current_faller = faller.get_faller()

        for i in range(3):
            if row - i > -2:
                self._board_game[col][row + 1 - i][0] = current_faller[2 - i]
                self._board_game[col][row + 1 - i][1] = 'f'

        if faller.get_counter() < 3:
            faller.set_counter()

        if row >= 2:
            self._board_game[col][row - 2][0] = ' '

        faller.set_current_pos((col, row + 1))

    def _handle_old_pos(self, old_position: (int, int)) -> None:
        '''erases older position of faller'''
        old_col, old_row = old_position
        for row in range(old_row, old_row-3, -1):
            if row > -1:
                self._board_game[old_col][row][0] = ' '
                self._board_game[old_col][row][1] = ''

    def _handle_landed(self, faller: Faller, row: int, col: int) -> None:
        '''handles the situation when the faller has landed'''
        faller.set_landed()
        count = faller.get_counter()

        for i in range(row, row - count, -1):
            self._board_game[col][i][1] = 'l'

    def _handle_frozen(self, faller: Faller, row: int, col: int) -> None:
        '''handles the frozen faller by setting its status'''
        faller.set_frozen()
        for i in range(row, row - 3, -1):
            self._board_game[col][i][1] = 'fr'

    def _set_board(self, faller: Faller) -> None:
        '''sets the faller position on the board'''
        col, row = faller.get_current_pos()
        current_faller = faller.get_faller()
        for i in range(3):
            if row - i > -1:
                self._board_game[col][row - i][0] = current_faller[2 - i]
                self._board_game[col][row - i][1] = 'f'

    def _check_move(self, faller: Faller, side: int) -> bool:
        '''check if there is a space on the left to move the faller'''
        col, row = faller.get_current_pos()
        col += side
        for i in range(3):
            if row-i > -1 and self._board_game[col][row-i][0] != ' ':
                return False

        return True

    def _check_matches(self, faller: Faller) -> None:
        '''checks for matches in the given faller'''
        col, row = faller._current_pos
        for i in range(3):
            self._check_jewel_matches(col, row-i)

    def _check_jewel_matches(self, col, row) -> None:
        '''checks for matches around the given jewel'''
        left_count = self._check_direction(col, row, (-1, 0))
        up_left_count = self._check_direction(col, row, (-1, 1))
        down_left_count = self._check_direction(col, row, (-1, -1))
        up_count = self._check_direction(col, row, (0, 1))
        down_count = self._check_direction(col, row, (0, -1))
        right_count = self._check_direction(col, row, (1, 0))
        down_right_count = self._check_direction(col, row, (1, -1))
        up_right_count = self._check_direction(col, row, (1, 1))

        if left_count + right_count > 3:
            self._handle_direction(col, row, (left_count, right_count), ((-1, 0), (1, 0)))
            self._any_matches = True

        if up_left_count + down_right_count > 3:
            self._handle_direction(col, row, (up_left_count, down_right_count), ((-1, 1),(1, -1)))
            self._any_matches = True

        if up_count + down_count > 3:
            self._handle_direction(col, row, (up_count, down_count), ((0, 1), (0, -1)))
            self._any_matches = True

        if down_left_count + up_right_count > 3:
            self._handle_direction(col, row, (down_left_count, up_right_count), ((-1, -1), (1, 1)))
            self._any_matches = True

    def _handle_direction(self, col:int, row: int, counts: (int, int), directions: ((int, int), (int, int))) -> None:
        '''handles the matches in specific direction'''
        self._handle_match(col, row, counts[0], directions[0])
        self._handle_match(col, row, counts[1], directions[1])

    def _check_direction(self, col: int,row: int, delta: (int, int)) -> int:
        '''checks how many matches are in a given direction'''
        count = 0
        for i in range(self.get_cols()):
            next_col = col + delta[0]*i
            next_row = row + delta[1]*i
            if self._is_valid(next_col, next_row) and \
                            self._board_game[col][row][0] == self._board_game[next_col][next_row][0]:
                count += 1
            else:
                break

        return count

    def _is_valid(self, col: int, row: int) -> bool:
        '''checks if a given row and column are within the boundaries of the board'''
        if  0 <= col < self._cols and 0 <= row < self._rows:
            return True
        else:
            return False

    def _handle_match(self, col: int, row: int, count: int, delta: (int, int)) -> None:
        '''handles the matches by turning all matching jewels into matching status'''
        for i in range(count):
            next_col = col + delta[0] * i
            next_row = row + delta[1] * i
            self._board_game[next_col][next_row][1] = 'm'

    def _handle_erase(self, col: int, row: int) -> None:
        '''erases the given jewel'''
        board = self._board_game
        board[col][row][0] = ' '
        board[col][row][1] = ''
        for i in range(row, 0, -1):
            board[col][i][0] = board[col][i-1][0]
            board[col][i][1] = board[col][i-1][1]

