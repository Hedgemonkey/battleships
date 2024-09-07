import random
import gspread
from google.oauth2.service_account import Credentials
import string

# Set up Google Sheets API Credentials
SCOPE = [
  "https://www.googleapis.com/auth/spreadsheets",
  "https://www.googleapis.com/auth/drive.file",
  "https://www.googleapis.com/auth/drive"
  ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('battleship_scores').sheet1

# Colors for console output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Function to display the welcome message with colors
def welcome_message():
    print(bcolors.HEADER + bcolors.BOLD + "\nWelcome to Battleships!\n" + bcolors.ENDC)

# Function to display top 5 high scores
def display_high_scores():
    print(bcolors.OKCYAN + "\nTop 5 Highest Scores: (Lower Number is better)" + bcolors.ENDC)
    scores = SHEET.get_all_values()
    for i in range(2, 7):
        if i <= len(scores):
            print(f"{i}. {scores[i-1][0]}: {scores[i-1][1]}")
        else:
            print(f"{i}. N/A")

# Function to get valid board size input
def get_board_size():
    while True:
        try:
            size = int(input("Choose board size (5-10): "))
            if 5 <= size <= 10:
                return size
            else:
                print("Invalid size. Please enter a number between 5 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to create and initialize boards
def create_boards(size):
    player_board = [['O' for _ in range(size)] for _ in range(size)]
    computer_board = [['O' for _ in range(size)] for _ in range(size)]
    return player_board, computer_board
    
# Function to place ships randomly
def place_ships(board, num_ships):
    ship_locations = []
    for _ in range(num_ships):
        while True:
            row = random.randint(0, len(board) - 1)
            col = random.randint(0, len(board[0]) - 1)
            if board[row][col] == 'O':
                board[row][col] = 'S'
                ship_locations.append((row, col))
                break
    return ship_locations

# Function to display both boards side by side with colors and spacing
def display_boards(player_board, computer_board):
    board_size = len(player_board)
    header_spacing = board_size
    if board_size == 9:
        header_spacing -= 1
    elif board_size == 8:
        header_spacing -= 2
    elif board_size == 7:
        header_spacing -= 3
    elif board_size == 6:
        header_spacing -= 4
    elif board_size == 5:
        header_spacing -= 5
    print("\nPlayer Board  " + " "*header_spacing + " |  Computer Board")
    header_length = len("Player Board") + len("Computer Board") + 3  # 3 for spaces
    spacing = 0
    if board_size < 10:
        spacing += 1
    print(spacing)
    print("   " + " ".join([str(i) for i in range(1, board_size + 1)]) + " "*spacing + "  |" + "    " + " ".join([str(i) for i in range(1, board_size + 1)]) + "  ")
    letters = list(string.ascii_uppercase[:board_size])
    for i in range(board_size):
        player_row = ' '.join(player_board[i])
        computer_row = ' '.join(computer_board[i])
        print(f"{letters[i]:<2} {player_row:<{len(player_row) + 2}} | {letters[i]:<2} {computer_row:<{len(player_row) + 2}}")

player_board, computer_board = create_boards(5)
player_ships = place_ships(player_board, 5)  # 5 ships of length 1
computer_ships = place_ships(computer_board, 5)
display_boards(player_board, computer_board)