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
