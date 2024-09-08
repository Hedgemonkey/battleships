import random
import gspread
from google.oauth2.service_account import Credentials
import string
import os
import re

"""
Set up Google Sheets API Credentials
"""
SCOPE = [
  "https://www.googleapis.com/auth/spreadsheets",
  "https://www.googleapis.com/auth/drive.file",
  "https://www.googleapis.com/auth/drive"
  ]


CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('battleship_scores').sheet1


def center_text(text):
    """
    Function to center text in the console
    """
    console_width = os.get_terminal_size().columns
    text_length = len(re.sub(r'\x1b\[[0-9;]*m', '', text))
    padding = (console_width - text_length) // 2
    return " " * padding + text + " " * padding


def pause():
    """
    Function to pause and clear the screen
    """
    input("\n" + bcolors.OKCYAN + center_text("Press Enter to continue...") + bcolors.ENDC)
    os.system('cls' if os.name == 'nt' else 'clear')


class bcolors:
    """
    Colors for console output
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[34m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[32m'
    WARNING = '\033[93m'
    RED = '\033[31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def welcome_message():
    """
    Function to display the welcome message with colors
    """
    print(bcolors.HEADER + bcolors.BOLD + center_text("Welcome to Battleships!") + bcolors.ENDC)
    print("\n" + bcolors.BOLD + center_text("Welcome to my simple battleships game!") + bcolors.ENDC)
    print("\n" + bcolors.BOLD + center_text("The aim of the game is to hit your opponents ships in the least trys possible!") + bcolors.ENDC)
    print("\n" + bcolors.BOLD + center_text("Just select a gameboard size between a 5x5 grid and a 9x9 grid!") + bcolors.ENDC)
    print("\n" + bcolors.BOLD + center_text("Then enter the co-ordinates of where you want to shoot when prompted!") + bcolors.ENDC)


def display_high_scores():
    """
    Function to display top 5 high scores
    """
    print("\n" + bcolors.HEADER + center_text("Current High Scores") + bcolors.ENDC)
    print("\n" + bcolors.OKCYAN + center_text("Top 5 Lowest Misses:") + bcolors.ENDC)
    scores = SHEET.get_all_values()
    sorted_scores = scores[1:]
    sorted_scores.sort(key=lambda x: int(x[1]))
    for i in range(1, 6):
        if i <= len(sorted_scores):
            print(center_text(f"{i}. {sorted_scores[i-1][0]}: {sorted_scores[i-1][1]}"))
        else:
            print(f"{i}. N/A")


def get_board_size():
    """
    Function to get valid board size input
    """
    while True:
        try:
            size = int(input("Choose board size (5-9): "))
            if 5 <= size <= 9:
                return size
            else:
                print("Invalid size. Please enter a number between 5 and 9")
        except ValueError:
            print("Invalid input. Please enter a number.")


def create_boards(size):
    """
    Function to create and initialize boards
    """
    player_board = [['O' for _ in range(size)] for _ in range(size)]
    computer_board = [['O' for _ in range(size)] for _ in range(size)]
    return player_board, computer_board


def place_ships(board, num_ships):
    """
    Function to place ships randomly
    """
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


def display_boards(player_board, computer_board):
    """
    Function to display both boards side by side with colors and spacing
    """
    board_size = len(player_board)
    header_spacing = board_size - 3
    if board_size == 6:
        header_spacing -= 1
    elif board_size == 7:
        header_spacing -= 2
    elif board_size == 8:
        header_spacing -= 3
    elif board_size == 9:
        header_spacing -= 4
    print("\n" + center_text(bcolors.RED + "Player Board  " + " "*header_spacing + bcolors.ENDC + " | " + bcolors.RED + " Computer Board" + bcolors.ENDC))
    print("\n" + center_text(bcolors.OKCYAN + "   " + " ".join([str(i) for i in range(1, board_size + 1)]) + " " + bcolors.ENDC + "  |" + "    " + bcolors.OKCYAN + " ".join([str(i) for i in range(1, board_size + 1)]) + "  " + bcolors.ENDC))
    letters = list(string.ascii_uppercase[:board_size])
    for i in range(board_size):
        player_row = []
        computer_row = []
        for j in range(board_size):
            if player_board[i][j] == 'X':
                player_row.append(bcolors.RED + bcolors.BOLD + 'X' + bcolors.ENDC)
            elif player_board[i][j] == 'S':
                player_row.append(bcolors.OKBLUE + bcolors.BOLD + 'S' + bcolors.ENDC)
            elif player_board[i][j] == 'M':
                player_row.append(bcolors.OKGREEN + bcolors.BOLD + 'M' + bcolors.ENDC)
            else:
                player_row.append(player_board[i][j])
            if computer_board[i][j] == 'X':
                computer_row.append(bcolors.RED + bcolors.BOLD + 'X' + bcolors.ENDC)
            elif computer_board[i][j] == 'M':
                computer_row.append(bcolors.OKGREEN + bcolors.BOLD + 'M' + bcolors.ENDC)
            else:
                computer_row.append('O')
        player_row_str = ' '.join(player_row)
        computer_row_str = ' '.join(computer_row)
        row_str = f"{bcolors.OKCYAN}{letters[i]: <2} {bcolors.ENDC}{player_row_str: <{len(player_row_str) + 2}} | {bcolors.OKCYAN}{letters[i]: <2}{bcolors.ENDC} {computer_row_str: <{len(computer_row_str) + 2}}"
        print(center_text(row_str))


def get_target(board):
    """
    Function to get valid target coordinates
    """
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


def player_turn(player_board, computer_board, computer_ships, misses):
    """
    Function to handle player's turn
    """
    print(bcolors.OKBLUE + "\nYour turn:" + bcolors.ENDC)
    display_boards(player_board, computer_board)
    while True:
        row, col = get_target(computer_board)
        if computer_board[row][col] == 'M' or computer_board[row][col] == 'X':
            print(bcolors.WARNING + "You already tried that target. Choose another one.\n" + bcolors.ENDC)
        else:
            if (row, col) in computer_ships:
                computer_board[row][col] = 'X'
                computer_ships.remove((row, col))
                print(bcolors.OKGREEN + "Hit! Target: " + chr(ord('A') + row) + " " + str(col + 1) + bcolors.ENDC)
            else:
                computer_board[row][col] = 'M'
                print(bcolors.RED + "Miss! Target: " + chr(ord('A') + row) + " " + str(col + 1) + bcolors.ENDC)
                misses += 1
            print(bcolors.OKCYAN + "\nMisses: " + bcolors.ENDC + str(misses))
            break
    return computer_board, computer_ships, misses


def computer_turn(player_board, player_ships, misses):
    """
    Function to handle computer's turn
    """
    print(bcolors.OKCYAN + "\nComputer's turn:" + bcolors.ENDC)
    while True:
        row = random.randint(0, len(player_board) - 1)
        col = random.randint(0, len(player_board[0]) - 1)
        if player_board[row][col] == 'M' or player_board[row][col] == 'X':
            continue
        else:
            if (row, col) in player_ships:
                player_board[row][col] = 'X'
                player_ships.remove((row, col))
                print(bcolors.OKGREEN + "Computer hit! Target: " + chr(ord('A') + row) + " " + str(col + 1) + bcolors.ENDC)
                break
            else:
                player_board[row][col] = 'M'
                print(bcolors.RED + "Computer missed! Target: " + chr(ord('A') + row) + " " + str(col + 1) + bcolors.ENDC)
                misses += 1
                break
    pause()
    return player_board, player_ships, misses


def play_game():
    """
    Function to handle the game loop
    """
    while True:
        os.system('cl' if os.name == 'nt' else 'clear')
        welcome_message()
        display_high_scores()
        board_size = get_board_size()
        pause()
        player_board, computer_board = create_boards(board_size)
        player_ships = place_ships(player_board, 5)
        computer_ships = place_ships(computer_board, 5)
        player_misses = 0
        computer_misses = 0
        while player_ships and computer_ships:
            computer_board, computer_ships, player_misses = player_turn(player_board, computer_board, computer_ships, player_misses)
            if not computer_ships:
                print(bcolors.OKGREEN + "\nCongratulations! You win!" + bcolors.ENDC)
                save_to_high_scores(player_misses)
                break
            player_board, player_ships, computer_misses = computer_turn(player_board, player_ships, computer_misses)
            if not player_ships:
                print(bcolors.RED + "\nYou lose! Better luck next time." + bcolors.ENDC)
                break
        print("\nFinal Score:")
        print(f"Player: {player_misses}")
        print(f"Computer: {computer_misses}")

        while True:
            play_again = input("\nPlay again? (y/n): ").lower()
            if play_again in ('y', 'n'):
                os.system('cls' if os.name == 'nt' else 'clear')
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        if play_again == 'n':
            print("Goodbye!")
            break


def save_to_high_scores(misses):
    """
    Function to handle saving scores to the spreadsheet
    """
    while True:
        save_score = input("Do you want to save your score to the high scores? (y/n): ")
        if save_score.lower() == 'y':
            name = input("Enter your name: ")
            SHEET.append_row([name, misses])
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Score saved successfully!")
            display_high_scores()
            break
        elif save_score.lower() == 'n':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Score not saved.")
            display_high_scores()
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


if __name__ == "__main__":
    """
    Main function to start the game
    """
    play_game()
