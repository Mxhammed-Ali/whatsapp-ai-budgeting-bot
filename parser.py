from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
import csv
import time
import os

class WhatsAppParser:
    def __init__(self, driver, wait, group_name="Budget home"):
        self.driver = driver
        self.wait = wait
        self.group_name = group_name

    def open_group(self):
        """Searches and opens the specified WhatsApp group."""
        try:
            search_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            search_box.clear()
            search_box.send_keys(self.group_name)
            time.sleep(2)

            chat = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f'//span[@title="{self.group_name}"]'))
            )
            chat.click()
            print(f"Opened group: {self.group_name}")
        except Exception as e:
            print(f"Error while opening the group: {e}")

    def scroll_messages(self, scroll_count=50):
        """Scrolls up to load older messages."""
        try:
            message_container = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chat-history"]'))
            )
            print("Scrolling through messages...")

            for _ in range(scroll_count):
                ActionChains(self.driver).move_to_element(message_container).click().perform()
                ActionChains(self.driver).send_keys(Keys.PAGE_UP).perform()
                time.sleep(0.5)

            print("Finished scrolling.")
        except Exception as e:
            print(f"Error while scrolling: {e}")

    def extract_and_save_messages(self):
        """Extracts messages from the past 7 days and saves them to a CSV file."""
        messages = self.driver.find_elements(By.XPATH, '//div[contains(@class, "message-in") or contains(@class, "message-out")]')
        today = datetime.now()
        seven_days_ago = today - timedelta(days=7)

        extracted_data = []

        for message in messages:
            try:
                timestamp_element = message.find_element(By.XPATH, './/div[contains(@data-pre-plain-text, "[")]')
                timestamp_text = timestamp_element.get_attribute('data-pre-plain-text')
                date_str = timestamp_text.split(']')[0][1:]

                msg_date = datetime.strptime(date_str, '%I:%M %p, %m/%d/%Y')

                if msg_date >= seven_days_ago:
                    try:
                        sender = timestamp_text.split('] ')[1].strip().replace(':', '')
                    except IndexError:
                        sender = "Unknown"

                    try:
                        msg_text = message.find_element(By.XPATH, './/span[contains(@class, "selectable-text")]').text
                    except:
                        try:
                            msg_text = message.find_element(By.XPATH, './/div[contains(@class, "copyable-text")]').text
                        except:
                            msg_text = "Media/Non-text message"

                    extracted_data.append([msg_date.strftime('%Y-%m-%d %H:%M:%S'), sender, msg_text])

            except Exception as e:
                print(f"Error extracting message: {e}")

        file_path = os.path.join(os.getcwd(), f"{self.group_name.replace(' ', '_')}_messages.csv")
        with open(file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Sender", "Message"])
            writer.writerows(extracted_data)

        print(f"Saved {len(extracted_data)} messages from the past 7 days to {file_path}")
