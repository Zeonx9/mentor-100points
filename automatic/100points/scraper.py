from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def log_to_site(mail, password):
    driver = webdriver.Chrome()
    driver.get('https://api.100points.ru/login')
    driver.implicitly_wait(30)

    # login to the api.100points
    driver.find_element(By.ID, 'email').send_keys(mail)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.TAG_NAME, 'button').click()

    # open the list of all accepted homeworks
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Одобрено').click()
    return driver


def get_data_from_cur_page(driver, write_to):
    # find the rows in the table bellow
    table = WebDriverWait(driver, 10).until(
        ec.presence_of_all_elements_located((By.XPATH, '//table//tr[@class="odd"]'))
    )
    row_count = len(table)

    for i in range(1, row_count + 1):
        # go to view page
        driver.find_element(By.XPATH, f'//table//tr[{i}]/td/a').click()
        # select a mark of student
        element_mark = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//div[@class="card-body"]/div/div[6]/div'))
        )
        mark = element_mark.text.split()[-1].split("/")[0]
        # return to the previous page
        driver.back()

        # extract data
        element_name = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, f'//table//tr[{i}]/td[3]/div[1]'))
        )
        name = element_name.text
        task = driver.find_element(By.XPATH, f'//table//tr[{i}]/td[4]/div[1]/small/b').text.split(".")[0]
        level = driver.find_element(By.XPATH, f'//table//tr[{i}]/td[4]/div[4]/small/b').text.split()[0]
        # save the data
        write_to.append(','.join([name, task + ' ' + level, mark]) + '\n')

    # # print retrieved data
    # print(*write_to[-row_count:], sep='', end='')


def go_to_next_page(driver):
    button = driver.find_element(By.PARTIAL_LINK_TEXT, 'Next')
    if button.get_attribute('disabled'):
        return False
    button.click()
    return True


to_do = input("Enter 'create' to generate data, or 'update' to append new data: ")
dr = log_to_site("tema_mushtukov@100points.ru", "mushtukov.artyom")
if to_do == 'create':
    extracted_data = []
    while True:
        get_data_from_cur_page(dr, extracted_data)
        if not go_to_next_page(dr):
            break

    with open("data.csv", "w", encoding="UTF-8") as file:
        file.writelines(extracted_data)

elif to_do == 'update':
    with open("data.csv", "r", encoding="UTF-8") as file:
        prev_data = file.readlines()

    new_lines = []
    while True:
        page_data = []
        get_data_from_cur_page(dr, page_data)
        count = len(new_lines) + len(page_data)
        new_lines += [s for s in page_data if s not in prev_data]
        print(count, len(new_lines))

        if count - len(new_lines) > 4:
            break
        go_to_next_page(dr)

    prev_data = new_lines + prev_data
    with open("data.csv", "w", encoding="UTF-8") as file:
        file.writelines(prev_data)

dr.close()
