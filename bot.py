
import random

from battlehack20.stubs import *

# This is an example bot written by the developers!
# Use this to help write your own code, or run it against your bot to see how well you can do!

DEBUG = 1
def dlog(str):
    if DEBUG > 0:
        log(str)


def check_space_wrapper(r, c, board_size):
    # check space, except doesn't hit you with game errors
    if r < 0 or c < 0 or c >= board_size or r >= board_size:
        return False
    try:
        return check_space(r, c)
    except:
        return None

turn_no = 0
def turn():
    """
    MUST be defined for robot to run
    This function will be called at the beginning of every turn and should contain the bulk of your robot commands
    """
    global turn_no
    turn_no += 1
    dlog('Starting Turn!')
    board_size = get_board_size()

    team = get_team()
    opp_team = Team.WHITE if team == Team.BLACK else team.BLACK
    dlog('Team: ' + str(team))

    robottype = get_type()
    dlog('Type: ' + str(robottype))

    if robottype == RobotType.PAWN:
        dlog('Human')

        r, c = get_location()
        dlog('My location is: ' + str(r) + ' ' + str(c))

        if team == Team.WHITE:
            forward = 1
            scan = 2
        else:
            forward = -1
            scan = -2
        
        # try capturing pieces
        if check_space_wrapper(r + forward, c + 1, board_size) == opp_team: # up and right
            capture(r + forward, c + 1)
            dlog('Captured at: (' + str(r + forward) + ', ' + str(c + 1) + ')') 

        elif check_space_wrapper(r + forward, c - 1, board_size) == opp_team: # up and left
            capture(r + forward, c - 1)
            dlog('Captured at: (' + str(r + forward) + ', ' + str(c - 1) + ')')
        
        elif r + forward != -1 and r + forward != board_size and not check_space_wrapper(r + forward, c, board_size):
            try:
                if check_space(r, c-1) == get_team() or check_space(r-1, c-1) == get_team() or check_space(r, c+1) == get_team() or check_space(r-1, c+1) == get_team():
                    move_forward()
                    dlog('Moved forward!')
            except:
                pass

        
    else:
        board = get_board()
        dlog(str(board))
        if team == Team.WHITE:
            forward = 1
            index = 0

        else:
            forward = -1
            index = board_size - 1
       
        deep_accum = []
        c_indexes = []
        heuristic_accum = []
        heuristic = 0
        for c in range(board_size):
            close = []
            for r in range(board_size):
                dlog(str(check_space(r, c)))
                if check_space(r, c) == opp_team:
                    if team == Team.WHITE:
                        close.append(r)
                    elif team == Team.BLACK:
                        close.append(board_size-r-1)
                    heuristic -= 1
                elif check_space(r, c) == team:
                    heuristic += 1
                else:
                    continue
            heuristic_accum.append([heuristic, c])
            if close != []:
                c_indexes.append(c)
                deep = sorted(close)
                deep_accum.append(deep[0])
            heuristic = 0
        close_index = sorted(list(zip(deep_accum, c_indexes)))
        for c in close_index:
            if c[0] == 0:
                continue           
            col = c[1]
            weighted_val = heuristic_accum[col][0]-15
            heuristic_accum[col][0] = weighted_val
            break

        heuristic_accum = sorted(heuristic_accum)

        for heur in heuristic_accum:
            col = heur[1]
            if not check_space_wrapper(index, col, board_size) and not check_space_wrapper(index+forward, col+1, board_size) == opp_team and not check_space_wrapper(index+forward, col-1, board_size) == opp_team:
                spawn(index, col)
                dlog('Spawned unit at: (' + str(index) + ', ' + str(col) + ')')
                break

    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))


