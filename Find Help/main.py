import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


d = DesiredCapabilities.CHROME

d['proxy'] = {
    "httpProxy": "http://38.132.126.214:8080",
    "sslProxy": "http://38.132.126.214:8080"
}

# Create a new Chrome browser instance with the desired capabilities
driver = webdriver.Chrome(desired_capabilities=d)
driver.get("https://www.findhelp.org/search_results/30324")

#
# # Now you can use the driver as you normally would to navigate to websites through the VPN proxy






# proxy_ip_port = '3.99.167.1'
#
# proxy = Proxy()
# proxy.proxy_type = ProxyType.MANUAL
# proxy.http_proxy = proxy_ip_port
# proxy.ssl_proxy = proxy_ip_port
# capabilities = webdriver.DesiredCapabilities.CHROME
# proxy.add_to_capabilities(capabilities)
#
#
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)

# driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
# driver.get("https://whatismyipaddress.com/")
# driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("https://www.findhelp.org/search_results/30324")

# button = driver.find_element(By.XPATH, "//a[@class='loading-on-click tlc-name']//span[@data-translate='Help Pay For Healthcare'][normalize-space()='Help Pay For Healthcare']")
# button.click()