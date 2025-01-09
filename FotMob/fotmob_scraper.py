# installs
!pip install selenium
!apt-get install chromium-driver

# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

## defining user agent is mandatory
#user_agent_string = "define_a_user_agent_string"

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

def scrape_urls(competition, season):
  """
  arguments:
    competition: string for example:
      English Premier League: "premier-league"
    season: string for example:
      2023-2024: "2023-2024"
  """
  match_urls = []
  match_url_list_by_round = [f"https://www.fotmob.com/leagues/47/matches/{competition}?group=by-round&round={str(i)}&season={season}" for i in range(1,39)]
  
  for url in match_url_list_by_round:
    driver = web_driver()
    driver.get(url)
    for any in driver.find_elements(By.TAG_NAME, 'a'):
      match_url = any.get_attribute('href')
      if '/matches/' in match_url and match_url not in match_urls and '/leagues/' not in match_url:
        match_urls.append(match_url)

  driver.quit()
  return match_urls

def scrape_stats(match_url):
  """
  arguments: match url in string
  """
  stats_url = match_url + ':tab=stats'
  driver = web_driver()
  driver.get(match_url)

  stats = []
  home = []
  away = []

  for element in driver.find_elements(By.CSS_SELECTOR, '.css-9e8ls0-TopStatsContainer .css-1l9ti9s-Stat'):
    for ele in element.find_elements(By.CLASS_NAME, 'title'):
      stats.append(ele.text)
    for ele in element.find_elements(By.CLASS_NAME, 'css-129ncdm-StatBox'):
      home.append(ele.text)
    for ele in element.find_elements(By.CLASS_NAME, 'css-1t9answ-StatBox'):
      away.append(ele.text)

  dataframe = pd.DataFrame(
      {
          'stats': stats,
          'home': home,
          'away': away
      }
  )
  return dataframe
