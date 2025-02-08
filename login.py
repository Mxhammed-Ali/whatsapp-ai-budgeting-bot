from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parser import WhatsAppParser  # Import the parser class
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument(r"user-data-dir=C:\Users\mohda\AppData\Local\Google\Chrome\User Data\Default")

# Initialize the driver
service = Service(executable_path='./chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open WhatsApp Web
driver.get('https://web.whatsapp.com')
print("WhatsApp Web opened. Waiting for QR code scan if needed...")

# Wait for WhatsApp Web to load
# Wait until the search box is present (user has scanned QR code)
wait = WebDriverWait(driver, 60)
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
print("Logged in successfully!")

# Initialize WhatsAppParser
group_name = "Budget home"
parser = WhatsAppParser(driver, wait, group_name)

# Perform parsing steps
parser.open_group()
parser.scroll_messages()
parser.extract_and_save_messages()

# Close after operations
time.sleep(5)
driver.quit()
