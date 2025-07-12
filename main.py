import requests
from datetime import datetime, timedelta
import pytz
import bs4
import psycopg2
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

category_keywords = {
 "Аналитика": {
    "keywords": [
      "аналитик", 'systems_analyst', 'data_analyst', 'business_analyst', 'bi-аналитик', 'бизнес-аналитик', 'marketing_analyst', 
      'bi_developer', 'bi-аналитик, аналитик данных', 'systems_analyst'
    ],
    "subcategories": {
      "Системный аналитик": [
        "системн", "systems_analyst",  "uml"
      ],
      "Бизнес аналитик": [
        "бизнес", "business", 'бизнес-аналитик', 'business_analyst'
      ],
      "Data аналитик & BI": [
        'data_analyst', 'bi-аналитик', "bi_developer", 'bi-аналитик, аналитик данных'
      ],
      "Продуктовый аналитик": [
        "продуктов", "product", "a/b", "ab test", "a/b test", 'продуктовый аналитик'
      ],
      "Аналитик DWH": [
        "data engineer", "dwh", "data warehouse", "airflow", "data lake",
        "databricks", "spark", "hadoop", 'sql'
      ],
      "Веб-аналитик": [
        "веб", "web",
      ],
      "Аналитик (другое)": []
  }
},
 "Тестирование": {
    "keywords": [
      "тестировщик", "tester", "qa", "quality assurance", "тестировщик-автоматизатор",
      "qa engineer", "инженер по тестирован", "ручн тестирован", "автоматизирован тестирован",
      "мобильн тестирован", "веб тестирован", "гейм тестирован", "api тестирован",
      "безопасност тестирован", "производительност тестирован", "нагрузочн тестирован",
      "интеграцион тестирован", "регрессион тестирован", "smoke тестирован", "приемочн тестирован",
      "quality manager", "qa lead", "qa architect", 'manual_testing', 'test_automation', 'qa_engineer'
    ],
    "subcategories": {
      "Ручное тестирование": [
        "ручн тестировщик", 'ручное', 'ручного', 'manual_testing'
      ],
      "Автоматизированное тестирование": [
        "автоматизатор тестирован", "automation tester", "qa automation", "test_automation"
      ],
     "Тестирование (Другое)": []
    }
},
 "Разработка": {
    "keywords": [
      "frontend", "front-end", "front end", "javascript", "js",
      "react", "angular", "vue", "typescript", 'software',
      "backend", 'devops', 'mobileapp_developer', "data_engineer", 'database_developer', 
      "fullstack", "full-stack", "full stack", "DevOps-инженер"
    ],
    "subcategories": {
      "Frontend разработка": [
        "frontend", "front-end", "front end", "javascript", "js",
        "react", "angular", "vue", "typescript", "ui developer"
      ],
      "Backend разработка": [
        "backend", "back-end", "back end", "server", "api",
        "python", "java", "php", "node", "nodejs", "net", "ruby", "go", "golang"
      ],
      "Fullstack разработка": [
        "fullstack", "full-stack", "full stack", 
      ],
      "Мобильная разработка": [
        "mobile", "android", "ios", "flutter", "react",
        "котлин", "kotlin", "swift", "mobileapp_developer"
      ],
      "DevOps": [
        "devops", "DevOps-инженер"
      ], 
      "Data engineer": [
        "data_engineer", 'database_developer'
      ],
  "Разработка (Другое)": []
    }
},
 "ML/AI/DS": {
    "keywords": [ 
      "ml engineer", "ml-engineer", "mlops", 'data_scientist', 'ml', 'ai', 'промт', 'дата-сайентист'
    ],
    "subcategories": {
      "Data Science": [
        "data science", "анализ данн", "дата-сайентист", "data_scientist", 'дата-сайентист'
      ],
      "ML Engineering & Mlops": [
        "ml engineer", "ml-engineer", "mlops", "model serving"
      ],
       "AI (Другое)": []
    }
},
 "Менеджмент": {
    "keywords": [
      'менеджер продукта', 'руководитель группы разработки', 'руководитель отдела аналитики', "руководитель проектов", 'project_manager',
      'project_director', 'product_manager', 'marketing_manager', 'account_manager'
    ],

    "subcategories": {
      "Продуктовый менеджмент": [
        "продуктов менеджер", "product manager", "PM", "product owner",
        "руководитель продукт", "head of product", 'product_manager'
      ],
      "Проектный менеджмент": [
        "проектн менеджер", "project manager", "PM", "руководитель проектов", 'project_manager', 'scrum_master', 'account_manager'
      ],
      "ИТ топ менеджмент": [
        'руководитель группы разработки',  'руководитель отдела аналитики', 'технический директор (сто)',  'project_director'
      ],

"Менеджер (Другое)": []
 }
    }
}

category_keywords_work = {
    
    "Аналитика": {
        "keywords": ["аналитик", "бизнес аналитик" "analyst", "аналитик данных", "data analyst", "бизнес-аналитик", "business analyst", "BI-аналитик", "BI analyst", "системный аналитик", "system analyst", "веб-аналитик", "web analyst"],
        "subcategories": {
            "Системный аналитик": ["системный", "system analyst"],
            "Бизнес-аналитик": ["бизнес-аналитик", "business analyst", "аналитик процессов", "process analyst", "bpm-аналитик", "бизнес"],
            "Data аналитик & BI": ["аналитик данных", "data", "данных", "bi", "аналитик отчетности", "data analytics specialist"],
            "Продуктовый аналитик": ["продуктовый аналитик", "product analyst", "продуктовый"],
            "Веб-аналитик": ["веб-аналитик", "web analyst", "google analytics analyst", "аналитик метрик", "аналитик трафика"],
            "Аналитик DWH": ["data engineer", "dwh", "data warehouse", "airflow", "data lake", "databricks", "spark", "hadoop", 'sql'],
            "Другое": ["risk analyst", "аналитик безопасности", "hr analyst", "операционный аналитик", "аналитик поддержки"]
}
    },
    "Разработка": {
        "keywords": ["разработчик", "developer", "программист", "engineer", "dev", "software", "приложений", "application", "код", "code"],
        "subcategories": {
            "Frontend разработка": ["frontend", "front-end", "front end", "javascript", "js", "react", "angular", "vue", "typescript", "ui developer"],
            "Backend разработка": ["backend", "back-end", "back end", "server", "api", "python", "java", "php", "node", "nodejs", ".net", "ruby", "go", "golang"],
            "Fullstack разработка": ["fullstack", "full-stack", "full stack", "универсальный разработчик","full", "mean", "lamp"],
            "Разработка (Другое)": ["lead developer", "architect", "cto", "техлид", "research", "r&d", "стажер", "intern"]
}
},
     "Тестирование": {
        "keywords": ["тестировщик", "tester", "qa", "quality assurance", "manual_testing", "тест", "test", "qa engineer", "инженер по тестированию"],
        "subcategories": {
            "Ручное тестирование": ["ручной тестировщик", "manual tester", "qa manual", "тестировщик ручного тестирования", "manual qa engineer", 'manual_testing'],
            "Автоматизированное тестирование": ['test_automation', "автоматизатор тестирования", "automation tester", "qa automation", "инженер по автоматизации тестирования", "automation qa engineer"],
            "Тестирование (Другое)": ["lead qa", "старший тестировщик", "главный тестировщик", "менеджер по качеству", "quality manager"]
}
}
}



# Парсим с hh и хабра и грузим в базу данных

import requests
from datetime import datetime, timedelta
import pytz
from bs4 import BeautifulSoup
import json
import re



def hh_parsing():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    date_from = yesterday.strftime("%Y-%m-%dT00:00:00")
    date_to = today.strftime("%Y-%m-%dT23:59:59")

    # Разбиваем роли на 3 логические группы для балансировки нагрузки
    role_groups = [
        ['156', '148', '160', '10',  '150', '165'],  # IT и управление
        ['36', '73', '96', '164', '104', '157' ],  # Маркетинг и продажи
        [  '107', '124', '125'] #,  # Другие специалисты
        # ['12', '25', '34', '155', '112','113', '114', '116', '121', '126']
    ]

    all_vacancies = []
    
    for group in role_groups:
        page = 0
        while True:
            params = {
                'professional_role': group,
                'date_from': date_from,
                'date_to': date_to,
                'per_page': 25,
                'page': page
            }
            
            try:
                response = requests.get("https://api.hh.ru/vacancies", params=params)
                response.raise_for_status()
                data = response.json()
                
                if not data['items']:
                    break
                    
                for item in data['items']:
                    vacancy = {
                        "title": item['name'],
                        "company": item['employer']['name'],
                        "date": item['published_at'],
                        "location": item['area']['name'],
                        "employment": item['employment']['name'],
                        "experience": item['experience']['name'],
                        "salary": item.get('salary'),
                        "skills": item['snippet']['requirement'],
                        "link": item['alternate_url'],
                        'source': 'hh',
                        'vacancy_type': item['professional_roles'][0]['name'],
                        'new_category': classify_vacancy(item['professional_roles'][0]['name'], item['name'])
                    }
                    all_vacancies.append(vacancy)
                
                # print(f"Группа {group[:3]}..., Страница {page}: {len(data['items'])} вакансий")
                page += 1
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Ошибка: {str(e)}")
                break
    
    return all_vacancies


def safe_find_text(element, selector, **kwargs):
    found = element.find(selector, **kwargs) if element else None
    return found.text.strip() if found else None

def classify_vacancy(title, vacancy_type,  description=""):
    """Классифицирует вакансию по названию и описанию"""
    text = f"{title} {description}".lower()
    vacancy_type = f"{vacancy_type} {title}".lower()
    if text == 'аналитик' or  text == 'программист, разработчик' or text == 'тестировщик':
      print('зашли')
      for category, data in category_keywords_work.items():
        if any(re.search(rf'{re.escape(keyword)}', vacancy_type) for keyword in data["keywords"]):
            # Затем проверяем подкатегории
            for subcategory, sub_keywords in data["subcategories"].items():
                if not sub_keywords:  # Если нет ключевых слов - это "Другое"
                    continue
                if any(re.search(rf'\b{re.escape(sub_kw)}\b', vacancy_type) for sub_kw in sub_keywords):
                    return f"{category} | {subcategory}"
            # Если подкатегория не найдена, возвращаем основную категорию + "Другое"
            return f"{category} | {category.split()[0]} (Другое)"
    else:
      # Сначала проверяем категории
      for category, data in category_keywords.items():
          if any(re.search(rf'{re.escape(keyword)}', text) for keyword in data["keywords"]):
              # Затем проверяем подкатегории
              for subcategory, sub_keywords in data["subcategories"].items():
                  if not sub_keywords:  # Если нет ключевых слов - это "Другое"
                      continue
                  if any(re.search(rf'\b{re.escape(sub_kw)}\b', text) for sub_kw in sub_keywords):
                      return f"{category} | {subcategory}"
              # Если подкатегория не найдена, возвращаем основную категорию + "Другое"
              return f"{category} | {category.split()[0]} (Другое)"

    return "Другое | Не определено"



def get_vacancy_categories(element):
    """Извлекает категории вакансий из ссылок /vacancies/spec/"""
    categories = []
    if element:
        spec_links = element.find_all('a', href=lambda x: x and '/vacancies/spec/' in x)
        for link in spec_links:
            # Извлекаем последнюю часть пути как название категории
            category = link['href'].split('/')[-1]
            categories.append(category)
    return ', '.join(categories) if categories else ''



def get_vacancy_level(element):
    """Извлекает уровень вакансии из текста рядом с /vacancies?qid"""
    if element:
        level_link = element.find('a', href=lambda x: x and '/vacancies?qid=' in x)
        if level_link:
            return level_link.text.strip()
    return None



def habr_parsing():
    a_list = []
    num_list = 25

    for j in range(num_list):
        j+=1
        data = requests.get(f'https://career.habr.com/vacancies?page={j}&type=all')
        soup = BeautifulSoup(data.content, 'html.parser')
        vacancy = soup.find_all('div', class_='vacancy-card')
        for i in vacancy:
            time_vac = safe_find_text(i, 'time', class_='basic-date')
            time_vac = parse_russian_date(time_vac)
            if datetime.now() - time_vac < timedelta(days=1):
                experience = get_vacancy_level(i)
                if experience is None:
                    experience = 'Не указано'
                elif (experience == 'Старший (Senior)') or (experience == 'Ведущий (Lead)') :
                    experience = "От 3 до 6 лет"
                elif experience == 'Стажёр (Intern)':
                    experience = "Нет опыта"
                elif (experience == 'Средний (Middle)') or (experience == 'Младший (Junior)'):
                    experience = "От 1 года до 3 лет"
                
                vacancy_list = {
                "title": safe_find_text(i, 'a', class_='vacancy-card__title-link'),
                "company": safe_find_text(i, 'a', class_='link-comp', href=lambda x: x and '/companies/' in x),
                "date": datetime.now(),
                "location": safe_find_text(i, 'a', href=lambda x: x and 'city_id=' in x),
                'source' : 'habr',
                "employment": safe_find_text(i, 'span', class_='preserve-line', string=lambda x: x and 'Полный рабочий день' in x),
                "salary": safe_find_text(i, 'div', class_='basic-salary'),
                "skills": ', '.join([skill.text for skill in i.find_all('a', class_='link-comp', href=lambda x: x and '/skills/' in x)]) if i.find_all('a', class_='link-comp', href=lambda x: x and '/skills/' in x) else '',
                "link": "https://career.habr.com" + i.find('a', class_='vacancy-card__title-link')['href'] 
                    if i.find('a', class_='vacancy-card__title-link') else None,
                "new_category" : classify_vacancy(get_vacancy_categories(i), safe_find_text(i, 'a', class_='vacancy-card__title-link')),
                "vacancy_type": get_vacancy_categories(i),  # Добавленные категории из /vacancies/spec/
                "experience": experience
                }

                a_list.append(vacancy_list)
            else:
                break
        time.sleep(1)
    return a_list


def parse_date(date_str):
    """Парсит дату из строки в формате '2025-06-25T13:02:24+0300'"""
    try:
    # Удаляем временную зону (+0300) для упрощения (можно сохранить отдельно если нужно)
        if isinstance(date_str, str) and 'T' in date_str:
            return datetime.strptime(date_str.split('+')[0], '%Y-%m-%dT%H:%M:%S')
        return date_str
    except Exception as e:
        print(f"Ошибка парсинга даты {date_str}: {e}")
    return None # или datetime.now() для подстановки текущей даты

def parse_russian_date(date_str):
    month_map = {
        'января': 1, 'февраля': 2, 'марта': 3,
        'апреля': 4, 'мая': 5, 'июня': 6,
        'июля': 7, 'августа': 8, 'сентября': 9,
        'октября': 10, 'ноября': 11, 'декабря': 12
    }
    
    # Извлекаем день и месяц
    match = re.match(r'(\d{1,2})\s+([а-я]+)', date_str.lower())
    if not match:
        return None
    
    day = int(match.group(1))
    month_ru = match.group(2)
    month = month_map.get(month_ru)
    
    if not month:
        return None
    
    # Берем текущий год (можно задать явно если нужно)
    year = datetime.now().year
    
    return datetime(year=year, month=month, day=day)

def loading_to_base(hh_list, habr_list):
    conn = psycopg2.connect(
        host="pg4.sweb.ru",
        port=5433,
        database="maksimarkh",
        user="maksimarkh",
        password="Maksim1232145!"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT distinct link FROM vacans")
    link_records = cursor.fetchall()
    link_list = [record[0] for record in link_records if record[0] is not None]

    cursor.execute("SELECT distinct link FROM vacans where date > CURRENT_DATE")
    link_records = cursor.fetchall()
    link_list_now = [record[0] for record in link_records if record[0] is not None]

    

    for i in habr_list:
        if i['link'] not in link_list_now:
            
            cursor.execute("""
                INSERT INTO vacans (title, company, date, employment, salary, skills, link, location, source, new_category, vacancy_type, experience) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,  %s,  %s, %s, %s)
            """, (
                i['title'], 
                i['company'], 
                i['date'], 
                i['employment'], 
                i['salary'], 
                i['skills'], 
                i['link'],
                i['location'],
                i['source'],
                i['new_category'],
                i['vacancy_type'],
                i['experience']
                
            ))

    for i in hh_list:
        if i['link'] not in link_list:
            date_value = parse_date(i['date'])

            cursor.execute("""
            INSERT INTO vacans (title, company, date, employment, salary, skills, link, location, source, vacancy_type, experience, new_category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
            i['title'],
            i['company'],
            date_value,
            i['employment'],
            str(i['salary']),
            i['skills'],
            i['link'],
            i['location'],
            i['source'],
            i['vacancy_type'],
            i['experience'],
            i['new_category']

            ))
    conn.commit()
    cursor.close()
    conn.close()


def main():
    try:
        logger.info("Запуск парсера...")
        hh_list = hh_parsing()
        logger.info("HH загрузило...")
        habr_list = habr_parsing()
        logger.info("Habr загрузило...")
        
        
        if hh_list or habr_list:
            logger.info("Начало загрузки в базу данных")
            loading_to_base(hh_list, habr_list)
            
    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)

if __name__ == "__main__":
    main()
