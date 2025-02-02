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


---

## ⚙️ Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/naradashen/Google-Maps-Photos-Scraper.git
   cd google-maps-image-scraper

2. **Activate the virtual environment:**
    
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install rependencies:**

    ```bash
    pip3 install selenium requests
