# 🚀 Google Maps Photos Scraper


This is a Python tool designed to extract high-quality image URLs from the Google Maps photo gallery. This scraper leverages Selenium to navigate the dynamic interface of Google Maps and extract thumbnail URLs from the left panel, ensuring you always get the latest images for your projects.

---

## ✨ Features

- **Dynamic Navigation:** Automatically searches for a specified place and opens the photo gallery.
- **Robust Gallery Extraction:** Uses multiple selectors and error handling to adapt to UI changes.
- **URL Standardization:** Converts image URLs to a consistent format (e.g., resolution set to `=s0`).
- **Next Button Navigation:** Iterates through gallery pages to capture additional images.
- **Easy-to-Use:** Simple, modular code that can be extended and customized for your needs.

---

## ⚙️ Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/naradashen/Google-Maps-Photos-Scraper.git
   ```

   ```bash
   cd google-maps-image-scraper
   ```

2. **Activate the virtual environment:**
    
    ```bash
    python3 -m venv venv
    ```

    ```bash
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip3 install selenium requests

---

## 🚀 Usage

1. **Update settings:**

- Open 'main.py' and adjust parameters as desired.
- Change the target location by modifying the 'place_name' variable in the main() function (line 29).

2. **Run the scraper:**

    ```bash
    python3 main.py
    ```

3. **Results:**

- The extracted image URLs will be saved as a JSON file in the 'extracted_data' folder.

---

## ⚠️ Note on Dynamic Content & Error Handling

Google Maps is a highly dynamic platform that frequently updates its interface and underlying DOM structure. As a result, you might encounter occasional errors such as:

- **Element Not Found:** The photo gallery button or thumbnail container may have updated attributes.
- **Scrolling Issues:** Dynamic content loading can affect the scroll behavior of the thumbnail container.
- **Timeouts:** Elements may take longer to load during periods of high traffic or due to network conditions.

*This repository is provided as a starting point. Users are encouraged to modify and enhance the code according to their specific requirements and changes in the Google Maps interface.*
