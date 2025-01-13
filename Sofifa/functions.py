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
