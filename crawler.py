#!/c/Python38/python

import time
import itertools
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


WEBDRIVER_PATH = 'vendor/chromedriver.exe'
ROOT_URL = 'https://www.nagumo.com.br/santo-andre-lj26-abc-sao-paulo-vila-marina-rua-coronel-seabra'
# ROOT_URL = 'http://localhost/wpplugin/'

INITIAL_RENDERING_TIMEOUT = 10
SCROLL_PAUSE_TIME = 0.8

driver = webdriver.Chrome(WEBDRIVER_PATH)



def is_valid_link(href):
  if href is None:
    return False
  
  if href == '' or href.find('javascript') != -1:
    return False

  root_domain = urlparse(ROOT_URL).netloc
  href_domain = urlparse(href).netloc

  if href_domain != root_domain:
    return False

  return True


def scroll_page():  
  last_height = driver.execute_script('return document.body.scrollHeight')
  time.sleep(SCROLL_PAUSE_TIME)

  while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    new_height = driver.execute_script('return document.body.scrollHeight')

    if new_height == last_height:
      break

    last_height = new_height

    time.sleep(SCROLL_PAUSE_TIME)


def scrap_links(url):
  driver.get(url)
  time.sleep(3)

  try:
    WebDriverWait(driver, INITIAL_RENDERING_TIMEOUT).until(
      EC.presence_of_element_located((By.LINK_TEXT, 'Site Institucional'))
    )
  except TimeoutException:
    print('TimeoutException at ' + url)
  
  scroll_page()

  links = driver.find_elements_by_css_selector('a')

  valid_links = []

  for link in links:
    href = link.get_attribute('href')
    
    if is_valid_link(href):
      href_without_hash = href.split('#')[0]
      valid_links.append(href_without_hash)
  
  return valid_links


def save_link(link, filename):
  with open(filename, 'a+') as file:
    file.write(link + '\n')


def save_links(links, filename):
  with open(filename, 'a+') as file:
    for link in links:
      file.write(link + '\n')


def debug_print_links(links):
  for link in links:
    print(link)


def summary_print(current, scrapped, recently_scrapped, to_scrap):
  print(f'\nScrapping: {current_link}')
  print(f'Scrapped {len(scrapped)} links. Got {len(recently_scrapped)}. {len(to_scrap)} links to go.\n')



if __name__ == '__main__':
  scrapped = []
  to_scrap = [ROOT_URL]
  starting_time = int(round(time.time() * 1000))

  scrapped_links_filename = f'scrapped-links-{starting_time}.txt'
  not_scrapped_links_filename = f'to-scrap-{starting_time}.txt'

  save_link(ROOT_URL, not_scrapped_links_filename)

  def not_seen(link):
    return link not in scrapped and link not in to_scrap

  while len(to_scrap) > 0:
    current_link = to_scrap.pop(0)
    links = scrap_links(current_link)
    scrapped.append(current_link)
    save_link(current_link, scrapped_links_filename)

    not_scrapped, not_scrapped_print, recently_scrapped = itertools.tee(filter(not_seen, links), 3)
    to_scrap.extend(not_scrapped)

    not_scrapped_print = list(not_scrapped_print)
    recently_scrapped = list(recently_scrapped)
    save_links(not_scrapped_print, not_scrapped_links_filename)
    summary_print(current_link, scrapped, recently_scrapped, to_scrap)

  driver.close()

  print('\nFinished scrapping!')
  debug_print_links(scrapped)
