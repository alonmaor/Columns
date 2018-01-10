# Name: Alon Maor, ID: 43549105


import columns_logic


def user_interface() -> bool:
    '''manages the user inputs'''
    rows = int(input())
    cols = int(input())
    game = columns_logic.Columns(rows, cols)

    begin_field = input()
    if begin_field == 'CONTENTS':
        for row in range(rows):
            content = input()
            game.set_contents(content, row)

    running = True

    faller = columns_logic.Faller(0, [])
    while running:
        _print_board(game)

        if game.is_gameover(faller):
            print('GAME OVER')
            return 0

        if game.get_any_matches():
            game.erase_matches()
        user_input = input()

        if user_input == '':
            game.move_down(faller)

        elif user_input == 'R':
            if not faller.is_frozen():
                game.rotate(faller)

        elif user_input == '<':
            game.move_left(faller)

        elif user_input == '>':
            game.move_right(faller)

        else:
            if user_input == 'Q':
                return 0

            input_list = user_input.split()
            if input_list[0] == 'F':
                col = int(input_list[1])-1
                jewels = input_list[2:]
                faller = columns_logic.Faller(col, jewels)
                game.move_down(faller)


def _print_board(game: columns_logic.Columns) -> None:
    '''prints out the board'''
    dash = '---'
    board = game.get_game_board()
    for row in range(game.get_rows()):
        print('|', end='')
        for col in range(game.get_cols()):
            jewel = board[col][row]
            if jewel[0] == ' ':
                print('   ', end ='')
            else:
                if jewel[1] == 'fr':
                    print(' ' + board[col][row][0], end=' ')
                elif jewel[1] == 'f':
                    print('[' + board[col][row][0] + ']', end='')
                elif jewel[1] == 'm':
                    print('*' + board[col][row][0] + '*', end='')
                else:
                    print('|' + board[col][row][0] + '|', end='')
        print('|')
    print(' ' + game.get_cols()*dash + ' ')


if __name__ == '__main__':
    user_interface()
