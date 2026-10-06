def print_board(board):
    print("-------------")
    for i in range(3):
        print(f"| {board[i*3]} | {board[i*3 + 1]} | {board[i*3 + 2]} |")
        print("-------------")

def check_win(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # columns
        [0, 4, 8], [2, 4, 6]             # diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

def check_draw(board):
    return " " not in board

def play_game():
    board = [" " for _ in range(9)]
    current_player = "X"

    print("Welcome to Tic-Tac-Toe (XO)!")
    print("Positions are 1-9, starting from top-left to bottom-right.")
    print_board(board)

    while True:
        try:
            move = int(input(f"Player {current_player}, enter your move (1-9): ")) - 1
            if move < 0 or move > 8 or board[move] != " ":
                print("Invalid move. Try again.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")
            continue

        board[move] = current_player
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    play_game()
