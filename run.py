import random
import gspread
from google.oauth2.service_account import Credentials

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

display_high_scores()
