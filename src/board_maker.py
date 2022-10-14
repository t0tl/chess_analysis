import numpy as np
import chess.pgn
from enum import Enum
import pandas as pd

class Color(Enum):
    BLACK = 0
    WHITE = 1

dictionary = {"a" : 1,
"b": 2,
"c": 3,
"d" : 4,
"e" : 5,
"f" : 6,
"g" : 7,
"h" : 8
}

def df_to_perc(df):
    return round(df.divide(df.to_numpy().sum())*100, ndigits=1)

def char_to_num(char) -> int:
    return dictionary[char]

def board_move_counter(lst, color):
    count = np.zeros((8,8)) 

    for game in lst:
        board = game.board()
        for move in game.mainline_moves():
            if color == Color.WHITE and board.turn:
                board.push(move)
                continue
            if color == Color.BLACK and not board.turn:
                board.push(move)
                continue

            pos = board.san(move)
            if len(pos) == 2:
                # Chess notation comes (col, row), therefore we need to swap around the indexes.
                # rows - 8-1 (top down)
                # cols - a-h (left to right)
                tmp = char_to_num(pos[0])
                pos = f"{pos[1]}{tmp}"
                count[int(pos[0])-1][int(pos[1])-1] += 1
            elif len(pos) == 3:
                if pos == "O-O" or pos[2] == "+" or pos[2] == "#":
                    board.push(move)
                    continue
                tmp = char_to_num(pos[1])
                pos = f"{pos[2]}{tmp}"
                count[int(pos[0])-1][int(pos[1])-1] += 1
            elif len(pos) == 4:
                if pos[3] == "+" or pos[3] == "#":
                    board.push(move)
                    continue
                if pos[2] == "=":
                    tmp = char_to_num(pos[0])
                    pos = f"{pos[1]}{tmp}"
                    count[int(pos[0])-1][int(pos[1])-1] += 1
                    board.push(move)
                    continue

                tmp = char_to_num(pos[2])
                pos = f"{pos[3]}{tmp}"
                count[int(pos[0])-1][int(pos[1])-1] += 1

            board.push(move)
    return pd.DataFrame(count)

def df_combiner(white_df, black_df):
    total_moves = white_df + black_df
    white_df = df_to_perc(white_df)
    black_df = df_to_perc(black_df)
    total_moves = df_to_perc(total_moves)

    white_df = white_df.assign(color = ["White", "White","White","White","White","White","White","White"])
    black_df = black_df.assign(color = ["Black", "Black", "Black","Black","Black","Black","Black","Black"])
    filterable = pd.concat([white_df, black_df])
    return total_moves, filterable

def board_heat():
    '''
    Creates one 8x8 array and one 16x9 array representing proportion of moves played. 
    '''

    pgn = open("src/niemann_yottabase.pgn")
    black = []
    white = []
    tmp = chess.pgn.read_game(pgn)
    while(tmp is not None):
        if tmp.headers["White"] == "Niemann, Hans Moke":
            white.append(tmp)
        else:
            black.append(tmp)
        tmp = chess.pgn.read_game(pgn)
    total_moves_white = board_move_counter(black, Color.BLACK)
    total_moves_black = board_move_counter(white, Color.WHITE)
    total_moves, filterable = df_combiner(total_moves_white, total_moves_black)

    return total_moves, filterable

