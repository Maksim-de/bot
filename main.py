import requests
from datetime import datetime, timedelta
import pytz
import bs4
import psycopg2
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

category_keywords = {
    
    "Аналитика": {
        "keywords": ["аналитик", "бизнес аналитик" "analyst", "аналитик данных", "data analyst", "бизнес-аналитик", "business analyst", "BI-аналитик", "BI analyst", "системный аналитик", "system analyst", "веб-аналитик", "web analyst"],
        "subcategories": {
            "Системный аналитик": ["системный аналитик", "system analyst", "аналитик требований", "business system analyst", "технический аналитик", "it analyst"],
            "Бизнес-аналитик": ["бизнес-аналитик", "business analyst", "аналитик процессов", "process analyst", "bpm-аналитик", "ba"],
            "Аналитик данных": ["аналитик данных", "data analyst", "аналитик sql", "bi analyst", "аналитик отчетности", "data analytics specialist"],
            "Продуктовый аналитик": ["продуктовый аналитик", "product analyst", "data product analyst", "аналитик продукта", "growth analyst"],
            "Финансовый аналитик": ["финансовый аналитик", "financial analyst", "инвестиционный аналитик", "fp&a analyst", "аналитик бюджетирования"],
            "Маркетинг-аналитик": ["маркетинг-аналитик", "marketing analyst", "crm-аналитик", "digital analyst", "аналитик рекламы", "media analyst"],
            "Веб-аналитик": ["веб-аналитик", "web analyst", "google analytics analyst", "аналитик метрик", "аналитик трафика"],
            "Другое": ["risk analyst", "аналитик безопасности", "hr analyst", "операционный аналитик", "аналитик поддержки"]
}
},
   "Тестирование": {
        "keywords": ["тестировщик", "tester", "qa", "quality assurance", "контроль качества", "тест", "test", "qa engineer", "инженер по тестированию"],
        "subcategories": {
            "Ручное тестирование": ["ручной тестировщик", "manual tester", "qa manual", "тестировщик ручного тестирования", "manual qa engineer"],
            "Автоматизированное тестирование": ["автоматизатор тестирования", "automation tester", "qa automation", "инженер по автоматизации тестирования", "automation qa engineer"],
            "Тестирование мобильных приложений": ["мобильный тестировщик", "mobile tester", "qa mobile", "тестировщик мобильных приложений", "mobile qa engineer"],
            "Тестирование веб-приложений": ["веб-тестировщик", "web tester", "qa web", "тестировщик веб-приложений", "web qa engineer"],
            "Тестирование игр": ["гейм тестировщик", "game tester", "qa game", "тестировщик игр", "game qa engineer"],
            "Тестирование API": ["api тестировщик", "api tester", "qa api", "тестировщик api", "api qa engineer"],
            "Тестирование безопасности": ["тестировщик безопасности", "security tester", "qa security", "пентестер", "security qa engineer"],
            "Тестирование производительности": ["тестировщик производительности", "performance tester", "qa performance", "load tester", "performance qa engineer"],
            "Тестирование (Другое)": ["lead qa", "старший тестировщик", "главный тестировщик", "менеджер по качеству", "quality manager"]
}
},
    
    "Разработка": {
        "keywords": ["разработчик", "developer", "программист", "engineer", "dev", "software", "приложений", "application", "код", "code"],
        "subcategories": {
            "Frontend разработка": ["frontend", "front-end", "front end", "javascript", "js", "react", "angular", "vue", "typescript", "ui developer"],
            "Backend разработка": ["backend", "back-end", "back end", "server", "api", "python", "java", "php", "node", "nodejs", ".net", "ruby", "go", "golang"],
            "Fullstack разработка": ["fullstack", "full-stack", "full stack", "универсальный разработчик","mern", "mean", "lamp"],
            "Мобильная разработка": ["mobile", "android", "ios", "flutter", "react native", "котлин", "kotlin", "swift", "xamarin"],
            "GameDev": ["game", "игр", "unity", "unreal", "геймдев", "cryengine", "gamedeveloper", "game programmer"],
            "DevOps": ["devops", "sre", "site reliability", "инфраструктура", "docker", "kubernetes", "k8s", "terraform", "ansible"],
            "Embedded/IoT": ["embedded", "встроенные", "iot", "arduino", "raspberry", "микроконтроллеры", "firmware", "драйверы"],
            "Блокчейн": ["blockchain", "смарт-контракты", "solidity", "web3", "defi", "crypto", "крипто"],
            "Разработка (Другое)": ["lead developer", "architect", "cto", "техлид", "research", "r&d", "стажер", "intern"]
}
    },
    "AI (ИИ)": {
        "keywords": ["nlp", "искусственный интеллект","computer vision", "cv", "ии", "ai", "artificial intelligence", "машинное обучение", "ml", "machine learning", "нейросети","deep learning", "data science"],
        "subcategories": {
            "Computer Vision": ["computer vision", "cv", "обработка изображений", "image processing","распознавание образов", "object detection", "openCV", "segmentation"],
            "Natural Language Processing": [ "nlp", "natural language processing", "обработка текста", "text processing", "chatbot", "чат-бот", "transformer", "LLM","large language model" ],
            "Data Science": ["data science", "ds", "data analysis", "feature engineering", "pandas", "numpy", "scikit-learn"],
            "Deep Learning": ["deep learning", "глубокое обучение", "нейронные сети", "neural networks", "tensorflow", "pytorch", "keras"],
            "ML Engineering": [ "ml engineer", "machine learning engineer", "инженер мл", "mlops", "deployment", "развертывание моделей", "model serving"],
            "AI Research": ["ai researcher", "research scientist", "научный сотрудник", "публикации","publications", "sota", "state of the art"],
            "ИИ (Другое)": ["ai стажер", "этика ии", "ai ethics", "ai intern", "ответственный ии", "ai консультант", "ai consultant","ai архитектор", "ai architect"
]
}
    },
    "Администрирование": {
        "keywords": ["администратор", "administrator", "админ", "admin", "сетевой", "network","баз данных", "database", "сервер", "server","поддержка", "support", "техподдержка", "helpdesk"],
        "subcategories": {
            "Системный администратор": ["системный администратор", "system administrator", "sysadmin", "linux администратор","windows администратор", "unix администратор", "админ серверов", "server administrator"],
            "Сетевой администратор": ["сетевой администратор", "network administrator", "админ сетей", "cisco администратор","junos администратор", "firewall администратор", "vpn администратор"],
"Администратор баз данных": [
"администратор баз данных", "dba", "database administrator", "mysql администратор",
"postgresql администратор", "oracle dba", "mssql администратор", "mongodb администратор"
],
"DevOps/Администрирование": [
"devops администратор", "sre", "site reliability engineer", "cloud администратор",
"aws администратор", "azure администратор", "gcp администратор", "kubernetes администратор"
],
"Администратор 1С": [
"администратор 1с", "1с администратор", "1с специалист", "1с поддержка",
"1с настройка", "1с конфигурация", "1с разработка"
],
"Виртуализация и облака": [
"администратор виртуализации", "vmware администратор", "hyper-v администратор", "kvm администратор",
"openstack администратор", "docker администратор", "kubernetes администратор"
],
"Безопасность": [
"администратор безопасности", "security administrator", "siem администратор", "soc администратор",
"кибербезопасность", "cybersecurity", "pentest администратор"
],
"Техническая поддержка": [
"администратор поддержки", "helpdesk администратор", "it support", "техподдержка",
"service desk", "офисный администратор"
],
"Администрирование (Другое)": [
"старший администратор", "lead administrator", "главный администратор", "стажер администратор", "junior administrator"
]
}
},
   "Информационная безопасность": {
"keywords": [
"безопасность", "security", "кибербезопасность", "cybersecurity",
"защита", "protection", "аудит", "audit",
"сетевой", "network", "pentest", "тестирование на проникновение",
"compliance", "соответствие", "политики", "policies"
],
"subcategories": {
"Аналитик безопасности": [
"аналитик безопасности", "security analyst", "SOC analyst", "мониторинг безопасности",
"инциденты", "incident response", "SIEM", "угрозы",
"threat intelligence"
],
"Пентестер": [
"тестирование на проникновение", "penetration tester", "этичный хакер", "ethical hacker",
"red team", "vulnerability assessment", "web app pentest", "network pentest",
"bug bounty"
],
"Сетевой безопасник": [
"сетевой безопасник", "network security", "firewall", "IDS/IPS",
"VPN", "DDoS protection", "NGFW", "ZTNA",
"микросетевой сегментации"
],
"Криптограф": [
"криптограф", "cryptography", "шифрование", "encryption",
"PKI", "TLS/SSL", "криптоанализ", "квантовая криптография",
"алгоритмы"
],
"Аудит и комплаенс": [
"аудит безопасности", "security audit", "compliance", "ISO 27001",
"PCI DSS", "GDPR", "регуляторные требования", "риск-менеджмент",
"политики безопасности"
],
"AppSec": [
"безопасность приложений", "application security", "DevSecOps", "SAST",
"DAST", "SCA", "OWASP", "API security",
"secure coding"
],
"Cloud Security": [
"безопасность облаков", "cloud security", "AWS security", "Azure security",
"GCP security", "CSPM", "CASB", "container security",
"serverless security"
],
"DFIR": [
"киберрасследования", "digital forensics", "incident response", "DFIR",
"memory forensics", "disk forensics", "malware analysis", "threat hunting",
"EDR"
],
"GRC": [
"GRC", "governance", "risk management", "compliance",
"регуляторные требования", "политики безопасности", "стандарты", "аудит",
"risk assessment"
],
"Информационная безопасность (Другое)": [
"CISO", "директор по безопасности", "security architect", "безопасность IoT",
"безопасность ICS", "безопасность блокчейна", "криптоанализ", "стажер по безопасности",
"junior security analyst"
]
}
},
    "Менеджмент": {
"keywords": [
"менеджер", "manager", "руководитель", "head",
"директор", "director", "управление", "management", 
"лидер", "leader", "team lead", "тимлид",
"управляющий", "executive", "администратор", "supervisor"
],
"subcategories": {
"Топ-менеджмент": [
"генеральный директор", "CEO", "директор", "director",
"исполнительный директор", "executive director", "управляющий партнер","managing partner",
"президент компании", "president"
],
"Продуктовый менеджмент": [
"продуктовый менеджер", "product manager", "PM", "product owner",
"руководитель продукта", "head of product", "CPO", "директор по продукту",
"product lead"
],
"Проектный менеджмент": [
"проектный менеджер", "project manager", "PM", "руководитель проектов",
"project lead", "PMP", "scrum master", "agile coach",
"менеджер внедрения"
],
"ИТ-менеджмент": [
"ИТ-директор", "CIO", "CTO", "руководитель IT",
"директор по разработке", "head of development", "tech lead", "team lead",
"руководитель отдела IT"
],
"Маркетинг-менеджмент": [
"маркетинг-директор", "CMO", "head of marketing", "brand manager",
"product marketing manager", "performance marketing manager", "digital marketing manager",
"руководитель отдела маркетинга"
],
"Финансовый менеджмент": [
"финансовый директор", "CFO", "financial manager", "head of finance",
"контроллер", "controller", "FP&A manager", "казначей",
"treasurer"
],
"Операционный менеджмент": [
"операционный директор", "COO", "operations manager", "head of operations",
"руководитель производства", "plant manager", "менеджер склада", "supply chain manager",
"логистика"
],
"HR-менеджмент": [
"HR-директор", "CHRO", "head of HR", "HRBP",
"recruitment manager", "talent manager", "learning and development manager",
"руководитель HR", "директор по персоналу"
],
"Офис-менеджмент": [
"офис-менеджер", "office manager", "администратор офиса","executive assistant",
"руководитель административного отдела", "head of administration", "менеджер по административной работе"
],
"Менеджмент (Другое)": [
"менеджер по продажам", "sales manager", "account manager", "региональный менеджер",
"менеджер филиала", "branch manager", "менеджер по работе с клиентами",
"руководитель направления", "startup founder"
]
}
},
    "Дизайн": {
"keywords": [
"дизайнер", "designer", "дизайн", "design",
"графика", "graphic", "визуал", "visual",
"креатив", "creative", "ui", "ux",
"иллюстрация", "illustration", "анимация", "animation"
],
"subcategories": {
"Графический дизайн": [
"графический дизайнер", "graphic designer", "дизайнер полиграфии", "print designer",
"дизайнер упаковки", "packaging designer", "бренд-дизайнер", "brand designer",
"дизайнер рекламы", "advertising designer"
],
"UI/UX дизайн": [
"ui/ux дизайнер", "ui designer", "ux designer", "product designer",
"дизайнер интерфейсов", "interface designer", "web designer", "mobile designer",
"дизайнер приложений", "app designer"
],
"Моушн-дизайн": [
"моушн-дизайнер", "motion designer", "аниматор", "animator",
"2d анимация", "2d animation", "3d анимация", "3d animation",
"видеодизайнер", "video designer"
],
"Иллюстрация": [
"иллюстратор", "illustrator", "художник", "artist",
"концепт-артист", "concept artist", "character designer", "дизайнер персонажей",
"книжная иллюстрация", "book illustration"
],
"3D-дизайн": [
"3d дизайнер", "3d designer", "3d artist", "3d визуализатор",
"3d modeler", "3d моделлер", "blender artist", "cad designer",
"архитектурная визуализация", "archviz"
],
"Гейм-дизайн": [
"гейм-дизайнер", "game designer", "level designer", "дизайнер уровней",
"ui дизайнер игр", "game ui designer", "ux дизайнер игр", "game ux designer",
"концепт-артист игр", "game concept artist"
],
"Промышленный дизайн": [
"промышленный дизайнер", "industrial designer", "дизайнер мебели", "furniture designer",
"дизайнер продуктов", "product designer", "транспортный дизайн", "transportation design",
"эргономика", "ergonomics"
],
"Фэшн-дизайн": [
"дизайнер одежды", "fashion designer", "модельер", "designer одежды",
"текстильный дизайн", "textile design", "дизайнер аксессуаров", "accessory designer",
"обувной дизайн", "footwear design"
],
"Арт-дирекшн": [
"арт-директор", "art director", "креативный директор", "creative director",
"ведущий дизайнер", "lead designer", "дизайн-лид", "design lead",
"бренд-директор", "brand director"
],
"Дизайн (Другое)": [
"дизайнер интерьеров", "interior designer", "ландшафтный дизайнер", "landscape designer",
"световой дизайн", "lighting design", "типографика", "typography",
"дизайн-стажер", "design intern"
]
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
    moscow_tz = pytz.timezone('Europe/Moscow')

    role = 'professional_role=156&professional_role=160&professional_role=10&professional_role=12&professional_role=150&professional_role=25&professional_role=165&professional_role=34&professional_role=36&professional_role=73&professional_role=155&professional_role=96&professional_role=164&professional_role=104&professional_role=157&professional_role=107&professional_role=112&professional_role=113&professional_role=148&professional_role=114&professional_role=116&professional_role=121&professional_role=124&professional_role=125&professional_role=126'
    period = '&search_period=1'
    page='&page=0'
    per_page = '&per_page=5'
    a_list = []

    max_len = 5


    current_time = datetime.now() - timedelta(hours=1.5)
    current_time = current_time.astimezone(moscow_tz)

    i = 0
    while max_len == 5:
        i+=1
        url = f"https://api.hh.ru/vacancies?{role}{period}{page}{per_page}"
        page=f"&page={i}"
        data = requests.get(url).json()
        try:
            max_len = len(data['items'])
            for j in data['items']:
                    vacancy_list = {
                            "title": j['name'],
                            "company": j['employer']['name'],
                            "date": j['published_at'],
                            "location": j['area']['name'],
                            "employment": j['employment']['name'],
                            "experience": j['experience']['name'],
                            "salary": j['salary'],
                            "skills": j['snippet']['requirement'],
                            "link": j['alternate_url'],
                            'source' : 'hh',
                            'vacancy_type': j['professional_roles'][0]['name'], # не совсем честно, но пока сойдет
                            'new_category' : classify_vacancy(j['name'])

                        }
                    a_list.append(vacancy_list)
        except:
            max_len = 0
    return a_list


def safe_find_text(element, selector, **kwargs):
    found = element.find(selector, **kwargs) if element else None
    return found.text.strip() if found else None

def classify_vacancy(title, description=""):
    """Классифицирует вакансию по названию и описанию"""
    text = f"{title} {description}".lower()
    
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



def habr_parsing():
    a_list = []
    num_list = 30

    for j in range(num_list):
        data = requests.get(f'https://career.habr.com/vacancies?page={j}&type=all')
        soup = BeautifulSoup(data.content, 'html.parser')
        vacancy = soup.find_all('div', class_='vacancy-card')
        
        for i in vacancy:
            vacancy_list = {
            "title": safe_find_text(i, 'a', class_='vacancy-card__title-link'),
            "company": safe_find_text(i, 'a', class_='link-comp', href=lambda x: x and '/companies/' in x),
            "date": safe_find_text(i, 'time', class_='basic-date'),
            "location": safe_find_text(i, 'a', href=lambda x: x and 'city_id=' in x),
            'source' : 'habr',
            "employment": safe_find_text(i, 'span', class_='preserve-line', string=lambda x: x and 'Полный рабочий день' in x),
            "salary": safe_find_text(i, 'div', class_='basic-salary'),
            "skills": [skill.text.strip() for skill in i.find_all('a', class_='link-comp', href=lambda x: x and '/skills/' in x)] or '',
            "link": "https://career.habr.com" + i.find('a', class_='vacancy-card__title-link')['href'] 
                if i.find('a', class_='vacancy-card__title-link') else None,
            "new_category" : classify_vacancy(safe_find_text(i, 'a', class_='vacancy-card__title-link'))
            }

            a_list.append(vacancy_list)
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

    

    for i in habr_list:
        if i['link'] not in link_list:
            # Обработка skills (преобразуем в JSON строку, если это список/словарь)
            skills = json.dumps(i['skills']) if isinstance(i['skills'], (list, dict)) else i['skills']
            
            # Преобразование даты в datetime, если она в строковом формате
            date_value = parse_russian_date(i['date']) if isinstance(i['date'], str) else i['date']
            cursor.execute("""
                INSERT INTO vacans (title, company, date, employment, salary, skills, link, location, source, new_category) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,  %s)
            """, (
                i['title'], 
                i['company'], 
                date_value, 
                i['employment'], 
                i['salary'], 
                i['skills'], 
                i['link'],
                i['location'],
                i['source'],
                i['new_category']
                
            ))

    for i in hh_list:
        if i['link'] not in link_list:
            date_value = parse_date(i['date'])

            cursor.execute("""
            INSERT INTO vacans (title, company, date, employment, salary, skills, link, location, source, vacancy_type, experience, new_category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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


hh_list = hh_parsing()
habr_list = habr_parsing()

loading_to_base(hh_list, habr_list)

def main():
    try:
        logger.info("Запуск парсера...")
        hh_list = hh_parsing()
        logger.info("HH загрузило...")
        habr_list = habr_parsing()
        logger.info("Habr загрузило...")
        
        
        if hh_list or habr_list:
            loading_to_base(hh_list, habr_list)
            
    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)

if __name__ == "__main__":
    main()
