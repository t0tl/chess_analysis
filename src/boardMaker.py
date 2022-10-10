import numpy as np

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

def char_to_num(char):
    return dictionary[char]

def board_heat(lst, firstmove):
    '''
    Creates an 8x8 array to show a heatmap of moves played.

    :param: firstmove is if Niemann played white. 
    '''
    count = np.zeros((8,8))

    # Chess notation comes (col, row), therefore we need to swap around the indexes.
    # rows - 8-1 (top down)
    # cols - a-h (left to right)
    for i in range(len(lst)):
        if firstmove == 1:
            if (i+1) % 2:
                continue
        else:
            if i % 2:
                continue
        board = lst[i].board()
        for move in lst[i].mainline_moves():
            pos = board.san(move)
            if len(pos) == 2:
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
    return count

