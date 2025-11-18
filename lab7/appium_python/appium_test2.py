from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


APK_PATH = r"C:\Users\USER\AndroidStudioProjects\lab7\app\build\outputs\apk\debug\app-debug.apk"
assert os.path.exists(APK_PATH), f"APK not found: {APK_PATH}"

options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "Android Emulator"
options.app = APK_PATH
options.app_package = "com.example.lab7"
options.app_activity = "com.example.lab7.MainActivity"


APPIUM_SERVER_URL = "http://127.0.0.1:4723"

print("Connecting to Appium:", APPIUM_SERVER_URL)
driver = webdriver.Remote(command_executor=APPIUM_SERVER_URL, options=options)


try:

    WebDriverWait(driver, 15).until(
        lambda d: d.execute_script("mobile: isAppInstalled", {"bundleId": options.app_package}) is not None
    )
except Exception:

    time.sleep(3)

try:
    wait = WebDriverWait(driver, 15)

    print("Waiting for FAB (accessibility id = 'Add')...")
    fab = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//*[@text='+']"))
    )
    print("FAB found, clicking...")
    fab.click()
    print("Clicked FAB — test succeeded.")
    time.sleep(1)

except Exception as e:
    print("ERROR: element not found or other error:", e)

finally:
    driver.quit()
    print("Driver quit.")
