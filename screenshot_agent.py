from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def capture_gmail_screenshots(to_email, subject, body):
    options = Options()
    options.add_argument("--headless=new")  # Remove for visible browser during testing
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    screenshots_folder = "screenshots"
    os.makedirs(screenshots_folder, exist_ok=True)

    screenshot_paths = []

    try:
        # 1. Open Gmail login page
        driver.get("https://mail.google.com/")
        time.sleep(10)  # Wait for manual login if needed
        login_path = os.path.join(screenshots_folder, "login_page.png")
        driver.save_screenshot(login_path)
        screenshot_paths.append(login_path)

        # 2. Wait until inbox is loaded (up to 60 seconds)
        start_time = time.time()
        while "inbox" not in driver.current_url.lower() and time.time() - start_time < 60:
            time.sleep(2)

        inbox_path = os.path.join(screenshots_folder, "inbox.png")
        driver.save_screenshot(inbox_path)
        screenshot_paths.append(inbox_path)

        # 3. Click Compose button
        compose_button = driver.find_element(By.XPATH, "//div[text()='Compose']")
        compose_button.click()
        time.sleep(3)

        # Fill in the email fields
        to_field = driver.find_element(By.NAME, "to")
        to_field.send_keys(to_email)

        subject_field = driver.find_element(By.NAME, "subjectbox")
        subject_field.send_keys(subject)

        body_field = driver.find_element(By.XPATH, "//div[@aria-label='Message Body']")
        body_field.send_keys(body)

        compose_filled_path = os.path.join(screenshots_folder, "compose_filled.png")
        driver.save_screenshot(compose_filled_path)
        screenshot_paths.append(compose_filled_path)

        # 4. Click Send button
        send_button = driver.find_element(By.XPATH, "//div[text()='Send']")
        send_button.click()
        time.sleep(5)  # Wait for confirmation

        sent_path = os.path.join(screenshots_folder, "sent_confirmation.png")
        driver.save_screenshot(sent_path)
        screenshot_paths.append(sent_path)

    except Exception as e:
        print("Screenshot capture error:", e)

    finally:
        driver.quit()

    return screenshot_paths
