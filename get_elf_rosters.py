from datetime import datetime, timedelta
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from elf_utils import parse_names


def get_old_elf_rosters(save=False):
    rosters_df = pd.DataFrame()
    row_df = pd.DataFrame()

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

    hit_wall = False
    retries = 0
    page_num = 0
    running_count = 0
    while hit_wall == False:
        page_num += 1
        players_url = f"https://europeanleague.football/league/players?7e78f181_page={page_num}"
        time.sleep(1)

        response = requests.get(players_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        # print(response.encoding)
        if response.status_code == 200:
            soup = BeautifulSoup(
                response.text, features='lxml')
            # soup = soup.html.encode('utf-8')
            time.sleep(1)
            player_cards = soup.find_all('div', {'class': 'player-card'})
            player_count = len(player_cards)
            running_count = player_count + running_count

            for i in player_cards:  # tqdm(player_cards):
                player_id = str(i.find('a').get('href')).replace(
                    'player', '').replace('/', '')
                player_first_name = i.find(
                    'h3', {'fs-cmsfilter-field': 'first-name'}).text
                player_last_name = i.find(
                    'h3', {'fs-cmsfilter-field': 'last-name'}).text

                # print(f"\n{player_first_name} {player_last_name}")
                player_info = i.find('div', {'class': 'pc-info-part'})

                player_number = player_info.find(
                    'div', {'fs-cmsfilter-field': 'player-number'}).text

                player_position = player_info.find(
                    'div', {'fs-cmsfilter-field': 'pos'}).text
                try:
                    player_height_m = float(str(player_info.find(
                        'div', {'fs-cmsfilter-field': 'height'}).text).replace(',', '.'))
                except:
                    player_height_m = None

                if player_height_m != None:
                    player_height_in = round((player_height_m / 0.0254), 2)
                else:
                    player_height_in = None

                try:
                    player_weight_kg = int(player_info.find(
                        'div', {'fs-cmsfilter-field': 'weight'}).text)
                except:
                    player_weight_kg = None

                if player_weight_kg != None:
                    player_weight_lbs = round(
                        (player_weight_kg / 0.45359237), 2)
                else:
                    player_weight_lbs = None

                del player_info

                player_seasons = i.find_all(
                    'div', {'class': 'multi-item-line-wrapper'})

                for j in range(2, len(player_seasons)):
                    ps = player_seasons[j]

                    row_df = pd.DataFrame({'player_id': player_id,
                                           'player_number': player_number,
                                           'player_first_name': player_first_name,
                                           'player_last_name': player_last_name,
                                           'player_position': player_position,
                                           'player_height_m': player_height_m,
                                           'player_height_in': player_height_in,
                                           'player_weight_kg': player_weight_kg,
                                           'player_weight_lbs': player_weight_lbs
                                           }, index=[0])

                    player_season = int(str(ps.find_all(
                        'div', {'class': 'pc-pre-heading is--multi-item'})[0].text).replace(' Team:', ''))
                    player_team = ps.find_all(
                        'div', {'class': 'pc-pre-heading is--multi-item'})[1].text

                    if player_team == "-":
                        pass
                    else:
                        row_df['season'] = player_season
                        row_df['team'] = player_team

                        rosters_df = pd.concat(
                            [rosters_df, row_df], ignore_index=True)

            print(
                f"{player_count} ELF players loaded in, {running_count} ELF players currently parsed.")

            if player_count < 50:
                print('Finished parsing through the ELF players list.')
                hit_wall = True

            elif player_count == 0:
                print('No further ELF players were found.')
                hit_wall = True

            print('')
        elif retries < 5:
            print(
                f"Couldn't load in player cards, attempting to reconnect. (Previous retries: {retries})")
            retries += 1

        elif retries == 5:
            print(
                'Aborting download/parsing of ELF player rosters. Maximum retries reached.')
        else:
            hit_wall = True

    if save == True:
        rosters_df.to_csv('rosters/csv/elf_rosters.csv')
        rosters_df.to_parquet('rosters/parquet/elf_rosters.parquet')

    return rosters_df


if __name__ == "__main__":
    get_old_elf_rosters(True)
