# Chess Analysis
A repository collecting, analysing, and visualising Hans Niemanns chess games

### A 'Dash' of an Interactive Heatmap
The plotly heatmap shows the likelihood of Hans moving any of his pieces to one the squares. One can further choose to segment on only his games as white or black.
![Heatmap of proportion of moves landing on a specific square](https://github.com/t0tl/chess_analysis/blob/main/README_ASSETS/hans_niemann_square_frequency.png?raw=true)

### Another Excerpt from the Dash App
Two histograms of Niemann's accuracy scores depending on whether he is playing the black or white pieces.
![Histograms of Niemann's accuracy scores](https://github.com/t0tl/chess_analysis/blob/main/README_ASSETS/histogram.png?raw=true)

## Getting started with the repo
To use the repository, you need to have the an chess engine downloaded. For this project, I have used Stockfish 15 which can be downloaded from [Stockfish](https://stockfishchess.org/).

You also might need to install some dependecies using the following command:
```
pip install chess psycopg2 pandas numpy
```
You will also need to connect the program to a postgres database as it currently stands. To do that, make a file called `database.ini` and specify your credentials inside. 
```ini
[postgresql]
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
