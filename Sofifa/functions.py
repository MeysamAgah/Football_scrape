# installs
!pip install selenium
!apt-get install chromium-driver

#requirements and imports
# import necessary modules
import pandas as pd
import os
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#initializing webscrappig tools
user_agent_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'

def web_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--verbose")
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920, 1200")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f"user-agent={user_agent_string}")
    driver = webdriver.Chrome(options=options)
    return driver

def find_versions():
  """
  this function will result a pandas dataframe consist of all versions and all games and date of all versions.
  """
  df = pd.DataFrame(
      columns=['fifa', 'version', 'date']
  )
  initial_versions = [str(0) + str(70001+i*10000) if i <3 else str(70001+i*10000) for i in range(19)]
  for ver in tqdm(initial_versions):
    driver = web_driver()
    initial_url = f"https://sofifa.com/?r={ver}&set=true"
    driver.get(initial_url)
    time.sleep(2)
    version_dates = driver.find_elements("name", "roster")
    dates = version_dates[0].text.split("\n")[::-1]
    versions = [str(int(ver) + i) if ver[0] != '0' else '0' + str(int(ver) + i) for i in range(len(dates))]
    fifa = [i[:2] for i in versions]
    df_temp = pd.DataFrame(
        {
            'fifa': fifa,
            'version': versions,
            'date': dates
        }
    )
    df = pd.concat([df, df_temp], ignore_index=True)

  return df

def scrape_leagues(version):
  """
  arguments: version (string)
  this will result dataframe consist of all leagues information
  """
  driver = web_driver()
  url = f"https://sofifa.com/leagues?r={version}&set=true"
  driver.get(url)

  table = driver.find_elements(By.TAG_NAME, 'td')

  league_urls =[]
  league_names = []
  country_names = []
  num_teams = []
  num_players = []
  num_added_players = []
  num_updated_players = []
  num_removed_players = []
  
  for i in range(len(table)):
    if i%8==0:
      pass
    elif i%8==1:
      league_urls.append(a[i].find_element(By.TAG_NAME, 'a').get_attribute('href'))
      league_names.append(a[i].text.split('\n')[0])
      country_names.append(a[i].text.split('\n')[1])
    elif i%8==2:
      num_teams.append(a[i].text)
    elif i%8==3:
      num_players.append(a[i].text)
    elif i%8==4:
      num_added_players.append(a[i].text)
    elif i%8==5:
      num_updated_players.append(a[i].text)  
    elif i%8==6:
      num_removed_players.append(a[i].text)  
    else:
      pass

  driver.quit()
    
  df = pd.DataFrame(
      {
          'league_urls': league_urls,
          'league_names': league_names,
          'country_names': country_names,
          'num_teams': num_teams,
          'num_players': num_players,
          'num_added_players': num_added_players,
          'num_updated_players': num_updated_players,
          'num_removed_players': num_removed_players
      }
  )

  return df

def scrape_teams(league_url, version='250016'):
  """
  argumets:
    league_url (string): url of league for example: 'https://sofifa.com/league/13'
    version (string): version of sofifa
  this will result dataframe consist of all teams information in selected league
  columns:
    team: indicate team name (string)
    overall: a number indicating overall score of team
  """
  #initializing webscrapping
  driver = web_driver()
  driver.get(league_url)

  teams = []
  overalls = []
  urls = []

  for e in driver.find_elements(By.CLASS_NAME, "ellipsis")[1:]:
    teams.append(e.text.split('\n')[0])
    overalls.append(e.text.split('\n')[1])
    urls.append(e.find_elements(By.TAG_NAME, 'a')[1].get_attribute('href') + f"?r={version}&set=true")

  df = pd.DataFrame(
      {
          'team': teams,
          'overall': overalls,
          'urls': urls
      }
  )

  return df

def player_features_dict():
    feature_mapping_dict = {
      'ID': 'pi',
      'Age': 'ae',
      'Height': 'hi',
      'Weight': 'wi',
      'Preferred_foot': 'pf',
      'Overall_rating': 'oa',
      'Potential': 'pt',
      'Best_overall': 'bo',
      'Best_position': 'bp',
      'Growth': 'gu',
      'Joined': 'jt',
      'Loan_date_end': 'le',
      'Value': 'vl',
      'Wage': 'wg',
      'Release_clause': 'rc',
      'Attcking_Total': 'ta',
      'Attacking_Crossing': 'cr',
      'Attacking_Finishing': 'fi',
      'Attacking_Heading_accuracy': 'he',
      'Attacking_Short_passing': 'sh',
      'Attacking_Volleys': 'vo',
      'Skill_Total': 'ts',
      'Skill_Dribbling': 'dr',
      'Skill_Curve': 'cu',
      'Skill_FK_accuracy': 'fr',
      'Skill_Long_passing': 'lo',
      'Skill_Ball_control': 'bl',
      'Movement_Total': 'to',
      'Movement_Acceleration': 'ac',
      'Movement_Sprint_speed': 'sp',
      'Movement_Agility': 'ag',
      'Movement_Reactions': 're',
      'Movement_Balance': 'ba',
      'Power_Total': 'tp',
      'Power_Shot_power': 'so',
      'Power_Jumping': 'ju',
      'Power_Stamina': 'st',
      'Power_Strength': 'sr',
      'Power_Long_shots': 'ln',
      'Mentality_Total': 'te',
      'Mentality_Aggression': 'ar',
      'Mentality_Interceptions': 'in',
      'Mentality_Att.Position': 'po',
      'Mentality_Vision': 'vi',
      'Mentality_Penalties': 'pe',
      'Mentality_Composure': 'cm',
      'Defending_Total': 'td',
      'Defending_Defensive_awareness': 'ma',
      'Defending_Standing_tackle': 'sa',
      'Defending_Sliding_tackle': 'sl',
      'Goalkeeping_Total': 'tg',
      'Goalkeeping_Diving': 'gd',
      'Goalkeeping_Handling': 'gh',
      'Goalkeeping_Kicking': 'gc',
      'Goalkeeping_Positioning': 'gp',
      'Goalkeeping_Reflexes': 'gr',
      'Total_Stats': 'tt',
      'Base_Stats': 'bs',
      'Weak_Foot': 'wk',
      'Skill_Moves': 'sk',
      'Attacking_Work_rate': 'aw',
      'Defensive_Work_rate': 'dw',
      'International_Reputation': 'ir',
      'Body_type': 'bt',
      'Real_face': 'hc',
      'Pace/Diving': 'pac',
      'Shooting/Handling': 'sho',
      'Passing/Kicking': 'pas',
      'Dribbling/Reflexes': 'dri',
      'Defending/Pace': 'def',
      'Physical/Positioning': 'phy',
      'Traits1': 't1',
      'Traits2': 't2',
      'PlayStyles': 'ps1',
      'PlayStyles+': 'ps2',
      'Number_of_PlayStyles': 'tc',
      'Acceleration_Type': 'at'
  }

    return feature_mapping_dict

def scrape_players(team_url, version='250016', feature_mode='all', features=None, player_mode='all'):
  """
  argumets:
    team_url (string): url of team for example: 'https://sofifa.com/team/10/manchester-city'
    version (string): version of sofifa
    feature_mode (string):
      "all": output all possible features
      "include": output a list of given features
      "exclude": output all possible features except list of given features
    features (list): list of given features
    *** You don'y need to modify this argument if feature_mode is set on "all" ***
    player_mode (string):
      "all": will consider all players of team including squad players and loan players
      "squad": will consider only squad players
      "loan": will consider only loan players
  this will result dataframe consist of all players information in selected team
  columns: desired features 
  """
  feature_mapping_dict = player_features_dict()
  
  # considering different situations for how to output playerrs features
  if feature_mode == 'all':
    features = list(feature_mapping_dict.keys())
  elif feature_mode == 'include':
    features = list(set(feature_mapping_dict.keys()) & set(features))
  elif feature_mode == 'exclude':
    features = list(set(feature_mapping_dict.keys()) - set(features))
  else:
    raise ValueError("feature_mode must be 'all', 'include' or 'exclude'")

  # considering different situations for how to select players
  if player_mode == 'all':
    xpath = "/html/body/main[2]/article" 
  elif player_mode == 'squad':
    xpath = "/html/body/main[2]/article/table[1]"
  elif player_mode == 'loan':
    xpath = "/html/body/main[2]/article/table[2]"
  else:
    raise ValueError("player_mode must be 'all', 'squad' or 'loan'")

  # finding desired url
  base_url = team_url
  url_version_adder = f"/?r={version}&set=true" #this part specifies version of table
  base_feature_adder = "&showCol%5B%5D=" # this part is in url after specifying each position included on table
  final_url = base_url + url_version_adder
  for f in features:
    final_url += base_feature_adder + feature_mapping_dict[f]
  
  # initializing webscrapping
  driver = web_driver()
  driver.get(final_url)

  # getting basic information
  player_elements1 = driver.find_elements(By.XPATH, xpath + '//a[contains(@href, "/player/")]')
  player_names = []
  player_full_names = []
  player_urls = []

  for player in player_elements1:
    player_name = player.text  # Extract the displayed name
    player_full_name = player.get_attribute('data-tippy-content')  # Full name from attribute
    player_url = player.get_attribute('href')  # Full URL
    player_names.append(player_name)
    player_full_names.append(player_full_name)
    player_urls.append(player_url)

  player_elements2 = driver.find_elements(By.XPATH, xpath + '//img[contains(@class, "flag")]')
  countries = []

  for player in player_elements2:
    countries.append(player.get_attribute('title'))

  # forming up a base dataframe
  df = pd.DataFrame(
      {
          'player_names': player_names,
          'player_full_names': player_full_names,
          'player_urls': player_urls,
          'countries': countries,
      }
  )

  # adding desired features
  for f in features:
    val = feature_mapping_dict[f]
    td_elements = driver.find_elements(By.XPATH, xpath + f'//td[@data-col="{val}"]')
    values = [element.text for element in td_elements]
    df[f] = values

  df['version'] = version
    
  return df

def scrape_players2(league_ids, offset_num, type_='all', version='250016', feature_mode='all', features=None):
  """
  argumets:
    league_ids (integer): ids of leagues e.g. England Premier League ID is 13 check scrape_leagues() for more info
    offset_num (integer): specifies number of players to scrape e.g. offset_nu of 120 will scrape first two pages and maximum 120 players
    type (string):
      "all": will consider all players in current roster
      "added": will consider only added players to version
      "updated": will consider only updated players on current version
      "free": will consider only free players on current version
      "onLoan": will consider only on Loan players on current version
      "removed": will consider only removed players from current version
      "history": will consider all players on history
    version (string): version of sofifa
    feature_mode (string):
      "all": output all possible features
      "include": output a list of given features
      "exclude": output all possible features except list of given features
    features (list): list of given features
    *** You don'y need to modify this argument if feature_mode is set on "all" ***
    player_mode (string):
      "all": will consider all players of team including squad players and loan players
      "squad": will consider only squad players
      "loan": will consider only loan players
  this will result dataframe consist of all players information in selected team
  columns: desired features
  """

  # dictionary of feature names and their code
  feature_mapping_dict = player_features_dict()

  # considering different situations for how to output playerrs features
  if feature_mode == 'all':
    features = list(feature_mapping_dict.keys())
  elif feature_mode == 'include':
    features = list(set(feature_mapping_dict.keys()) & set(features))
  elif feature_mode == 'exclude':
    features = list(set(feature_mapping_dict.keys()) - set(features))
  else:
    raise ValueError("feature_mode must be 'all', 'include' or 'exclude'")

  # specifying a general xpath
  xpath = "/html/body/main[1]/article/table"

  def url_maker(league_ids, ver):
    base_url = "https://sofifa.com/players?type=all"
    type_url = f"?type={type_}"
    final_url = base_url + type_url
    for l in league_ids:
      final_url += f"&lg%5B%5D={l}"
    #feature_url = ""
    for f in features:
      final_url += f"&showCol%5B%5D={feature_mapping_dict[f]}"
    version_url = f"&r={ver}&set=true"
    final_url = final_url + version_url
    return final_url

  num_pages = offset_num // 60 + 1

  urls = []
  for i in range(num_pages):
    offset_number = str(60*i)
    urls.append(url_maker(league_ids, version) + f"&offset={offset_number}")
  
  def form_df(url):
    driver = web_driver()
    driver.get(url)

    # getting basic information
    player_elements1 = driver.find_elements(By.XPATH, xpath + '//a[contains(@href, "/player/")]')
    player_names = []
    player_full_names = []
    player_urls = []

    for player in player_elements1:
      player_name = player.text  # Extract the displayed name
      player_full_name = player.get_attribute('data-tippy-content')  # Full name from attribute
      player_url = player.get_attribute('href')  # Full URL
      player_names.append(player_name)
      player_full_names.append(player_full_name)
      player_urls.append(player_url)

    player_elements2 = driver.find_elements(By.XPATH, xpath + '//img[contains(@class, "flag")]')
    countries = []

    for player in player_elements2:
      countries.append(player.get_attribute('title'))

    # forming up a base dataframe
    df = pd.DataFrame(
        {
            'player_names': player_names,
            'player_full_names': player_full_names,
            'player_urls': player_urls,
            'countries': countries,
        }
    )

    # adding desired features
    for f in features:
      val = feature_mapping_dict[f]
      td_elements = driver.find_elements(By.XPATH, xpath + f'//td[@data-col="{val}"]')
      values = [element.text for element in td_elements]
      df[f] = values
    
    return df

  problem_urls = []
  df = form_df(urls[0])
  # First iteration: Attempt to scrape all URLs
  for url in tqdm(urls[1:]):
    try:
      df = pd.concat([df, form_df(url)], ignore_index=True)
    except:
      problem_urls.append(url)

  # Continuously retry scraping problematic URLs until all are resolved
  while problem_urls:
    print(f"Retrying {len(problem_urls)} problematic URLs...")
    retry_urls = problem_urls.copy()  # Create a copy of the list to iterate over
    problem_urls = []  # Clear the list for the next iteration

    for url in tqdm(retry_urls):
      try:
        df = pd.concat([df, form_df(url)], ignore_index=True)
      except Exception as e:
        problem_urls.append(url)  # Add the URL back to the list if it fails again
        print(f"Failed to scrape {url}. Error: {e}")

    # Optional: Add a delay between retries to avoid overwhelming the server
    time.sleep(5)  # Adjust the delay as needed

  df['version'] = version

  return df

def scrape_player(player_url, version='250016'):
  """
  argumets:
    player_url (string): url of player for example: 'https://sofifa.com/player/192985/kevin-de-bruyne/'
    version (string): version of sofifa
  this will result dataframe consist of all classic features of player
  these features are:
  name: abbreviated player name
  full_name: full name of player
  country: country of player
  position: positions of player
  age: age of player
  date_of_birth: date player was born in format "Mon dd, yyyy"
  height_cm: height in cm
  height_ft: height in feet and inches
  weight_kg: weight in kg
  weight_lb: weight in pounds
  overall: overall rating score(1-100)
  potential: overall potential score(1-100)
  value: value of player in Million euro
  wage: wage of player in thousand euro
  likes: number of likes of player
  dislikes: number of dislikes of player
  follow: number of followers of player
  preferred_foot: Preferred foot of player (right or left)
  skill_moves: Skill moves score of player (1-5)
  weak_foot: weak foot score of player (1-5)
  international_reputation: international reputation score of player (1-5)
  body_type: Body type (categorical)
  real_face: Real face (yes or no)
  release_clause: Release clause in Million euro
  acceleration_type: Acceleration Type (categorical)
  specialities: Player specialities (multiple strings)
  club: team name
  club_league: league name
  club_overall: overall score of team (1-100)
  club_position: player position in team
  club_kit_num: player kit number in team
  club_joined_date: date player joined club
  club_contract_expire: date player contract expires
  attacking_crossing: attacking crossing score (1-100)
  attacking_finishing: attacking finishing score (1-100)
  attacking_heading_accuracy: attacking heading accuracy score (1-100)
  attacking_short_passing: attacking short passing score (1-100)
  attacking_volleys: attacking volleys score (1-100)
  skill_dribbling: skill dribbling score (1-100)
  skill_curve: skill curve score (1-100)
  skill_fk_accuracy: skill free kick accuracy score (1-100)
  skill_long_passing: skill long passing score (1-100)
  skill_ball_control: skill ball control score (1-100)
  movement_acceleration: movement acceleration score (1-100)
  movement_sprint_speed: movement sprint speed score (1-100)
  movement_agility: movement agility score (1-100)
  movement_reactions: movement reactions score (1-100)
  movement_balance: movement balance score (1-100)
  power_shot_power: power shot power score (1-100)
  power_jumping: power jumping score (1-100)
  power_stamina: power stamina score (1-100)
  power_strength: power strength score (1-100)
  power_long_shots: power long shots score (1-100)
  mentality_aggression: mentality aggression score (1-100)
  mentality_interceptions: mentality interceptions score (1-100)
  mentality_positioning: mentality positioning score (1-100)
  mentality_vision: mentality vision score (1-100)
  mentality_penalties: mentality penalties score (1-100)
  mentality_composure: mentality composure score (1-100)
  defending_marking: defending marking score (1-100)
  defending_standing_tackle: defending standing tackle score (1-100)
  defending_sliding_tackle: defending sliding tackle score (1-100)
  goalkeeping_diving: goalkeeping diving score (1-100)
  goalkeeping_handling: goalkeeping handling score (1-100)
  goalkeeping_kicking: goalkeeping kicking score (1-100)
  goalkeeping_positioning: goalkeeping positioning score (1-100)
  goalkeeping_reflexes: goalkeeping reflexes score (1-100)
  playstyles: multiple playstyles of player
  overall_LS: overall as Left Stiker
  potential_LS: potential as Left Stiker
  overall_ST: overall as Striker
  potential_ST: overall as Striker
  overall_RS: overall as Right stiker
  potential_RS: potential as Right stiker
  overall_LW: overall as Left Winger
  potential_LW: potential as Left Winger
  overall_LF: overall as left Forward
  potential_LF: potential as left Forward
  overall_RF: overall as Right Forward
  potential_RF: potential as Right Forward
  overall_RW: overall as Right Winger
  potential_RW: potential as Right Winger
  overall_LAM: overall as Left Attacking Midfielder
  potential_LAM: potential as Left Attacking Midfielder
  overall_CAM: overall as Center Midfielder
  potential_CAM: potential as Center Midfielder
  overall_RAM: overall as Right Attacking Midfielder
  potential_RAM: potential as Right Attacking Midfielder
  overall_LM: overall as Left Midfielder
  potential_LM: potential as Left Midfielder
  overall_LCM: overall as Left Center Midfielder
  potential_LCM: potential as Left Center Midfielder
  overall_CM: overall as Center Midfielder
  potential_CM: potential as Center Midfielder
  overall_RCM: overall as Right Center Midfielder
  potential_RCM: potential as Right Center Midfielder
  overall_RM: overall as Right Midfielder
  potential_RM: potential as Right Midfielder
  overall_LDM: overall as Left Defensive Midfielder
  potential_LDM: potential as Left Defensive Midfielder
  overall_CDM: overall as Center Defensive Midfielder
  potential_CDM: potential as Center Defensive Midfielder
  overall_RDM: overall as Right Defensive Midfielder
  potential_RDM: potential as Right Defensive Midfielder
  overall_LB: overall as Left Back
  potential_LB: potential as Left Back
  overall_LCB: overall as Left Center Back
  potential_LCB: potential as Left Center Back
  overall_CB: overall as Center Back
  potential_CB: potential as Center Back
  overall_RCB: overall as Right Center Back
  potential_RCB: potential as Right Center Back
  overall_RB: overall as Right Back
  potential_RB: potential as Right Back
  overall_GK: overall as GoalKeeper
  potential_GK: potential as GoalKeeper
  """
  #initializing webscrapping
  driver = web_driver()
  driver.get(player_url)

  name = driver.find_element(By.CLASS_NAME, "ellipsis").text
  profile = driver.find_element(By.CLASS_NAME, "profile").text.split('\n')
  full_name = profile[1]
  country = driver.find_element(By.XPATH, '/html/body/main[1]/article/div[1]/p/a').get_attribute('title')
  position = profile[2]
  age = int(profile[3].split(" ")[0].split('y')[0])
  date_of_birth = " ".join(profile[3].split(" ")[1:4])[1:-1]
  height_cm = int(profile[3].split(" ")[4][:-2])
  height_ft = profile[3].split(" ")[6]
  height_ft = height_ft.replace('/', '')
  height_ft = height_ft.replace('"', '')
  weight_kg = profile[3].split(" ")[7][:-2]
  weight_lb = profile[3].split(" ")[9][:-3]
  
  overall = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[2]/div[1]/em").text)
  potential = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[2]/div[2]/em").text)
  value = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[2]/div[3]/em").text
  wage = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[2]/div[4]/em").text
  
  likes = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/button[1]/span").text)
  dislikes = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/button[2]/span").text)
  follow = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/button[3]/span").text)
  
  preferred_foot = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[1]/p[1]").text.split(" ")[-1]
  skill_moves = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[1]/p[2]").text.split(" ")[0])
  weak_foot = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[1]/p[3]").text.split(" ")[0])
  international_reputation = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[1]/p[4]").text.split(" ")[0])
  body_type = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[1]/p[5]").text.split(" ")[-1]
  real_face = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[1]/p[6]").text.split(" ")[-1]
  release_clause = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[1]/p[7]").text.split(" ")[0]
  acceleration_type = " ".join(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[1]/p[8]").text.split(' ')[2:])
  
  specialities_list = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[2]").text.split('\n')[1:]
  specialities = ", ".join(specialities_list)
  specialities = specialities.replace('#', '')

  #if driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[3]/h5").text == 'Club':
  club = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[3]/p[1]/a").text
  club_league = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[3]/p[2]/a").text
  club_overall = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[3]/p[3]").text)
  club_position = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[3]/p[4]/span").text
  club_kit_num = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[3]/p[5]").text.split(" ")[-1]
  club_joined_date = " ".join(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[3]/p[6]").text.split(" ")[1:])
  club_contract_expire = " ".join(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[3]/p[7]").text.split(" ")[3:])
  #elif driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[4]/h5").text == 'Club':
    #club = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[4]/p[1]/a/").text
    #club_league = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[4]/p[2]/a").text
    #club_overall = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[4]/p[3]").text)
    #club_position = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[4]/p[4]/span").text
    #club_kit_num = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[4]/p[5]").text.split(" ")[-1]
    #club_joined_date = " ".join(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[4]/p[6]").text.split(" ")[1:])
    #club_contract_expire = " ".join(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[4]/div[4]/p[7]").text.split(" ")[3:])

  attacking_crossing = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[1]/p[1]/em").text)
  attacking_finishing = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[1]/p[2]/em").text)
  attacking_heading_accuracy = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[1]/p[3]/em").text)
  attacking_short_passing = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[1]/p[4]/em").text)
  attacking_volleys = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[1]/p[5]/em").text)
  
  skill_dribbling = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[2]/p[1]/em").text)
  skill_curve = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[2]/p[2]/em").text)
  skill_fk_accuracy = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[2]/p[3]/em").text)
  skill_long_passing = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[2]/p[4]/em").text)
  skill_ball_control = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[2]/p[5]/em").text)
  
  movement_acceleration = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[3]/p[1]/em").text)
  movement_sprint_speed = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[3]/p[2]/em").text)
  movement_agility = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[3]/p[3]/em").text)
  movement_reactions = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[3]/p[4]/em").text)
  movement_balance = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[3]/p[5]/em").text)
  
  power_shot_power = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[4]/p[1]/em").text)
  power_jumping = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[4]/p[2]/em").text)
  power_stamina = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[4]/p[3]/em").text)
  power_strength = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[4]/p[4]/em").text)
  power_long_shots = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[7]/div[4]/p[5]/em").text)

  mentality_aggression = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[8]/div[1]/p[1]/em").text)
  mentality_interceptions = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[8]/div[1]/p[2]/em").text)
  mentality_positioning = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[8]/div[1]/p[3]/em").text)
  mentality_vision = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[8]/div[1]/p[4]/em").text)
  mentality_penalties = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[8]/div[1]/p[5]/em").text)
  mentality_composure = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[8]/div[1]/p[6]/em").text)

  defending_marking = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[8]/div[2]/p[1]/em").text)
  defending_standing_tackle = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[8]/div[2]/p[2]/em").text)
  defending_sliding_tackle = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[8]/div[2]/p[3]/em").text)

  goalkeeping_diving = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[8]/div[3]/p[1]/em").text)
  goalkeeping_handling = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[8]/div[3]/p[2]/em").text)
  goalkeeping_kicking = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[8]/div[3]/p[3]/em").text)
  goalkeeping_positioning = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[8]/div[3]/p[4]/em").text)
  goalkeeping_reflexes = int(driver.find_element(By.XPATH, "/html/body/main[1]/article/div[8]/div[3]/p[5]/em").text)

  playstyles_list = driver.find_element(By.XPATH, "/html/body/main[1]/article/div[8]/div[4]").text.split('\n')[1:]
  playstyles = ", ".join(playstyles_list)


  LS = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[1]/div[2]/div/em").text.split('+')
  overall_LS = int(LS[0])
  potential_LS = int(LS[0]) + int(LS[1])

  ST = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[1]/div[3]/div/em").text.split('+')
  overall_ST = int(ST[0])
  potential_ST = int(ST[0]) + int(ST[1])

  RS = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[1]/div[4]/div/em").text.split('+')
  overall_RS = int(RS[0])
  potential_RS = int(RS[0]) + int(RS[1])

  LW = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[2]/div[1]/div/em").text.split('+')
  overall_LW = int(LW[0])
  potential_LW = int(LW[0]) + int(LW[1])

  LF = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[2]/div[2]/div/em").text.split('+')
  overall_LF = int(LF[0])
  potential_LF = int(LF[0]) + int(LF[1])

  RF = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[2]/div[4]/div/em").text.split('+')
  overall_RF = int(RF[0])
  potential_RF = int(RF[0]) + int(RF[1])

  RW = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[2]/div[5]/div/em").text.split('+')
  overall_RW = int(RW[0])
  potential_RW = int(RW[0]) + int(RW[1])

  LAM = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[3]/div[2]/div/em").text.split('+')
  overall_LAM = int(LAM[0])
  potential_LAM = int(LAM[0]) + int(LAM[1])

  CAM = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[3]/div[3]/div/em").text.split('+')
  overall_CAM = int(CAM[0])
  potential_CAM = int(CAM[0]) + int(CAM[1])

  RAM = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[3]/div[4]/div/em").text.split('+')
  overall_RAM = int(RAM[0])
  potential_RAM = int(RAM[0]) + int(RAM[1])

  LM = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[4]/div[1]/div/em").text.split('+')
  overall_LM = int(LM[0])
  potential_LM = int(LM[0]) + int(LM[1])

  LCM = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[4]/div[2]/div/em").text.split('+')
  overall_LCM = int(LCM[0])
  potential_LCM = int(LCM[0]) + int(LCM[1])

  CM = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[4]/div[3]/div/em").text.split('+')
  overall_CM = int(CM[0])
  potential_CM = int(CM[0]) + int(CM[1])

  RCM = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[4]/div[4]/div/em").text.split('+')
  overall_RCM = int(RCM[0])
  potential_RCM = int(RCM[0]) + int(RCM[1])

  RM = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[4]/div[5]/div/em").text.split('+')
  overall_RM = int(RM[0])
  potential_RM = int(RM[0]) + int(RM[1])

  LDM = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[5]/div[2]/div/em").text.split('+')
  overall_LDM = int(LDM[0])
  potential_LDM = int(LDM[0]) + int(LDM[1])

  CDM = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[5]/div[3]/div/em").text.split('+')
  overall_CDM = int(CDM[0])
  potential_CDM = int(CDM[0]) + int(CDM[1])

  RDM = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[5]/div[4]/div/em").text.split('+')
  overall_RDM = int(RDM[0])
  potential_RDM = int(RDM[0]) + int(RDM[1])

  LB = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[6]/div[1]/div/em").text.split('+')
  overall_LB = int(LB[0])
  potential_LB = int(LB[0]) + int(LB[1])

  LCB = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[6]/div[2]/div/em").text.split('+')
  overall_LCB = int(LCB[0])
  potential_LCB = int(LCB[0]) + int(LCB[1])  

  CB = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[6]/div[3]/div/em").text.split('+')
  overall_CB = int(CB[0])
  potential_CB = int(CB[0]) + int(CB[1])

  RCB = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[6]/div[4]/div/em").text.split('+')
  overall_RCB = int(RCB[0])
  potential_RCB = int(RCB[0]) + int(RCB[1])

  RB = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[6]/div[5]/div/em").text.split('+')
  overall_RB = int(RB[0])
  potential_RB = int(RB[0]) + int(RB[1])

  GK = driver.find_element(By.XPATH, "/html/body/main[1]/aside/div[1]/div[1]/div/div[7]/div[3]/div/em").text.split('+')
  overall_GK = int(GK[0])
  potential_GK = int(GK[0]) + int(GK[1])

  driver.quit()

  player_dict = {
      'name': name,
      'full_name': full_name,
      'country': country,
      'position': position,
      'age': age,
      'date_of_birth': date_of_birth,
      'height_cm': height_cm,
      'height_ft': height_ft,
      'weight_kg': weight_kg,
      'weight_lb': weight_lb,
      'overall': overall,
      'potential': potential,
      'value': value,
      'wage': wage,
      'likes': likes,
      'dislikes': dislikes,
      'follow': follow,
      'preferred_foot': preferred_foot,
      'skill_moves': skill_moves,
      'weak_foot': weak_foot,
      'international_reputation': international_reputation,
      'body_type': body_type,
      'real_face': real_face,
      'release_clause': release_clause,
      'acceleration_type': acceleration_type,
      'specialities': specialities,
      'club': club,
      'club_league': club_league,
      'club_overall': club_overall,
      'club_position': club_position,
      'club_kit_num': club_kit_num,
      'club_joined_date': club_joined_date,
      'club_contract_expire': club_contract_expire,
      'attacking_crossing': attacking_crossing,
      'attacking_finishing': attacking_finishing,
      'attacking_heading_accuracy': attacking_heading_accuracy,
      'attacking_short_passing': attacking_short_passing,
      'attacking_volleys': attacking_volleys,
      'skill_dribbling': skill_dribbling,
      'skill_curve': skill_curve,
      'skill_fk_accuracy': skill_fk_accuracy,
      'skill_long_passing': skill_long_passing,
      'skill_ball_control': skill_ball_control,
      'movement_acceleration': movement_acceleration,
      'movement_sprint_speed': movement_sprint_speed,
      'movement_agility': movement_agility,
      'movement_reactions': movement_reactions,
      'movement_balance': movement_balance,
      'power_shot_power': power_shot_power,
      'power_jumping': power_jumping,
      'power_stamina': power_stamina,
      'power_strength': power_strength,
      'power_long_shots': power_long_shots,
      'mentality_aggression': mentality_aggression,
      'mentality_interceptions': mentality_interceptions,
      'mentality_positioning': mentality_positioning,
      'mentality_vision': mentality_vision,
      'mentality_penalties': mentality_penalties,
      'mentality_composure': mentality_composure,
      'defending_marking': defending_marking,
      'defending_standing_tackle': defending_standing_tackle,
      'defending_sliding_tackle': defending_sliding_tackle,
      'goalkeeping_diving': goalkeeping_diving,
      'goalkeeping_handling': goalkeeping_handling,
      'goalkeeping_kicking': goalkeeping_kicking,
      'goalkeeping_positioning': goalkeeping_positioning,
      'goalkeeping_reflexes': goalkeeping_reflexes,
      'playstyles': playstyles,
      'overall_LS': overall_LS,
      'potential_LS': potential_LS,
      'overall_ST': overall_ST,
      'potential_ST': potential_ST,
      'overall_RS': overall_RS,
      'potential_RS': potential_RS,
      'overall_LW': overall_LW,
      'potential_LW': potential_LW,
      'overall_LF': overall_LF,
      'potential_LF': potential_LF,
      'overall_RF': overall,
      'potential_RF': potential_RF,
      'overall_RW': overall_RW,
      'potential_RW': potential_RW,
      'overall_LAM': overall_LAM,
      'potential_LAM': potential_LAM,
      'overall_CAM': overall_CAM,
      'potential_CAM': potential_CAM,
      'overall_RAM': overall_RAM,
      'potential_RAM': potential_RAM,
      'overall_LM': overall_LM,
      'potential_LM': potential_LM,
      'overall_LCM': overall_LCM,
      'potential_LCM': potential_LCM,
      'overall_CM': overall_CM,
      'potential_CM': potential_CM,
      'overall_RCM': overall_RCM,
      'potential_RCM': potential_RCM,
      'overall_RM': overall_RM,
      'potential_RM': potential_RM,
      'overall_LDM': overall_LDM,
      'potential_LDM': potential_LDM,
      'overall_CDM': overall_CDM,
      'potential_CDM': potential_CDM,
      'overall_RDM': overall_RDM,
      'potential_RDM': potential_RDM,
      'overall_LB': overall_LB,
      'potential_LB': potential_LB,
      'overall_LCB': overall_LCB,
      'potential_LCB': potential_LCB,
      'overall_CB': overall_CB,
      'potential_CB': potential_CB,
      'overall_RCB': overall_RCB,
      'potential_RCB': potential_RCB,
      'overall_RB': overall_RB,
      'potential_RB': potential_RB,
      'overall_GK': overall_GK,
      'potential_GK': potential_GK,
  }
  return player_dict

def scrape_players2(league_ids, offset_num, type_='all', version='250016', feature_mode='all', features=None):
  """
  argumets:
    league_ids (integer): ids of leagues e.g. England Premier League ID is 13 check scrape_leagues() for more info
    offset_num (integer): specifies number of players to scrape e.g. offset_nu of 120 will scrape first two pages and maximum 120 players
    type (string):
      "all": will consider all players in current roster
      "added": will consider only added players to version
      "updated": will consider only updated players on current version
      "free": will consider only free players on current version
      "onLoan": will consider only on Loan players on current version
      "removed": will consider only removed players from current version
      "history": will consider all players on history
    version (string): version of sofifa
    feature_mode (string):
      "all": output all possible features
      "include": output a list of given features
      "exclude": output all possible features except list of given features
    features (list): list of given features
    *** You don'y need to modify this argument if feature_mode is set on "all" ***
    player_mode (string):
      "all": will consider all players of team including squad players and loan players
      "squad": will consider only squad players
      "loan": will consider only loan players
  this will result dataframe consist of all players information in selected team
  columns: desired features
  """

  # dictionary of feature names and their code
  feature_mapping_dict = player_features_dict()

  # considering different situations for how to output playerrs features
  if feature_mode == 'all':
    features = list(feature_mapping_dict.keys())
  elif feature_mode == 'include':
    features = list(set(feature_mapping_dict.keys()) & set(features))
  elif feature_mode == 'exclude':
    features = list(set(feature_mapping_dict.keys()) - set(features))
  else:
    raise ValueError("feature_mode must be 'all', 'include' or 'exclude'")

  # specifying a general xpath
  xpath = "/html/body/main[1]/article/table"

  def url_maker(league_ids, ver):
    base_url = "https://sofifa.com/players?type=all"
    type_url = f"?type={type_}"
    final_url = base_url + type_url
    for l in league_ids:
      final_url += f"&lg%5B%5D={l}"
    #feature_url = ""
    for f in features:
      final_url += f"&showCol%5B%5D={feature_mapping_dict[f]}"
    version_url = f"&r={ver}&set=true"
    final_url = final_url + version_url
    return final_url

  num_pages = offset_num // 60 + 1

  urls = []
  for i in range(num_pages):
    offset_number = str(60*i)
    urls.append(url_maker(league_ids, version) + f"&offset={offset_number}")

  def form_df(url):
    driver = web_driver()
    driver.get(url)

    # getting basic information
    player_elements1 = driver.find_elements(By.XPATH, xpath + '//a[contains(@href, "/player/")]')
    player_names = []
    player_full_names = []
    player_urls = []

    for player in player_elements1:
      player_name = player.text  # Extract the displayed name
      player_full_name = player.get_attribute('data-tippy-content')  # Full name from attribute
      player_url = player.get_attribute('href')  # Full URL
      player_names.append(player_name)
      player_full_names.append(player_full_name)
      player_urls.append(player_url)

    player_elements2 = driver.find_elements(By.XPATH, xpath + '//img[contains(@class, "flag")]')
    countries = []

    for player in player_elements2:
      countries.append(player.get_attribute('title'))

    player_elements3 = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/team/"]')
    clubs = []

    for player in player_elements3:
      clubs.append(player.text)


    # forming up a base dataframe
    df = pd.DataFrame(
        {
            'player_names': player_names,
            'player_full_names': player_full_names,
            'player_urls': player_urls,
            'countries': countries,
            'club': clubs
        }
    )

    # adding desired features
    for f in features:
      val = feature_mapping_dict[f]
      td_elements = driver.find_elements(By.XPATH, xpath + f'//td[@data-col="{val}"]')
      values = [element.text for element in td_elements]
      df[f] = values

    return df

  problem_urls = []
  df = form_df(urls[0])
  # First iteration: Attempt to scrape all URLs
  for url in tqdm(urls[1:]):
    try:
      df = pd.concat([df, form_df(url)], ignore_index=True)
    except:
      problem_urls.append(url)

  # Continuously retry scraping problematic URLs until all are resolved
  while problem_urls:
    print(f"Retrying {len(problem_urls)} problematic URLs...")
    retry_urls = problem_urls.copy()  # Create a copy of the list to iterate over
    problem_urls = []  # Clear the list for the next iteration

    for url in tqdm(retry_urls):
      try:
        df = pd.concat([df, form_df(url)], ignore_index=True)
      except Exception as e:
        problem_urls.append(url)  # Add the URL back to the list if it fails again
        print(f"Failed to scrape {url}. Error: {e}")

    # Optional: Add a delay between retries to avoid overwhelming the server
    time.sleep(5)  # Adjust the delay as needed

  df['version'] = version

  return df
