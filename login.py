from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome options to keep session active
chrome_options = Options()
chrome_options.add_argument(r"user-data-dir=C:\Users\mohda\AppData\Local\Google\Chrome\User Data\Default")

# Initialize the driver
service = Service(executable_path='./chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open WhatsApp Web
driver.get('https://web.whatsapp.com')
print("WhatsApp Web opened. Waiting for QR code scan if needed...")

# Wait until the search box is present (user has scanned QR code)
wait = WebDriverWait(driver, 60)
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
print("Logged in successfully!")

# Define your group name
group_name = "Budget home"


# Search for the group and ensure the element is fresh before sending keys
def search_and_open_group():
    try:
        # Re-find the search box to avoid stale element reference
        search_box = wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
        search_box.clear()
        search_box.send_keys(group_name)
        time.sleep(2)  # Give WhatsApp time to show the search result

        # Locate the chat after it appears
        chat = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[@title="{group_name}"]')))
        chat.click()

        print(f"Opened group: {group_name}")

    except Exception as e:
        print(f"Error while opening the group: {e}")


# Call the function to open the group
search_and_open_group()

# Your further logic to read messages and tally expenses goes here

# Close after operations
time.sleep(5)
driver.quit()
