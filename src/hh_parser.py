import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from src.db import connect

search_tags = 'Python Django'
url = 'https://hh.ru/'
vacancy_fields = ['job_type', 'company_name',
                  'pub_date', 'vacancy_description',
                  'work_hours', 'address', 'key_skills',
                  ['salary', 'town', 'experience'],
                  ]
xpaths = [
    '//span[@itemprop="employmentType"]',
    '//a[@itemprop]',
    '//time[@itemprop]',
    '//div[@itemprop="description"]',
    '//span[@itemprop="workHours"]',
    "//div[@data-qa='vacancy-address-with-map']",
    ("//span[@class='Bloko-TagList-Text']",),
    ("//td[contains(@class,'b-v-info-content')]",),
]

driver = webdriver.Chrome()


def start(uri):
    print('Worker is running')
    driver.get(uri)
    path = '//input[@data-qa="vacancy-serp__query"]'
    search_box = driver.find_element_by_xpath(path)
    search_box.send_keys(search_tags)
    search_box.send_keys(Keys.RETURN)


def collect_links():
    print('Collecting links')
    path = "//a[@data-qa='vacancy-serp__vacancy-title']"
    vacancies = driver.find_elements_by_xpath(path)
    return vacancies


def visit_all_links(links):
    queryset = list()
    for link in links:
        print('Collecting link ' + link.text)
        link.send_keys(Keys.CONTROL, Keys.RETURN)
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[1])
        data = collect_information()
        queryset.append(data)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print('Success')
    return queryset


def collect_information():
    result = {}
    print('Getting data from page')
    for i in range(len(vacancy_fields)):
        try:
            if type(xpaths[i]) == tuple and type(vacancy_fields[i]) == list:
                data = driver.find_elements_by_xpath(xpaths[i][0])
                result.update(unpack_data(data, vacancy_fields[i]))
                continue
            if type(xpaths[i]) == tuple and type(vacancy_fields[i]) != list:
                data = driver.find_elements_by_xpath(xpaths[i][0])
                result[vacancy_fields[i]] = ', '.join([x.text for x in data])
                continue
            data = driver.find_element_by_xpath(xpaths[i]).text
            result[vacancy_fields[i]] = data
        except NoSuchElementException:
            pass
    result['url'] = driver.current_url
    print('Collecting data finished')
    return result


def unpack_data(parsed_data, fields):
    result = dict()
    for x in range(len(fields)):
        result[fields[x]] = parsed_data[x].text
    return result


def put_in_db(data):
    print('Putting to db proccess')
    meta, connection = connect()
    connection.execute(meta.tables['vacancies'].insert(), data)


def interrupt():
    print('Job done')
    driver.quit()


def main():
    start(url)
    links = collect_links()
    data = visit_all_links(links)
    put_in_db(data)
    driver.quit()
main()
