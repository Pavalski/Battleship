import random
import os
import time
from termcolor import colored, cprint
from new_ship import ship_check, ship_boarder
from comp_AI import comp_ai
from Screens import hide, attack, start, start2, hit_text, sunk_text, player1_text, player2_text, commence, win_text, lose_text, tie_text
from boards import make_board, show_board, show_boards

#########################
# Place Ships Functions #
#########################

def comp_ship(board):
  """Hides the computers ships somewhere on its board"""
  global comp_row, comp_column, comp_ships

  ship_lengths = [5, 4, 3, 3, 2]
  comp_ships = []

  for length in ship_lengths:
    ship_placed = False
    while not ship_placed:
      row = random.randint(0, 7)
      col = random.randint(0, 7)
      if ship_boarder(comp_board, row, col, True, []) == True:
          if ship_check(row, col, length, comp_board, "hide") != False:
            poss_direc = ship_check(row, col, length, comp_board, "hide")
            comp_board[row][col] = "@"
            direction = random.choice(poss_direc)
            place_ships(row, col, direction, length, "comp")
            direction = "e"
            place_ships(row, col, direction, length, "comp")
            ship_placed = True
  for row_n, row in enumerate(comp_board):
    for col_n, col in enumerate(row):
      if comp_board[row_n][col_n] == "X" or comp_board[row_n][col_n] == "@":
        comp_board[row_n][col_n] = "~"

def human_ship(player_number):
  """ The player hides their ships on their board """
  global human_ships, human_ships2
  ship_lengths = [5, 4, 3, 3, 2]
  if player_number == 1:
    human_ships = []
    ships = human_ships
  if player_number == 2:
    human_ships2 = []
    ships = human_ships2
  direc_dic = {"u": "up", "d": "down", "r": "right", "l": "left", "enter": "e"}

  if player_number == 1:
    board = human_board
  elif player_number == 2:
    board = human_board2
    
  for len_num, length in enumerate(ship_lengths):
    ship_placed = False
    while not ship_placed:
      os.system("cls")
      show_boards(play_num, comp_board, human_board, human_board2)
      try:
        print("Ships:")
        if len_num != 0:
          for leng in ship_lengths[:len_num]:
            print(colored(leng, "green"), end = " ")
        print(colored(length, "yellow"), end = " ")
        if len_num != len(ship_lengths) - 1:
          for leng in ship_lengths[len_num + 1:]:
            print(colored(leng, "red"), end = " ")
        print("\n")
        row_col = input("Choose a coordinate: ").strip()
        if len(row_col) != 2 or row_col[0].lower() not in row_name.keys() or int(row_col[1]) < 1 or int(row_col[1]) > 8:
          print("Choose an actual row and column.")
          input("Enter to continue ")
        else:
          row = row_name.get(row_col[0].lower())
          col = int(row_col[1]) - 1
          if ship_boarder(board, row, col, True, []) == True:
              if ship_check(row, col, length, board, "hide") != False:
                poss_direc = ship_check(row, col, length, board, "hide")
                board[row][col] = "@"
                direction = random.choice(poss_direc)
                if player_number == 1:
                  place_ships(row, col, direction, length, "human")
                elif player_number == 2:
                  place_ships(row, col, direction, length, "human2")
                while direction != "e":
                  os.system("cls")
                  show_boards(play_num, comp_board, human_board, human_board2)
                  print("Possible Directions:", end = " ")
                  for direc in poss_direc:
                    print(f"{direc[0]}: {direc}", end = (",  "))
                  print("e: enter\n")
                  direction = input("Choose a direction: ").lower()
                  if direction not in poss_direc and direction != "e" and direction != "enter" and direc_dic.get(direction) not in poss_direc:
                    print("That direction won't work.")
                    input("Enter to continue ")
                  else:
                    if direction in direc_dic.keys():
                      direction = direc_dic.get(direction)
                    if player_number == 1:
                      place_ships(row, col, direction, length, "human")
                    elif player_number == 2:
                      place_ships(row, col, direction, length, "human2")
                ship_placed = True
                for spot in ships[len_num]:
                  ship_boarder(board, spot[0], spot[1], False, [])
                os.system("cls")
                show_boards(play_num, comp_board, human_board, human_board2)
      except:
        print("Try Again.")
        input("Enter to continue ")
          
  for row_n, row in enumerate(board):
    for col_n, col in enumerate(row):
      if board[row_n][col_n] == "X" or board[row_n][col_n] == "@":
        board[row_n][col_n] = "~"


def place_ships(orig_r, orig_c, direction, length, player):
  """Takes an original coordinate from a player and shows how a direction would look and 
  when it recieves e as a direction it places the ship on that players board
  """
  global human_ships, comp_ships, human_ships2
  
  if player == "human":
    board = human_board
  elif player == "comp":
    board = comp_board
  elif player == "human2":
    board = human_board2
  else:
    board = test_board
    
  if direction != "e":
    for row_n, row  in enumerate(board):
      for col_n, symbol in enumerate(row):
        if symbol == "*":
          board[row_n][col_n] = "~"

    for offset in range(1, length):
      if direction == "up":
          board[orig_r - offset][orig_c] = "*"
        
      elif direction == "down":
        board[orig_r + offset][orig_c] = "*"
        
      elif direction == "right":
        board[orig_r][orig_c + offset] = "*"
        
      elif direction == "left":
        board[orig_r][orig_c - offset] = "*"
      
  else:
    ship = [[orig_r, orig_c]]
    for row_n, row in enumerate(board):
      for col_n, symbol in enumerate(row):
        if symbol == "*":
          board[row_n][col_n] = "@"
          ship.append([row_n, col_n])
    if player == "human":
      human_ships.append(ship)
    elif player == "comp":
      comp_ships.append(ship)
    elif player == "human2":
      human_ships2.append(ship)
      
##########################
# Attack Ships Functions #
##########################
  
def guess_ship(player_number):
  """The player guesses where the computer hid it's ships"""
  global win, game_over, comp_ships, human_ships, human_board, human_ships2, comp_board, human_board2
  
  lengs = [5, 4, 3, 2]
  h_lengs = []
  h2_lengs = []
  c_lengs = []
  for ship in human_ships:
    h_lengs.append(len(ship))
  if play_num == 1:
    for ship in comp_ships:
      c_lengs.append(len(ship))
    lengs_1 = h_lengs
    lengs_2 = c_lengs
    board = comp_board
    other_ships = comp_ships
    your_ships = human_ships
  elif play_num == 2:
    for ship in human_ships2:
      h2_lengs.append(len(ship))
    if player_number == 1:
      lengs_1 = h_lengs
      lengs_2 = h2_lengs
      board = human_board2
      other_ships = human_ships2
      your_ships = human_ships
    elif player_number == 2:
      lengs_1 = h2_lengs
      lengs_2 = h_lengs
      board = human_board
      other_ships = human_ships
      your_ships = human_ships2
      
  while True:
    try:
      os.system("cls")
      show_boards(play_num, comp_board, human_board, human_board2)
      print("Your ships left: ", end = "")
      for leng in lengs:
        if leng in lengs_1:
          if leng == 3:
            if len(set(lengs_1)) == len(lengs_1):
              print(colored(3, "red"), end = ", ")
            for amnt in range(lengs_1.count(3)):
              print(colored(3, "green"), end = ", ")
          elif leng == 2:
            print(colored(2, "green"), end = "\n")
          else:
            print(colored(leng, "green"), end = ", ")
        else:
          if leng == 2:
            print(colored(2, "red"), end = "\n")
          elif leng == 3:
            for _ in range(2):
              cprint(3, "red", end = ", ")
          else:
            cprint(leng, "red", end = ", ")
      if play_num == 1:
        print("Computer ships left: ", end = "")
      else:
        if player_number == 1:
          print("Player 2 ships left: ", end = "")
        else:
          print("Player 1 ships left: ", end = "")
      for leng in lengs:
        if leng in lengs_2:
          if leng == 3:
            check = lengs_2.count(3)
            if check != 2:
              print(colored(3, "red"), end = ", ")
            for amnt in range(check):
              print(colored(3, "green"), end = ", ")
          elif leng == 2:
            print(colored(2, "green"), end = "\n")
          else:
            print(colored(leng, "green"), end = ", ")
        else:
          if leng == 2:
            print(colored(2, "red"), end = "\n")
          elif leng == 3:
            for _ in range(2):
              cprint(3, "red", end = ", ")
          else:
            cprint(leng, "red", end = ", ")
      print("\n")
      row_col = input("Choose a coordinate: ").strip()
      if len(row_col) != 2 or row_col[0].lower() not in row_name.keys() or int(row_col[1]) < 1 or int(row_col[1]) > 8:
        print("Choose an actual row and column.")
        input("Enter to continue ")
      else:
        g_row = row_name.get(row_col[0].lower())
        g_col = int(row_col[1]) - 1
        if board[g_row][g_col] == "X" or board[g_row][g_col] == "@":
          print("You guessed that one already.")
          input("Enter to continue ")
        else:
          hit = "no"
          for ship_n, ship in enumerate(other_ships):
            for spot in ship:
              if g_row == spot[0] and g_col == spot[1]:
                board[g_row][g_col] = "💥"
                os.system("cls")
                show_boards(play_num, comp_board, human_board, human_board2)
                time.sleep(0.3)
                board[g_row][g_col] = "@"
                hit = "yes"
                ship_hit = ship_n
                break
            if hit == "yes" and ship_n != len(other_ships) - 1:
              break
          if hit == "yes":
            spots = 0
            spots_hit = 0
            for spot in other_ships[ship_hit]:
              if board[spot[0]][spot[1]] == "@":
                spots_hit += 1
              spots += 1
            if spots_hit == spots:
              for spot in other_ships[ship_hit]:
                ship_boarder(board, spot[0], spot[1], False, [])
              other_ships.pop(ship_hit)  
              cprint(sunk_text, "red")
              time.sleep(1.1)
            else:
              print(colored(hit_text, "yellow"))
              time.sleep(0.8) 
          else:
            board[g_row][g_col] = "X"
          if len(other_ships) == 0 or len(your_ships) == 0:
            if player_number == 1 and len(other_ships) == 0:
              win += 1
            elif player_number == 2 and len(other_ships) == 0:
              win += 2
            game_over = True
            if play_num == 1:
              for ship in your_ships:
                for spot in ship:
                  if human_board[spot[0]][spot[1]] != "@":
                    human_board[spot[0]][spot[1]] = "*"
            else:
              if player_number == 2:
                if len(other_ships) != 0:
                  for ship in other_ships:
                    for spot in ship:
                      if human_board[spot[0]][spot[1]] != "@":
                        human_board[spot[0]][spot[1]] = "*"
                if len(your_ships) != 0:
                  for ship in your_ships:
                    for spot in ship:
                      if human_board2[spot[0]][spot[1]] != "@":
                        human_board2[spot[0]][spot[1]] = "*"
          break    
            
    except:
      print("Try Again")
      input("Enter to Continue")

def comp_guess():
  """The computer guesses where the player hid their ships"""
  global game_over, win, human_ships, hit, new_ship, coor, g_row, g_col, was_hit, comp_ships, comp_board
  if not hit and new_ship:
      point = [0, 0, 0]
      for row_n, row in enumerate(human_board):
        for col_n, col in enumerate(row):
          if human_board[row_n][col_n] == "X" or human_board[row_n][col_n] == "@" or ship_check(row_n, col_n, len(human_ships[0]), human_board, "attack") == False:
            pass
          else:
            num_direcs = ship_check(row_n, col_n, len(human_ships[0]), human_board, "attack")
            if len(num_direcs) > point[2]:
              point = [row_n, col_n, len(num_direcs)]
            elif len(num_direcs) == point[2]:
              rand_num = random.randint(1,3)
              if rand_num == 1:
                point = [row_n, col_n, len(num_direcs)]
      g_row = point[0]
      g_col = point[1]  
                    
  if hit and new_ship:
    coor = comp_ai(g_row, g_col, True, True, human_board, human_ships)
  elif hit and not new_ship:
    coor = comp_ai(g_row, g_col, False, True, human_board, human_ships)
  elif not hit and not new_ship:
    coor = comp_ai(g_row, g_col, False, False, human_board, human_ships)
  if len(coor) != 0:
    g_row = coor[0]
    g_col = coor[1]
  hit = False
  for ship_n, ship in enumerate(human_ships):
      for spot in ship:
        if g_row == spot[0] and g_col == spot[1]:
          human_board[g_row][g_col] = "@"
          hit = True
          if new_ship and was_hit:
            new_ship = False
          was_hit = True
          ship_hit = ship_n
  if hit:
    spots = 0
    spots_hit = 0
    for spot in human_ships[ship_hit]:
      if human_board[spot[0]][spot[1]] == "@":
        spots_hit += 1
      spots += 1
    if spots_hit == spots:
      new_ship = True
      was_hit = False
      hit = False
      coor = []
      for spot in human_ships[ship_hit]:
        ship_boarder(human_board, spot[0], spot[1], False, [])
      human_ships.pop(ship_hit)  
      if len(human_ships) == 0:
        win += 2
        game_over = True
        if len(comp_ships) != 0:
          for ship in comp_ships:
            for spot in ship:
              if comp_board[spot[0]][spot[1]] != "@":
                comp_board[spot[0]][spot[1]] = "*"
        return game_over
  else:
    human_board[g_row][g_col] = "X"
    hit = False
    if new_ship and was_hit:
      new_ship = False
    return False

#####################
# The Main Function #
#####################
    
def play_game():
  """Runs the whole game"""
  global game_over, win, comp_board, human_board, human_board2, hit, new_ship, coor, was_hit, row_name
  os.system("cls")
  game_over = False
  win = 0
  comp_board = []
  human_board = []
  human_board2 = []
  row_name = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h":7}
  if first_time:
    start_game()
  player_amnt()
  os.system("cls")
  if play_num == 1:
    make_board(comp_board)
  else:
    make_board(human_board2)
  make_board(human_board)
  print(hide)
  time.sleep(1)
  os.system("cls")
  if play_num == 1:
    comp_ship(comp_board)
  if first_time:
    inst_print(0, 9, 1)
    input("Enter to continue: ")
    os.system("cls")
    inst_print(0, 12, 2)
    input("Enter to continue: ")
    os.system("cls")
    inst_print(0, 15, 3)
    input("Enter to continue: ")
    os.system("cls")
    inst_print(0, 18, 4)
    input("Enter to continue: ")
    os.system("cls")
    inst_print(0, 20, 5)
    input("Enter to continue")
    os.system("cls")
    inst_print(0, 27, 6)
    input("Enter to continue")
    os.system("cls")
    print(commence)
    time.sleep(1)
  if play_num == 2:
    os.system("cls")
    print(player1_text)
    time.sleep(1)
    human_ship(1)
    os.system("cls")
    print(player2_text)
    time.sleep(1)
    human_ship(2)
  else:
    human_ship(1)
  os.system("cls")
  print(attack)
  time.sleep(1.5)
  os.system("cls")
  if first_time:
    inst_print(28, 36, 7)
    input("Enter to continue")
    os.system("cls")
    inst_print(28, 38, 8)
    input("Enter to continue")
    os.system("cls")
    inst_print(28, 44, 9)
    input("Enter to continue")
    os.system("cls")
    inst_print(28, 45, 0)
    input("Enter to continue")
    os.system("cls")
    print(commence)
    time.sleep(1)
  was_hit = False
  hit = False
  new_ship = True
  coor = list()
  while game_over == False:
    if play_num == 1:
      guess_ship(1)
    else:
      os.system("cls")
      print(player1_text)
      time.sleep(1)
      guess_ship(1)
    os.system("cls")
    show_boards(play_num, comp_board, human_board, human_board2)
    if play_num == 1:
      comp_guess()
    else:
      os.system("cls")
      print(player2_text)
      time.sleep(1)
      guess_ship(2)
  os.system("cls")
  show_boards(play_num, comp_board, human_board, human_board2)
  if play_num == 1:
    if win == 1:
      print(win_text)
    elif win == 2:
      print(lose_text)
    elif win == 3:
      print(tie_text)
  else:
    if win == 1:
      print(f"{player1_text}\n{win_text}")
    elif win == 2:
      print(f"{player2_text}\n{win_text}")
    elif win == 3:
      print(tie_text)
  play_again()

################################
# Other Functions for the Game #
################################

def play_again():
  """Asks the player if they want to play again"""
  global first_time
  again = (input("\nDo you want to play again?(y/n) ")).lower()
  if again == "yes" or again == "y":
    first_time = False
    play_game()
  elif again == "no" or again == "n":
    print("Thanks for playing!")
  else:
    print("Please print yes or no.")
    play_again()
  
def start_game():
  """Prints the title screen and the general instructions of the game"""
  global first_time
  print(start)
  time.sleep(3)
  os.system("cls")
  print(start2 + "\n")
  input("Enter to continue ")
  os.system("cls")
  while True:
    instr = input("Would you like instructions?(y/n) ").lower()
    if instr == "y" or instr == "yes":
      first_time = True
      break
    elif instr == "n" or instr == "no":
      first_time = False
      break
    else:
      print("")
      
def inst_print(start, end, sp_case):
  """Recives a start and an end line to print from Instructions.txt 
  and prints certain examples when needed
  """
  global test_board
  with open("Instructions.txt", "r") as inst:
    inst_lines = inst.readlines()
  for line in range(start, end):
    if line == 4 or line == 34 or line == 40:
      cprint(inst_lines[line][0], "green", end = "")
      print(inst_lines[line][1:])
    elif line == 5:
      cprint(inst_lines[line][0], "yellow", end = "")
      print(inst_lines[line][1:])
    elif line == 6 or line == 33 or line == 41:
      cprint(inst_lines[line][0], "red", end = "")
      print(inst_lines[line][1:])
    elif line == 19:
      print(inst_lines[line][:14], end = "")
      cprint(inst_lines[line][14], "yellow", end = "")
      print(inst_lines[line][15:])
    elif line == 44:
      print(inst_lines[line][:25], end = "")
      cprint(inst_lines[line][25], "yellow", end = " ")
      print(inst_lines[line][27:])
    else:
      print(inst_lines[line])
  if sp_case == 1:
    print("Example:\n")
    print("Ships:")
    cprint("5 4 ", "green", end = "")
    cprint("3 ", "yellow", end = "")
    cprint("3 2", "red")
    print("")
  elif sp_case == 2 or sp_case == 3 or sp_case == 5 or sp_case == 6:
    test_board = []
    if sp_case == 2:
      spots = [[2,2], [2,3], [2,4]]
    elif sp_case == 3 or sp_case == 5 or sp_case == 6:
      spots = [[1,5]]
    make_board(test_board)
    for spot in spots:
      test_board[spot[0]][spot[1]] = "@"
    if sp_case == 2:
      for spot in spots:
        ship_boarder(test_board, spot[0], spot[1], False, [])
    if sp_case == 5 or sp_case == 6:
      place_ships(1, 5, "down", 3, "test")
    if sp_case == 6:
      place_ships(1, 4, "e", 3, "test")
    if sp_case == 4:
      print("It would place here:\n")
    else:  
      print("Example: \n")
    show_board(test_board, 3, 0)
  elif sp_case == 4:
    print("For example: \n")
    print("Possible Direction: d: down, r: right, e: enter\n")
  elif sp_case == 7:
    test_board = []
    make_board(test_board) 
    test_board[2][2] = "X"
    test_board[4][4] = "@"
    print("Example: \n")
    show_board(test_board, 3, 0)
  elif sp_case == 8:
    cprint(hit_text, "yellow")
    print("")
    cprint(sunk_text, "red")
    print("")
  elif sp_case == 9:
    print("For example:\n")
    print("Your ships left: ", end = "")
    cprint("5, ", "green", end = "")
    cprint("4, 3, ", "red", end = "")
    cprint("3, 2", "green")
    print("Computer ships left: ", end = "")
    cprint("5, 4, ", "red", end = "")
    cprint("3, 3, ", "green", end = "")
    cprint("2", "red")
    print("")

def player_amnt():
  global play_num
  while True:
    try:
      os.system("cls")
      play_num = int(input("How many player?(1/2) "))
      if play_num == 1 or play_num == 2:
        break
      else:
        print("1 or 2")
        time.sleep(0.5)
    except:
      print("1 or 2")
      time.sleep(0.5)
  
first_time = True # States that this will be the first playthrough of the game
play_game() # Starts the game
