import random
import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

config = {
    "platformName": "Android",
    "platformVersion": "7.1.1",
    "deviceName": "192.168.100.111:4444",
    "appPackage": "com.jifen.qukan",
    "appActivity": "com.jifen.qkbase.main.MainActivity",
    "noReset": True,
    "unicodekeyboard": True,
    "resetkeyboard": True,
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', config)

