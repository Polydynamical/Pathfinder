import sys
import tqdm
from selenium import webdriver

urls = open(f"{sys.argv[1]}.txt").readlines()
out = open(f"out{sys.argv[1]}.txt", "a")
driver = webdriver.Firefox()

for url in tqdm.tqdm(urls):
    driver.get(url)
    initial = driver.current_url
    while driver.current_url == initial:
        pass
    
    out.write(driver.current_url + "\n")
    out.flush()


