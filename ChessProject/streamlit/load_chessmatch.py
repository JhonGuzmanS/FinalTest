from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# PATH = r"C:\Program Files\Google\Chrome\Application/chrome.exe"
#driver = webdriver.Chrome()

def open_match(text):
    driver = webdriver.Chrome()
    url = "https://www.chess.com/analysis?tab=analysis"
    driver.get(url)
    button = driver.find_element(By.CSS_SELECTOR, '[data-cy="add-games-btn"]')
    textarea = driver.find_element(By.CSS_SELECTOR, '[data-cy="pgn-textarea"]')
    textarea.send_keys(text)
    button.click()


