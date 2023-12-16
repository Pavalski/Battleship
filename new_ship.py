directions = ["up", "down", "right", "left"]

##########################################################
# Functions To Check Aspects Related to the Ship Boarder #
##########################################################

def ship_check(orig_r, orig_c, length, board, action):
  """Checks to see if a New ship can be placed in a certain spot
  If it can it returns a list of all the possible directions it could go
  """
  length2 = length - 1
  possible_direc = []
  for direction in directions:
    possible = True
    ship_locs = []
    if direction == "up":
      if orig_r - length2 >= 0:
        ship_locs.append([orig_r, orig_c])
        for offset in range(1, length):
          if action == "hide":
            if not ship_boarder(board, orig_r - offset, orig_c, True, ship_locs):
              possible = False
              break
          else:
            if board[orig_r - offset][orig_c] == "X" or board[orig_r - offset][orig_c] == "@":
              possible = False
              break
        if possible:
          possible_direc.append(direction)
    elif direction == "down":
      if orig_r + length2 <= len(board) - 1:
        ship_locs.append([orig_r, orig_c])
        for offset in range(1, length):
          if action == "hide":
            if not ship_boarder(board, orig_r + offset, orig_c, True, ship_locs):
              possible = False
              break
          else:
            if board[orig_r + offset][orig_c] == "X" or board[orig_r + offset][orig_c] == "@":
              possible = False
              break
        if possible:
          possible_direc.append(direction)
    elif direction == "right":
      if orig_c + length2 <= len(board[0]) - 1:
        ship_locs.append([orig_r, orig_c])
        for offset in range(1, length):
          if action == "hide":
            if not ship_boarder(board, orig_r, orig_c + offset, True, ship_locs):
              possible = False
              break
          else:
            if board[orig_r][orig_c + offset] == "X" or board[orig_r][orig_c + offset] == "@":
              possible = False
              break
        if possible:
          possible_direc.append(direction)
    elif direction == "left":
      if orig_c - length2 >= 0:
        ship_locs.append([orig_r, orig_c])
        for offset in range(1, length):
          if action == "hide":
            if not ship_boarder(board, orig_r, orig_c - offset, True, ship_locs):
              possible = False
              break
          else:
            if board[orig_r][orig_c - offset] == "X" or board[orig_r][orig_c - offset] == "@":
              possible = False
              break
        if possible:
          possible_direc.append(direction)
  if len(possible_direc) == 0:
    return False
  else:
    return possible_direc

def ship_boarder(board, ship_r, ship_c, new_ship, ship_locs):
  """Checks to see if a ship in a different ships boarder or
  It turns a ships boarder to X's when it's sunk
  """
  if ship_r == 0 and ship_c == 0:
    r_range_s, r_range_e = 0, 2
    c_range_s, c_range_e = 0, 2
  elif ship_r == 0 and ship_c == len(board[0]) - 1:
    r_range_s, r_range_e = 0, 2
    c_range_s, c_range_e = -1, 1
  elif ship_r == len(board) - 1 and ship_c == 0:
    r_range_s, r_range_e = -1, 1
    c_range_s, c_range_e = 0, 2
  elif ship_r == len(board) - 1 and ship_c == len(board[0]) - 1:
    r_range_s, r_range_e = -1, 1
    c_range_s, c_range_e = -1, 1
  elif ship_r == 0: 
    r_range_s, r_range_e = 0, 2
    c_range_s, c_range_e = -1, 2
  elif ship_r == len(board) - 1:
    r_range_s, r_range_e = -1, 1
    c_range_s, c_range_e = -1, 2
  elif ship_c == 0:
    r_range_s, r_range_e = -1, 2
    c_range_s, c_range_e = 0, 2
  elif ship_c == len(board[0]) - 1:
    r_range_s, r_range_e = -1, 2
    c_range_s, c_range_e = -1, 1
  else:
    r_range_s, r_range_e = -1, 2
    c_range_s, c_range_e = -1, 2
  for x in range(r_range_s, r_range_e):
    for y in range(c_range_s, c_range_e):
      if new_ship:
        if board[ship_r + x][ship_c + y] == "@":
          if [ship_r + x, ship_c + y] not in ship_locs:
            return False
      elif not new_ship:
        if board[ship_r + x][ship_c + y] != "@":
          board[ship_r + x][ship_c + y] = "X"
  if new_ship:
    return True