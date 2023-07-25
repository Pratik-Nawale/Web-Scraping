import csv
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

with open("input_medication.csv", encoding="utf-8-sig") as csvfile:
    reader = csv.reader(csvfile)

    count = 0
    medicine = []

    for row in reader:
        count = count + 1
        # print(row[0])
        medicine.append(row[0])

# print(medicine)

age = input("Enter Age:")
select_state = input("Enter State: ")
count_input = input("Enter Number of people living in the household:")
income_input = input("Enter Yearly income:")
residence = input("Residency Status(United States/Non-U.S. Citizen):")

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://medicineassistancetool.org/")

for i in medicine:
    medication = driver.find_element(By.XPATH, "//input[@placeholder='Search by Medication']")
    medication.send_keys(i)

    try:
        wait = WebDriverWait(driver, 8)
        wait.until(EC.presence_of_element_located((By.XPATH, "//ul/li/button[normalize-space()='Add to list']")))

        add_to_list = driver.find_elements(By.XPATH, "//ul/li/button[normalize-space()='Add to list']")
        for add in add_to_list:
            add.click()

        medication.clear()

    except TimeoutException:
        medication.clear()
        continue


# CLICKING THE NEXT BUTTON

driver.find_element(By.XPATH, "//div/button[normalize-space()='Next']").click()

household_count = driver.find_element(By.XPATH, "//input[@placeholder='Age']")
household_count.send_keys(f"{age}")


state = driver.find_element(By.XPATH, f"//li[normalize-space()='{select_state}']")
driver.execute_script("arguments[0].click();", state)

household_count = driver.find_element(By.XPATH, "//input[@placeholder='Number of people living in the household']")
household_count.send_keys(f"{count_input}")

income = driver.find_element(By.XPATH, "//input[@placeholder='Yearly household income']")
income.send_keys(f"{income_input}")

residency = driver.find_element(By.XPATH, "//button[normalize-space()='Residency status']")
residency.click()
select_residency = driver.find_element(By.XPATH, f"//li[normalize-space()='{residence}']")
ActionChains(driver).move_to_element(select_residency).click(select_residency).perform()

insured = driver.find_element(By.XPATH, f"//input[@id='insured-{'no'}']")
insured.click()

disaster = driver.find_element(By.XPATH, f"//input[@id='recent-disaster-{'no'}']")
disaster.click()

show_result = driver.find_element(By.XPATH, "//button[@value='Submit']")
show_result.click()

title = []
link = []
number = []
assistance_type = []

wait2 = WebDriverWait(driver, 30)
wait2.until(EC.presence_of_element_located((By.XPATH, "//h4[@class='medication-search-results__search-results-card-title']")))

try:

    card_title = driver.find_elements(By.XPATH, "//h4[@class='medication-search-results__search-results-card-title']")
    website = driver.find_elements(By.XPATH, "//a[normalize-space()='Visit Website']")
    contact = driver.find_elements(By.XPATH, "//div[@class='medication-search-results__search-results-card-contact-links']//a[2]")
    assistance = driver.find_elements(By.XPATH, '//div/div[@class="medication-search-results__search-results-card-body"]')

    for i in card_title:
        title.append(i.text)

    for i in website:
        link.append(i.get_attribute("href"))

    for i in contact:
        number.append(i.text)

    for i in assistance:
        assistance_type.append(i.text.replace("Assistance Type: ", ""))


except NoSuchElementException:
    print("No results were found for given information")


# print(card_title.text)
# print(website.text)
# print(contact.text)

# print(title)
# print(link)
# print(number)


# CONVERTING TO JSON

new_data = []
for i in range(len(title)):
    data = {
        i: {
            "Name": title[i],
            "Link": link[i],
            "Contact": number[i],
            "Assistance Type": assistance_type[i]
        }
    }
    new_data.append(data)

with open("data.json", "w") as data_file:
    json.dump(new_data, data_file, indent=4)

# CONVERTING TO CSV

data_list = []
for i in range(len(title)):
    data_list.append([title[i], link[i], number[i], assistance_type[i]])

df = pd.DataFrame(data_list, columns=["Name", "Link", "Contact", "Assistance Type"])
df.to_csv("data.csv")


# CLOSING THE BROWSER

# driver.quit()

