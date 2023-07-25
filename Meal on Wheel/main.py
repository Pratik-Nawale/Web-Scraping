import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

names = []
addresses = []
contact_numbers = []

zip_code = input("Enter Zip-Code: ")

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome("C:/Users/Pratik/development/chromedriver.exe")
driver.get(f'https://www.mealsonwheelsamerica.org/signup/aboutmealsonwheels/find-programs?filter={zip_code}')

try:

    # CLICKING VIEW ALL MORE RESULTS

    view_more = driver.find_element(By.XPATH, '//div/p/a[contains(@class, "thebutton")]')
    while True:
        try:
            view_more.click()

        except StaleElementReferenceException:
            break

    # FINDING DETAILS

    name = driver.find_elements(By.XPATH, '//div[@class="findmeal-result"]/div/h2')
    address = driver.find_elements(By.XPATH, '//div[@class="findmeal-result"]/div/p')
    contact_number = driver.find_elements(By.XPATH, '//div[@class="findmeal-result"]/div/p/a')

    # APPENDING DETAILS TO THE LISTS

    for i in name:
        names.append(i.text)

    for i in address:
        addresses.append(i.text)

    for i in contact_number:
        contact_numbers.append(i.text)

    # REMOVING CONTACT FROM ADDRESS LIST

    for i in addresses:
        for j in contact_numbers:
            if i == j:
                addresses.remove(i)

    # PRINTING LISTS

    # print(list(names))
    # print(list(addresses))
    # print(list(contact_numbers))

except NoSuchElementException:
    print("No service available at this pin code")

# CONVERTING TO JSON

new_data = []
for i in range(len(names)):
    data = {
        i: {
            "Name": names[i],
            "Address": addresses[i],
            "Contact": contact_numbers[i]
        }
    }
    new_data.append(data)

with open("data.json", "w") as data_file:
    json.dump(new_data, data_file, indent=4)

# CONVERTING TO CSV

data_list = []
for i in range(len(names)):
    data_list.append([names[i], addresses[i], contact_numbers[i]])

df = pd.DataFrame(data_list, columns=["Name", "Address", "Contact"])
df.to_csv("data.csv")


# CLOSING THE BROWSER

driver.quit()
