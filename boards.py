from termcolor import colored
from colored import bg, style, style, attr

###################
# Board Functions #
###################

BOARD_HEIGHT = 8
BOARD_LENGTH = 8

def make_board(board):
  """ Creates the boards for both players """
  for rows in range(BOARD_HEIGHT):
    board.append(["~"] * BOARD_LENGTH)

def show_board(board, num, num_of_players):
  """ Prints the given board on the terminal """
  bkrd = 159 #159, 195, 153
  row_value = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
  if num_of_players == 1:
    if num == 1:
      print("Computer's Board\n")
    elif num == 2:
      print("-" * 38, end = "\n\n")
      print("Your Board\n")
  if num_of_players == 2:
    if num == 1:
      print("Player 1 Board\n")
    elif num == 2:
      print("-" * 38, end = "\n\n")
      print("Player 2 Board\n")
  
  if num == 3:
    print("Your Board\n")
    
  print("     1   2   3   4   5   6   7   8\n")
  for row_n, row in enumerate(board):
    print(attr('reset'), end= "")
    print(row_value.get(row_n), end = "   ")
    for spot_n, spot in enumerate(row):
      print(bg(bkrd) + colored("│", "cyan"), end = f"{bg(bkrd)} ")
      if spot == "~":
        print(bg(bkrd) + colored(spot, "blue"), end = f"{bg(bkrd)} ")
      elif spot == "X":
        print(bg(bkrd) + colored(spot, "red"), end = f"{bg(bkrd)} ")
      elif spot == "@":
        print(bg(bkrd) + colored(spot, "green"), end = f"{bg(bkrd)} ")
      elif spot == "*":
        print(bg(bkrd) + colored(spot, "yellow"), end = f"{bg(bkrd)} ")
      else:
        print(bg(bkrd) + spot, end = f"{bg(bkrd)}")
      if spot_n == 7:
        print(bg(bkrd) + colored("│", "cyan"), end = f"{bg(bkrd)}")
    print(attr('reset') + "  ", end = "")
    print("")

  print("" + attr('reset'))

def show_boards(num_of_players, board_1, board_2, board_3):
  """ Runs the function show_board to show both boards """
  if num_of_players == 1:
    show_board(board_1, 1, 1)
    show_board(board_2, 2, 1)
  else:
    show_board(board_2, 1, 2)
    show_board(board_3, 2, 2)