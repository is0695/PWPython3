import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup


vacancy1 = ['Django', 'Flask']
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/58.0.3029.110 ',
}
url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
response = requests.get(url, headers=headers)

vacancy_list = []
vacancy_info = {}
soup = BeautifulSoup(response.text, 'html.parser')
vacancies = soup.find_all(class_="vacancy-serp-item__layout")
for vacancy in vacancies:
    name = vacancy.find("a", class_="serp-item__title").text
    company = vacancy.find("a", class_="bloko-link bloko-link_kind-tertiary").text
    link = vacancy.find("a", class_="serp-item__title")['href']
    salary_span = vacancy.find("span", {"class":"bloko-header-section-2"})
    if salary_span:
        salary_text = salary_span.text.strip()
        salary_span = salary_text.replace("\u202f", "")
    else:
        salary_span = 'Не указана'
    city = vacancy.find("div", {"data-qa": "vacancy-serp__vacancy-address", "class": "bloko-text"}).text
    vacancy_info = {
        'link': link,
        'company': company,
        'city': city,
        'salary': salary_span,
        'name' : name
                }
    vacancy_list.append(vacancy_info)
# pprint(vacancy_list)
with open('vacancies.json', 'w', encoding='utf-8') as file:
    json.dump(vacancy_list, file, ensure_ascii=False, indent=4)
