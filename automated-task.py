import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('selenium_script.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
logger.info("Chrome options initialized.")

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
logger.info("WebDriver initialized.")

def wait_for_element(by, value, timeout=10):
    logger.debug(f"Waiting for element by {by} with value '{value}' for up to {timeout} seconds.")
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        logger.debug(f"Element found: {element}")
        return element
    except Exception as e:
        logger.error(f"Timeout: Element with {by}='{value}' not found after {timeout} seconds.")
        raise e

def switch_to_frame(frame_element):
    logger.debug(f"Switching to frame: {frame_element}")
    driver.switch_to.frame(frame_element)

def switch_to_default_content():
    logger.debug("Switching back to default content.")
    driver.switch_to.default_content()

try:
    logger.info("Opening the login page.")
    driver.get("set_me")

    username_field = wait_for_element(By.ID, "mainCPHolder_login1_username")
    username_field.send_keys("set_me")

    password_field = wait_for_element(By.ID, "mainCPHolder_login1_password")
    password_field.send_keys("set_me")

    login_button = wait_for_element(By.ID, "mainCPHolder_login1_btnLogin")
    login_button.click()

    training_page_button = wait_for_element(By.ID, "mainCPHolder_relPersonHome_btnTraineeTraining")
    training_page_button.click()

    eLearning_button = wait_for_element(By.CSS_SELECTOR, "a[title='Μετάβαση σε τηλεκατάρτιση']")
    eLearning_button.click()

    my_courses_link = wait_for_element(By.LINK_TEXT, "Τα μαθήματά μου")
    my_courses_link.click()

    course_image = wait_for_element(By.CSS_SELECTOR, "div.card-img.dashboard-card-img") #edw epilegw thn eikona.
    course_image.click()

    scorm_link = wait_for_element(By.CSS_SELECTOR, "a[href*='mod/scorm/view.php?id=328']")
    scorm_link.click()

    login_button = wait_for_element(By.ID, "n")
    login_button.click()

    original_window = driver.current_window_handle
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
   
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

    logger.info("Switching to the iframe within the popup window.")
    iframe_element = wait_for_element(By.XPATH, "//iframe[@id='scorm_object']")
    switch_to_frame(iframe_element)

    logger.info("Checking if switched to iframe successfully.")
    logger.debug(driver.page_source)

    start_time = time.time()
    duration = 4 * 60 * 60  # 4 hours the program will run

    while (time.time() - start_time) < duration:
        try:
            current_url = driver.current_url
            logger.info(f"Current URL before clicking 'ΕΠΟΜΕΝΗ': {current_url}")
           
            logger.info("Waiting for 'ΕΠΟΜΕΝΗ' button inside the iframe.")
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'uikit-primary-button_next')]"))
            )
            logger.info("Clicking 'ΕΠΟΜΕΝΗ' button.")
            next_button.click()
           
            logger.info("Waiting for 35 seconds before next click.")
            time.sleep(35)  # Wait for 35 seconds
        except Exception as e:
            logger.error(f"Failed to click 'ΕΠΟΜΕΝΗ': {e}")
            break
   
    switch_to_default_content()
    driver.close()
    driver.switch_to.window(original_window)

except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
finally:
    logger.info("Closing the browser.")
    driver.quit()
