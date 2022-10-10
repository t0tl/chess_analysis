# chess_analysis
A repository collecting, analysing, and visualising Hans Niemanns chess games

## Getting started
To use the repository, you need to have the an chess engine downloaded. For this project, I have used Stockfish 15 which can be downloaded from [Stockfish](https://stockfishchess.org/).

You also might need to install some dependecies using the following command:
```
pip install chess psycopg2 pandas numpy
```
You will also need to connect the program to a postgres database as it currently stands. To do that, make a file called `database.ini` and specify your credentials inside. 
```ini
[postgres]
host=HOST
database=DB_NAME
user=DB_USER
password=DB_PASSWORD
```

The database table needs to have a specification similar to the one below:
```postgres
CREATE TABLE name (
	id serial PRIMARY KEY,
	event_date date,
	white VARCHAR ( 50 ),
	black VARCHAR ( 50 ),
	accuracy real,
    n_moves int smallint
);
```
