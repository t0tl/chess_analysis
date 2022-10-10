import chess.pgn
import chess.engine
import multiprocessing as mp
import sys
import re

# Future improvement could be to get the 
# move by move evaluation and run unsupervised methods (random forest, clustering)
# to see if there are time periods where Niemann engaged in cheating.

lst = []

def game_eval(game, color):
    engine = chess.engine.SimpleEngine.popen_uci(r".\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")
    board = game.board()
    sum_moves = 0
    n_moves = 0
    nie_moves = 0

    for move in game.mainline_moves():
        n_moves += 1

        # Start analysing after move 8
        if (n_moves < 16):
            board.push(move)
            continue

        # Do not analyse moves by black if color of interest is white
        if (n_moves % 2 == 0 and color == "White"): 
            board.push(move)
            continue

        # Do not analyse moves by black if color of interest is white
        elif ((n_moves+1) % 2 == 0 and color == "Black"): 
            board.push(move)
            continue

        info = engine.analyse(board, chess.engine.Limit(depth=30))
        nie_moves += 1
        if (info["pv"][0] == move):
            sum_moves += 1
        board.push(move)
    accuracy = (float(sum_moves)/float(nie_moves))*100
    engine.quit()
    return (game.headers['EventDate'], game.headers['White'], game.headers['Black'], accuracy, game.headers['PlyCount'])

def list_updater(res):
    print(res)
    lst.append(res[3])
    return lst

def printer(err):
    print(err)

def analyse(game_list, color):
    '''
    Analyses each game asynchronously using Stockfish.
    Returns a list of accuracy scores for each game.

    Takes game_list which is a list of type Game
    containing every game with the specified color.
    color is a string, "White" or "Black".
    '''
    nprocs = mp.cpu_count()
    pool = mp.Pool(processes=nprocs) 
    r1 = [pool.apply_async(func = game_eval, args=(game, color), callback = list_updater, error_callback=printer) for game in game_list]
    for r in r1:
        r.wait()
    pool.close()
    pool.join()
    return

if __name__ == "__main__":
    sys.setrecursionlimit(2000)

    pgn = open("niemann_yottabase.pgn")
    black = []
    white = []
    tmp = chess.pgn.read_game(pgn)
    rgx = re.compile(r"(\d+(\.\d{2})+(\.\d{2}))")
    while(tmp is not None):
        if (re.match(rgx, tmp.headers["EventDate"]) is None):
            tmp.headers["EventDate"] = "1111.11.11"
        if (int(tmp.headers["PlyCount"]) < 60): # Only select games with more than 30 moves.
            tmp = chess.pgn.read_game(pgn)
            continue
        if tmp.headers["White"] == "Niemann, Hans Moke":
            white.append(tmp)
        else:
            black.append(tmp)
        tmp = chess.pgn.read_game(pgn)
    white_list = analyse(white, "White")
    lst = []
    black_list = analyse(black, "Black")

