# european-league-of-football-data

Houses data related to the European League of Football (ELF).

## Repository Structure

```
european-league-of-football-data
|
├── game_stats
|   ├── player
|   |   ├── csv
|   |   └── parquet
|   └── team
|       ├── csv
|       └── parquet
|
├── gamebooks
|
├── pbp
|   ├── raw
|   |   ├── csv
|   |   └── parquet
|   ├── season
|   |   ├── csv
|   |   └── parquet
|   └── single_game
|       ├── csv
|       └── parquet
|
├── player_info
|   ├── participation_data
|   |   ├── csv
|   |   └── parquet
|   ├── photos
|   └── transactions
|       ├── csv
|       └── parquet
|
├── raw_game_data
|   ├── json
|   └── xml
|
├── rosters
|   ├── csv
|   ├── parquet
|   └── raw
|
├── schedule
|   ├── csv
|   └── parquet
|
├── standings
|   ├── csv
|   └── parquet
|
└── teams

```

### Main Directory Folders:

- `game_stats`: Houses tabular season and game stats for both players and teams.
- `gamebooks`: Houses gamebooks from the ELF from previous games.
- `pbp`: Houses play-by-play (PBP) data for the ELF.
- `player_info`: Houses participation data, player headshots, and (eventually) player transaction information.
- `raw_game_data`: Holds JSON and XML files from past ELF games.
- `rosters`: Houses current and historical ELF rosters.
- `schedule`: Houses current and historical ELF schedules.
- `standings`: Houses current and historical ELF standings data.
- `teams`: Houses any and all data specifically related to ELF teams.
