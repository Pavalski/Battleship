import random
from new_ship import ship_check

##########################
# The AI of the computer #
##########################

opp_direc = {"up": "down", "down": "up", "right": "left", "left": "right"}

direc = None
try_direc = None
shot = 1
start_r = 1
start_c = 1

def comp_ai(orig_r, orig_c, new, hit, board, ships_left):
  """Checks to see where the computer should attack if it hit a ship"""
  global direc, shot, try_direc, start_r, start_c, directions
  
  if new:
    directions = ship_check(orig_r, orig_c, len(ships_left[-1]), board, "attack")
    start_r = orig_r
    start_c = orig_c
    try_direc = None
    shot = 1
  if not hit or (hit and new):
    if try_direc != None:
      direc = try_direc
      shot = 1
    elif not new:
      directions.remove(direc)
  else:
    try_direc = opp_direc.get(direc)
    shot += 1
  good_direc = False
  while not good_direc:
    if (not hit or (hit and new)) and try_direc == None:
      direc = random.choice(directions)
    if direc == "up":
      if (start_r - shot) >= 0 and board[start_r - shot][start_c] != "X" :
        good_direc = True
        direc = "up"
      else:
        directions.remove(direc)
    elif direc == "down":
      if (start_r + shot) <= 7 and board[start_r + shot][start_c] != "X" :
        good_direc = True
        direc = "down"
      else:
        directions.remove(direc)
    elif direc == "right":
      if (start_c + shot) <= 7 and board[start_r][start_c + shot] != "X":
        good_direc = True
        direc = "right"
      else:
        directions.remove(direc)
    elif direc == "left":
      if (start_c - shot) >= 0 and board[start_r][start_c - shot] != "X":
        good_direc = True
        direc = "left"
      else:
        directions.remove(direc)
    if not good_direc and try_direc != None:
      direc = try_direc
      shot = 1
      good_direc = True
  if direc == "up":
    return [start_r - shot, start_c]
  elif direc == "down":
    return [start_r + shot, start_c]
  elif direc == "right":
    return [start_r, start_c + shot]
  elif direc == "left":
    return [start_r, start_c - shot]

