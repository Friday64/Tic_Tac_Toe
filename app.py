from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Initialize global variables
board = [' ' for _ in range(9)]  # 3x3 empty board
player_symbol = 'X'
computer_symbol = 'O'
current_player = 'Player'  # Can be 'Player' or 'Computer'

def check_winner():
    """Check if there's a winner or a draw."""
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6],            # Diagonals
    ]
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != ' ':
            return board[combo[0]]  # Return the winner ('X' or 'O')

    if ' ' not in board:
        return 'Draw'  # No spaces left, it's a draw

    return None  # No winner yet

def computer_move():
    """Make a random move for the computer."""
    available_cells = [i for i, cell in enumerate(board) if cell == ' ']
    if available_cells:
        move = random.choice(available_cells)
        board[move] = computer_symbol

@app.route('/')
def player_selection():
    """Allow the player to select X or O."""
    return render_template('player_selection.html')

@app.route('/start', methods=['POST'])
def start_game():
    """Start the game with the selected symbol."""
    global player_symbol, computer_symbol, current_player, board
    player_symbol = request.form['symbol']
    computer_symbol = 'O' if player_symbol == 'X' else 'X'
    board = [' ' for _ in range(9)]  # Reset the board
    current_player = 'Player'  # Player always starts
    return redirect(url_for('game'))

@app.route('/game')
def game():
    """Display the game board."""
    global current_player  # Declare 'current_player' as global before using it
    winner = check_winner()
    if winner is None and current_player == 'Computer':  # If no winner and it's the computer's turn
        computer_move()
        winner = check_winner()
        if winner is None:  # Switch back to Player if no winner
            current_player = 'Player'
    return render_template('game.html', board=board, winner=winner, current_player=current_player)


@app.route('/move/<int:cell>', methods=['POST'])
def make_move(cell):
    """Handle the player's move."""
    global current_player
    if board[cell] == ' ' and not check_winner() and current_player == 'Player':
        board[cell] = player_symbol
        current_player = 'Computer'
    return redirect(url_for('game'))

@app.route('/reset', methods=['POST'])
def reset_game():
    """Reset the game."""
    global board, current_player
    board = [' ' for _ in range(9)]
    current_player = 'Player'
    return redirect(url_for('player_selection'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

