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
    print(bcolors.OKCYAN + "\nTop 5 Lowest Misses:" + bcolors.ENDC)
    scores = SHEET.get_all_values()
    # Sort by the score (second column, index 1)
    sorted_scores = scores[1:]  # Ignore the first row (header)
    sorted_scores.sort(key=lambda x: int(x[1]))  # Sort based on the score column (index 1)
    for i in range(1, 6):  # Start the loop from 1
        if i <= len(sorted_scores):  # Use sorted_scores for indexing
            print(f"{i}. {sorted_scores[i-1][0]}: {sorted_scores[i-1][1]}")
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
        player_row = []
        computer_row = []
        for j in range(board_size):
            if player_board[i][j] == 'X':
                player_row.append(bcolors.FAIL + 'X' + bcolors.ENDC)  # Red 'X' for hit
            elif player_board[i][j] == 'S':
                player_row.append(bcolors.OKBLUE + 'S' + bcolors.ENDC)  # Blue 'S' for ship
            elif player_board[i][j] == 'M':
                player_row.append(bcolors.OKGREEN + 'M' + bcolors.ENDC)  # Green 'M' for miss
            else:
                player_row.append(player_board[i][j])
            if computer_board[i][j] == 'X':
                computer_row.append(bcolors.FAIL + 'X' + bcolors.ENDC)  # Red 'X' for hit
            elif computer_board[i][j] == 'S':
                computer_row.append(bcolors.OKBLUE + 'S' + bcolors.ENDC)  # Blue 'S' for ship
            elif computer_board[i][j] == 'M':
                computer_row.append(bcolors.OKGREEN + 'M' + bcolors.ENDC)  # Green 'M' for miss
            else:
                computer_row.append(computer_board[i][j])
        player_row_str = ' '.join(player_row)
        computer_row_str = ' '.join(computer_row)
        print(f"{letters[i]:<2} {player_row_str:<{len(player_row_str) + 2}} | {letters[i]:<2} {computer_row_str:<{len(player_row_str) + 2}}")

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
def player_turn(player_board, computer_board, computer_ships, misses):
    print(bcolors.OKBLUE + "\nYour turn:" + bcolors.ENDC)
    display_boards(player_board, computer_board)
    row, col = get_target(computer_board)
    if (row, col) in computer_ships:
        computer_board[row][col] = 'X'  
        computer_ships.remove((row, col))
        print(bcolors.OKGREEN + "Hit! Target: " + chr(ord('A') + row) + " " + str(col + 1) + bcolors.ENDC)
    else:
        computer_board[row][col] = 'M' 
        print(bcolors.FAIL + "Miss! Target: " + chr(ord('A') + row) + " " + str(col + 1) + bcolors.ENDC)
        misses += 1  # Increment misses on miss
    print(bcolors.OKCYAN + "\nMisses: " + bcolors.ENDC + str(misses))
    return computer_board, computer_ships, misses
# Function to handle computer's turn
def computer_turn(player_board, player_ships, misses):
    print(bcolors.OKCYAN + "\nComputer's turn:" + bcolors.ENDC)
    while True:
        row = random.randint(0, len(player_board) - 1)
        col = random.randint(0, len(player_board[0]) - 1)
        if (row, col) in player_ships:
            player_board[row][col] = 'X' 
            player_ships.remove((row, col))
            print(bcolors.OKGREEN + "Computer hit! Target: " + chr(ord('A') + row) + " " + str(col + 1) + bcolors.ENDC)
            break
        else:
            player_board[row][col] = 'M' 
            print(bcolors.FAIL + "Computer missed! Target: " + chr(ord('A') + row) + " " + str(col + 1) + bcolors.ENDC)
            misses += 1  # Increment misses on miss
            break
    pause() # Call the pause function after the computer's turn
    return player_board, player_ships, misses
# Function to handle the game loop
def play_game():
    while True:  # Loop for playing multiple games
        welcome_message()
        display_high_scores()
        board_size = get_board_size()
        pause() # Call pause after board size is chosen
        player_board, computer_board = create_boards(board_size)
        player_ships = place_ships(player_board, 5)  # 5 ships of length 1
        computer_ships = place_ships(computer_board, 5)
        player_misses = 0
        computer_misses = 0
        while player_ships and computer_ships:
            computer_board, computer_ships, player_misses = player_turn(player_board, computer_board, computer_ships, player_misses)
            if not computer_ships:  # Check if computer ships are empty
                print(bcolors.OKGREEN + "\nCongratulations! You win!" + bcolors.ENDC)
                save_to_high_scores(player_misses)
                break # Exit the inner loop if the player wins
            player_board, player_ships, computer_misses = computer_turn(player_board, player_ships, computer_misses)
            if not player_ships:  # Check if player ships are empty
                print(bcolors.FAIL + "\nYou lose! Better luck next time." + bcolors.ENDC)
                break # Exit the inner loop if the player loses
        print("\nFinal Score:")
        print(f"Player: {player_misses}")
        print(f"Computer: {computer_misses}")
        
        while True:  # Loop for validating play again input
            play_again = input("\nPlay again? (y/n): ").lower()  # Convert input to lowercase
            if play_again in ('y', 'n'):
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        if play_again == 'n':
            print("Goodbye!")
            break  # Exit the game loop
# Function to handle saving scores to the spreadsheet
def save_to_high_scores(misses):
    while True:
        save_score = input("Do you want to save your score to the high scores? (y/n): ")
        if save_score.lower() == 'y':
            name = input("Enter your name: ")
            SHEET.append_row([name, misses])
            os.system('cls' if os.name == 'nt' else 'clear') # Clear the screen
            print("Score saved successfully!")
            display_high_scores()
            break
        elif save_score.lower() == 'n':
            os.system('cls' if os.name == 'nt' else 'clear') # Clear the screen
            print("Score not saved.")
            display_high_scores()
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

# Main function to run the game
if __name__ == "__main__":
    play_game()