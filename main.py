from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json
import re

# Initialize WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Uncomment for headless mode
driver = webdriver.Chrome(options=options)

# Navigate to Google Maps
driver.get("https://www.google.com/maps")

# Wait for the search box and perform the search
try:
    search_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "searchboxinput"))
    )
except Exception as e:
    print("Search box not found:", e)
    driver.quit()
    exit()

place_name = "unawatuna beach"
search_box.send_keys(place_name)
search_box.send_keys(Keys.RETURN)
time.sleep(5)

# Click the "All" button to open the full photo gallery
try:
    all_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='All']"))
    )
    all_button.click()
    time.sleep(5)  # Allow gallery to open
except Exception as e:
    print("Error clicking 'All' button:", e)

# Create or open the output folder for JSON file
output_folder = "extracted_data"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Initialize list to store image URLs
image_urls = []

# Function to extract image URLs from the left-side panel
def extract_image_urls():
    try:
        # Locate all div elements with the class "Uf0tqf loaded" in the left-side panel
        image_divs = driver.find_elements(By.CSS_SELECTOR, "div.Uf0tqf.loaded")
        for div in image_divs:
            # Extract the style attribute
            style = div.get_attribute("style")
            # Use regex to extract the URL from the background-image property
            match = re.search(r'url\("([^"]+)"\)', style)
            if match:
                image_url = match.group(1)
                # Validate that the URL is a Google Photos URL
                if image_url.startswith("https://lh5.googleusercontent.com") and image_url not in image_urls:
                    image_urls.append(image_url)
                    print(f"Extracted image URL: {image_url}")
    except Exception as e:
        print("Error extracting image URLs:", e)

# Function to click the Next button
def click_next_button():
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Next']"))
        )
        next_button.click()
        time.sleep(2)  # Wait for the next image to load
        return True
    except Exception as e:
        print("Error clicking Next button:", e)
        return False

# Extract image URLs from all photos
max_images = 50  # Set a maximum number of images to capture
for i in range(max_images):
    try:
        # Extract URLs from the left-side panel
        extract_image_urls()

        # Click the Next button to move to the next image
        if not click_next_button():
            break  # Stop if there are no more images
    except Exception as e:
        print(f"Error processing image {i+1}: {e}")
        break

# Save the image URLs to a JSON file
json_filename = os.path.join(output_folder, "image_urls.json")
with open(json_filename, "w") as f:
    json.dump(image_urls, f, indent=4)
print(f"Image URLs saved to {json_filename}")

# Close the browser after extraction
driver.quit()

print("Image URL extraction complete.")
