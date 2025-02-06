from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up ChromeDriver service
service = Service(executable_path='./chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Open WhatsApp Web
driver.get('https://web.whatsapp.com')
print("WhatsApp Web opened. Please scan the QR code.")

# Wait for user to scan QR code and for WhatsApp to load
wait = WebDriverWait(driver, 60)
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
print("QR Code scanned successfully!")

# Define the contact/group name and message
contact_name = "budget home"
message = "Hello! I can help you with budgeting. Type 'budget' to start."

# Search for the contact
search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
search_box.click()
search_box.clear()
search_box.send_keys(contact_name)
search_box.send_keys(Keys.ENTER)

# Wait for the message box to appear
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')))

# Send the message
msg_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
msg_box.click()
msg_box.send_keys(message)
msg_box.send_keys(Keys.ENTER)

print("Message sent successfully!")
time.sleep(5)

# Close the browser
driver.quit()
