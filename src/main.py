import chess.pgn
import chess.engine
import multiprocessing as mp
import sys
import psycopg2
import re
from config import config

def game_eval(game, color):
    '''
    A function which analyses each move Hans Niemann
    played (excluding the first 8 moves) and 
    returns his accuracy for the game
    '''
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

def db_insert(res):
    '''
    Retrieves return values from game_eval and 
    inserts into a postgres database.
    '''
    try:
        cur.execute('''INSERT INTO niemann(event_date, white, black, accuracy, n_moves) VALUES(%s,%s,%s,%s,%s);''', res)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as err:
        print(err)

def analyse(game_list, color):
    '''
    Analyses each game asynchronously by calling game_eval.
    Returns a list of accuracy scores for each game.

    Takes game_list which is a list of type Game
    containing every game with the specified color.
    color is a string, "White" or "Black".
    '''
    nprocs = mp.cpu_count()
    pool = mp.Pool(processes=nprocs) 
    r1 = [pool.apply_async(func = game_eval, args=(game, color), callback = lambda res: db_insert(res), error_callback=print) for game in game_list]
    for r in r1:
        r.wait()
    pool.close()
    pool.join()
    return

if __name__ == "__main__":
    sys.setrecursionlimit(2000)
    
    # Get the db params from config.py
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)
    conn.autocommit = True

    # create a cursor
    cur = conn.cursor()

    pgn = open("niemann_yottabase.pgn")
    black = []
    white = []
    tmp = chess.pgn.read_game(pgn)
    # Regex which checks for date using format yyyy.mm.dd
    rgx = re.compile(r"(\d+(\.\d{2})+(\.\d{2}))") 
    while(tmp is not None):

        if (re.match(rgx, tmp.headers["EventDate"]) is None):
            tmp.headers["EventDate"] = "1111.11.11"

            # Only select games with more than 30 moves.
        if (int(tmp.headers["PlyCount"]) < 60): 
            tmp = chess.pgn.read_game(pgn)
            continue

        if tmp.headers["White"] == "Niemann, Hans Moke":
            white.append(tmp)

        else:
            black.append(tmp)

        tmp = chess.pgn.read_game(pgn)
        
    analyse(white, "White")
    analyse(black, "Black")
    cur.close()
    conn.close()
