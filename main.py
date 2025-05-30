from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json
import re

# === CONFIG ===
PLACE_NAME    = "caltech"
OUTPUT_DIR    = "extracted_data"
OUTPUT_FILE   = os.path.join(OUTPUT_DIR, "image_urls.json")
SCROLL_STEP   = 2000    # px per scroll
SCROLL_PAUSE  = 1.0    # seconds
MAX_NO_CHANGE = 5     # stop after this many scrolls with no new content

# prepare
os.makedirs(OUTPUT_DIR, exist_ok=True)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
wait   = WebDriverWait(driver, 20)

# 1) search place
driver.get("https://www.google.com/maps")
search = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
search.send_keys(PLACE_NAME, Keys.RETURN)
time.sleep(5)

# 2) open “All” gallery
all_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='All']")))
all_btn.click()
time.sleep(5)

# 3) locate the gallery panel
gallery = wait.until(EC.presence_of_element_located((
    By.CSS_SELECTOR,
    "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde"
)))

# 4) prepare extraction
URL_RE = re.compile(
    r'url\((?:&quot;|["\']?)(https?://lh3\.googleusercontent\.com[^)"\']+)(?:&quot;|["\']?)\)'
)

image_urls = set()

def extract_from_gallery():
    # every tile is <a class="OKAoZd"> → contains <div.U39Pmb role="img">
    tiles = gallery.find_elements(By.CSS_SELECTOR, "a.OKAoZd div.U39Pmb[role='img']")
    for tile in tiles:
        style = tile.get_attribute("style") or ""
        m = URL_RE.search(style)
        if m:
            url = m.group(1)
            if url not in image_urls:
                image_urls.add(url)
                print(url)
        # nested high-res
        nested = tile.find_elements(By.CSS_SELECTOR, "div.Uf0tqf.loaded[style*='background-image']")
        for div in nested:
            s2 = div.get_attribute("style") or ""
            m2 = URL_RE.search(s2)
            if m2:
                url2 = m2.group(1)
                if url2 not in image_urls:
                    image_urls.add(url2)
                    print(url2)

# 5) smooth, incremental scroll until no new tiles
last_height = driver.execute_script("return arguments[0].scrollHeight", gallery)
no_change   = 0

while True:
    extract_from_gallery()
    # scroll down
    driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", gallery, SCROLL_STEP)
    time.sleep(SCROLL_PAUSE)

    new_height = driver.execute_script("return arguments[0].scrollHeight", gallery)
    if new_height == last_height:
        no_change += 1
        if no_change >= MAX_NO_CHANGE:
            break
    else:
        last_height = new_height
        no_change    = 0

# 6) save results
with open(OUTPUT_FILE, "w") as f:
    json.dump(sorted(image_urls), f, indent=2)

print(f"Done! Extracted {len(image_urls)} URLs → {OUTPUT_FILE}")
driver.quit()
