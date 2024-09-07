import random
import gspread
from google.oauth2.service_account import Credentials
import string
import os

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

# Function to pause and clear the screen
def pause():
  input(bcolors.OKCYAN + "\nPress Enter to continue..." + bcolors.ENDC)
  os.system('cls' if os.name == 'nt' else 'clear') # Clear the screen
    
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

# Function to get valid target coordinates
def get_target(board):
    while True:
        try:
            row_letter = input("Enter row (A-{}). ".format(chr(ord('A') + len(board) - 1))).upper()
            row = string.ascii_uppercase.index(row_letter.upper())
            col = int(input("Enter column (1-{}). ".format(len(board)))) - 1
            if 0 <= row < len(board) and 0 <= col < len(board[0]):
                return row, col
            else:
                print("Invalid coordinates. Please enter numbers within the board size.")
        except ValueError:
            print("Invalid input. Please enter letters for Rows and numbers for columns.")

# Function to handle player's turn
def player_turn(player_board, computer_board, computer_ships, score):
    print(bcolors.OKBLUE + "\nYour turn:" + bcolors.ENDC)
    display_boards(player_board, computer_board)
    row, col = get_target(computer_board)

    if (row, col) in computer_ships:
        computer_board[row][col] = 'X'  
        computer_ships.remove((row, col))
        score += 1
        print(bcolors.OKGREEN + "Hit! Target: " + chr(ord('A') + row) + " " + str(col + 1) + bcolors.ENDC)
    else:
        computer_board[row][col] = 'M' 
        print(bcolors.FAIL + "Miss! Target: " + chr(ord('A') + row) + " " + str(col + 1) + bcolors.ENDC)
    print(bcolors.OKCYAN + "\nScore: " + bcolors.ENDC + str(score))
    return computer_board, computer_ships, score
# Function to handle computer's turn
def computer_turn(player_board, player_ships, score):
    print(bcolors.OKCYAN + "\nComputer's turn:" + bcolors.ENDC)
    while True:
        row = random.randint(0, len(player_board) - 1)
        col = random.randint(0, len(player_board[0]) - 1)
        if (row, col) in player_ships:
            player_board[row][col] = 'X' 
            player_ships.remove((row, col))
            score += 1
            print(bcolors.OKGREEN + "Computer hit! Target: " + chr(ord('A') + row) + " " + str(col + 1) + bcolors.ENDC)
            break
        else:
            player_board[row][col] = 'M' 
            print(bcolors.FAIL + "Computer missed! Target: " + chr(ord('A') + row) + " " + str(col + 1) + bcolors.ENDC)
            break
    pause() # Call the pause function after the computer's turn
    return player_board, player_ships, score

# Function to handle the game loop
def play_game():
    welcome_message()
    display_high_scores()
    board_size = get_board_size()
    player_board, computer_board = create_boards(board_size)
    player_ships = place_ships(player_board, 5)  # 5 ships of length 1
    computer_ships = place_ships(computer_board, 5)
    player_score = 0
    computer_score = 0
    while player_ships and computer_ships:
        computer_board, computer_ships, player_score = player_turn(player_board, computer_board, computer_ships, player_score)
        if not computer_ships:
            break
        player_board, player_ships, computer_score = computer_turn(player_board, player_ships, computer_score)
    print("\nFinal Score:")
    print(f"Player: {player_score}")
    print(f"Computer: {computer_score}")
    if player_score > computer_score:
        print(bcolors.OKGREEN + "\nCongratulations! You win!" + bcolors.ENDC)
        save_to_high_scores(player_score)
    else:
        print(bcolors.FAIL + "\nYou lose! Better luck next time." + bcolors.ENDC)

# Function to handle saving scores to the spreadsheet
def save_to_high_scores(score):
    while True:
        save_score = input("Do you want to save your score to the high scores? (y/n): ")
        if save_score.lower() == 'y':
            name = input("Enter your name: ")
            SHEET.append_row([name, score])
            print("Score saved successfully!")
            display_high_scores()
            break
        elif save_score.lower() == 'n':
            print("Score not saved.")
            display_high_scores()
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

# Main function to run the game
if __name__ == "__main__":
    play_game()