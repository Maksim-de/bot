from aiogram import Bot, Router, types, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import *
from api_handler import *
from aiogram.utils.markdown import hbold, hitalic, hunderline, text, code
# from config import TOKEN_WEATHER
from datetime import datetime
import io
from category import *
import asyncio
import json
import html
import re
from aiogram.utils.markdown import html_decoration as hd
from bs4 import BeautifulSoup
import re
from markdown import markdown
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates

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



from aiogram import F
from aiogram.types import Message, FSInputFile
import logging

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

users = {}

selected_subcategories = {}

selected_cities = {}

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.filters import Command
from aiogram import html as h
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Главное меню
main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Поиск вакансий")],
    [KeyboardButton(text="AI ассистент")],
    [KeyboardButton(text="В начало"), KeyboardButton(text="Помощь")]
], resize_keyboard=True)

# Меню категорий вакансий
categories_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Аналитика"), KeyboardButton(text="Разработка")],
    [KeyboardButton(text="Тестирование"), KeyboardButton(text="AI (ИИ)")],
    [KeyboardButton(text="Менеджмент"), KeyboardButton(text="Дизайн")],
    [KeyboardButton(text="Безопасность"), KeyboardButton(text="Администрирование")],
    [KeyboardButton(text="Готово")],  
    [KeyboardButton(text="В главное меню")]
], resize_keyboard=True)

# Функция для создания клавиатуры подкатегорий
def get_subcategories_keyboard(category: str, user_id: int = None) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    subcategories = category_keywords[category]["subcategories"].keys()

    # Добавляем кнопки подкатегорий (по 2 в ряд)
    for subcategory in subcategories:
        if user_id and str(user_id) in selected_subcategories and subcategory in selected_subcategories[str(user_id)]:
            text_button = f"✅ {subcategory}"
        else:
            text_button = subcategory
        builder.add(KeyboardButton(text=text_button))
    builder.adjust(2)
    print(selected_subcategories)
    # print(selected_subcategories[str(user_id)])
    # Добавляем кнопки управления (включая "Готово")
    builder.row(
        KeyboardButton(text="Назад в категории"),
        KeyboardButton(text="Готово")
        
    )
    # builder.row(KeyboardButton(text="В главное меню"))
    
    return builder.as_markup(resize_keyboard=True)



# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    # user_id = message.from_user.id
    user_id = str(message.from_user.id)
    await state.set_state(Form.user_id)
    await state.update_data(user_id=user_id) 
    print(f"Processing user {user_id}")
    await check_and_add_user(user_id, message.from_user.first_name)


    
    welcome_text = (
        f"{h.bold('🌟 Привет, я твой персональный hr-помощник! 🏋️‍♀️')}\n\n"
        f"{h.italic('Я помогу тебе найти работу мечты,')}\n"
        f"• {h.bold('/set_profile')} - {h.italic('В работе')}\n"
        f"• {h.bold('/update_resume')} - {h.italic('Редактирование резюме')}\n"
        f"Для удобной работы со мной можешь воспользоваться меню.\n"
        f"Первым делом создай профиль пользователя {h.bold('/set_profile')}"
    )
    print("User checked/added to DB")
    await message.answer(welcome_text,  parse_mode="HTML", reply_markup=main_keyboard)
    print("Welcome message sent")


# Обработчик кнопки "Поиск вакансий"
@router.message(lambda message: message.text == "Поиск вакансий")
async def search_vacancies(message: Message):
    await message.answer("Выберите категорию:", reply_markup=categories_keyboard)

# Обработчик выбора категории
@router.message( lambda message: message.text in category_keywords.keys())
async def handle_category(message: Message, state: FSMContext):
    category = message.text
    await state.set_state(Form.category)
    await state.update_data(current_category=category)
    data = await state.get_data()
    user_id = str(data.get('user_id'))
    await message.answer(
        f"Выберите подкатегории для {category}:\n"
        "Можно выбрать несколько вариантов",
        reply_markup=get_subcategories_keyboard(category, user_id)
    )

# Обработчик выбора подкатегорий
@router.message(F.text, lambda message: any(
    message.text.replace("✅ ", "") in subcats 
    for cat in category_keywords.values() 
    for subcats in cat["subcategories"].keys()
))
async def handle_subcategory(message: Message):
    user_id = str(message.from_user.id)
    # user_id = message.from_user.id
    subcategory = message.text.replace("✅ ", "")  # Удаляем эмодзи если есть
    
    if user_id not in selected_subcategories:
        selected_subcategories[user_id] = set()
    
    if subcategory in selected_subcategories[user_id]:
        selected_subcategories[user_id].remove(subcategory)
        action = "❌ Убрано из выбора"
    else:
        selected_subcategories[user_id].add(subcategory)
        action = "✅ Добавлено к выбору"
    
    # Получаем текущую категорию для обновления клавиатуры
    current_category = next(
        cat for cat in category_keywords 
        if subcategory in category_keywords[cat]["subcategories"]
    )
    
    selected = "\n".join(selected_subcategories.get(user_id, ["Пока ничего не выбрано"]))
    await message.answer(
        f"{action}: {subcategory}\n\n"
        f"Текущий выбор:\n{selected}\n\n"
        "Продолжайте выбирать или нажмите 'Готово'",
        reply_markup=get_subcategories_keyboard(current_category, user_id)
    )

@router.message(lambda message: message.text == "Готово")
async def handle_subcategories_done(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    print('Весь список', selected_subcategories)
    if user_id is None:
        user_id = str(message.from_user.id)
    print(user_id)
    vacancy_list = selected_subcategories[user_id]
    print('vacancy_list', vacancy_list)

    
    
    selected = "\n".join(selected_subcategories[user_id])
    await message.answer(
        f"Вы выбрали:\n{selected}\n\n"
        "Пожалуйста выберите или введите город...",
        reply_markup=get_cities_keyboard(all_cities)
    )



    
def get_cities_keyboard(all_cities,user_id: int = None) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Назад в категории"))
    builder.row(KeyboardButton(text="Начать поиск вакансий"))
    builder.adjust(1)
    
    
    # Полный список городов России (пример)
    all_cities_now = all_cities
    
    # Приоритетные города (должны быть в начале)
    priority_cities = ["Москва", "Санкт-Петербург", "Казань"]
    
    # Сортируем города: сначала приоритетные, затем остальные по алфавиту
    sorted_cities = priority_cities + sorted(
        [city for city in all_cities_now if city not in priority_cities],
        key=lambda x: x.lower()
    )
    
    # Добавляем кнопки городов (по 2 в ряд)
    for city in sorted_cities:
        if user_id and str(user_id) in selected_cities and city in selected_cities[str(user_id)]:
            text_button = f"✅ {city}"
        else:
            text_button = city
        builder.add(KeyboardButton(text=text_button))
    
    builder.adjust(2)
    
    # Добавляем кнопки управления

    return builder.as_markup(resize_keyboard=True)


@router.message(lambda message: message.text in ["Назад", "Назад в категории"])
async def back_to_categories(message: Message):
    await message.answer("Возвращаемся к выбору категорий", reply_markup=categories_keyboard)


@router.message(F.text, lambda message: message.text.replace("✅ ", "") in all_cities)
async def handle_city_selection(message: Message):
    user_id = str(message.from_user.id)
    city = message.text.replace("✅ ", "")  # Удаляем эмодзи если есть
    
    # Инициализируем множество для пользователя, если его нет
    if user_id not in selected_cities:
        selected_cities[user_id] = set()
    
    # Добавляем или удаляем город
    if city in selected_cities[user_id]:
        selected_cities[user_id].remove(city)
        action = "❌ Убрано из выбора"
    else:
        selected_cities[user_id].add(city)
        action = "✅ Добавлено к выбору"
    
    # Формируем список выбранных городов
    selected = "\n".join(selected_cities.get(user_id, ["Пока ничего не выбрано"]))
    
    # Обновляем клавиатуру
    await message.answer(
        f"{action}: {city}\n\n"
        f"Текущий выбор:\n{selected}\n\n"
        "Продолжайте выбирать или нажмите «Начать поиск»",
        reply_markup=get_cities_keyboard(all_cities, user_id)
    )


@router.message(F.text == "Начать поиск вакансий")
async def handle_vacancy_search(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    
    # Проверяем, что пользователь выбрал города
    if not selected_cities.get(user_id):
        await message.answer(
            "❌ Вы не выбрали ни одного города!\n"
            "Пожалуйста, выберите города для поиска.",
            reply_markup=get_cities_keyboard(all_cities, user_id)
        )
        return
    
    try:
        # Сохраняем выбранные города в базу
  
        # Получаем данные из state (если нужно)
        category = selected_subcategories[user_id]

        category_text =  "\n".join(f"• {category}" for category in selected_subcategories[user_id])
        
        # Формируем текст с выбранными городами
        cities_text = "\n".join(f"• {city}" for city in selected_cities[user_id])
        
        # Начинаем поиск
        await message.answer(
            "🔍 Начинаем поиск вакансий...\n\n"
            f"<b>Категория:</b> {category_text}\n"
            f"<b>Города:</b>\n{cities_text}\n\n"
            "Новые вакансии моментально попадут к вам...",
            parse_mode="HTML", reply_markup=main_keyboard)
    except:
         await message.answer(
            "🔍 Ошибка блин блинский.\n\n",
            parse_mode="HTML", reply_markup=main_keyboard
        )
        
    
# Обработчик кнопки "В главное меню"
@router.message(lambda message: message.text == "В главное меню")
async def back_to_main(message: Message):
    user_id = message.from_user.id
    if user_id in selected_subcategories:
        del selected_subcategories[user_id]
    await message.answer("Возвращаемся в главное меню", reply_markup=main_keyboard)

@router.message(lambda message: message.text == "AI ассистент")
async def update_resume(message: Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="🔥 Прожарка резюме на основе вакансий")],
            [KeyboardButton(text="🎯 Общая оценка резюме")]
        ]
    )
    await message.answer(
        text=f"Привет, {message.from_user.first_name}! 👋 Я — твой AI-помощник для улучшения резюме. Давай сделаем твоё резюме идеальным! Что тебе нужно?",
        reply_markup=markup
    )



def escape_html(text):
    return markdown(text, extensions=['fenced_code'])


def clean_and_format(text: str) -> str:
    # Сначала экранируем HTML-спецсимволы
    # text = escape_html(text)
    
    # Преобразуем Markdown в HTML
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # **жирный** -> <b>жирный</b>
    # text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)      # *курсив* -> <i>курсив</i>
    

    # text = re.sub(r'</?h[1-6]>', '', text)  # Удаляем <h3> и подобные
    # text = re.sub(r'</?p>', '\n\n', text)   # Заменяем <p> на двойные переносы

    # text = text.replace('<hr/>', '\n━━━━━━━━━━\n')  # Заменяем горизонтальную линию
   

    # # Очищаем HTML через BeautifulSoup
    # soup = BeautifulSoup(text, 'html.parser')
    return text


@router.message(lambda message: message.text == "Общая оценка резюме")
async def greet(message: Message, state: FSMContext):
    await message.answer(
        text="Отлично, пришлите резюме в формате .pdf", 
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Form.resume)
    logger.info(f"Пользователь {message.from_user.id} перешёл в состояние Form.resume")

@router.message(F.document, Form.resume)  # Сначала проверяем состояние
async def handle_pdf(message: Message, state: FSMContext):
    try:
        if not message.document.file_name.lower().endswith('.pdf'):
            await message.answer("❌ Файл должен быть в формате PDF!")
            return

        logger.info(f"Получен документ: {message.document.file_name}")

        await message.answer("📄 Файл получил, мне нужно пару минут...")

        # Скачиваем файл
        file = await message.bot.download(message.document.file_id)
        if not file:
            await message.answer("❌ Не удалось загрузить файл. Попробуйте ещё раз.")
            return

        pdf_bytes = file.read()
        extracted_text = extract_text_from_pdf(pdf_bytes)

        if not extracted_text:
            await message.answer("❌ Не удалось извлечь текст из PDF. Убедитесь, что файл не сканированный.")
            return

        logger.info(f"Извлечен текст из документа: {message.document.file_name}")
        answer = generating_answer_without_vacancy(extracted_text, temp=0.8)
        # answer = answer.replace("**", "<b>").replace("*", "<i>") 
        print(answer)
        # answer = html.escape(answer)
        # answer = answer.replace("_", "\\_").replace("*", "\\*").replace("`", "\\`").replace("#", "\\#")
        answer = clean_and_format(answer)
        print(answer) 
        await message.answer(answer, parse_mode="HTML")
        await state.clear()

    except Exception as e:
        logger.error(f"Ошибка при обработке PDF: {e}")
        await message.answer("⚠️ Произошла ошибка. Попробуйте другой файл.")
        await state.clear()





@router.message(lambda message: message.text == "🔥 Прожарка резюме на основе вакансий")
async def start_resume_roast(message: Message, state: FSMContext):
    await state.set_state(ResumeStates.waiting_for_category)
    await message.answer(
        "🔍 Для точной прожарки твоего резюме выбери категорию вакансий:",
        reply_markup=categories_keyboard
    )

@router.message(ResumeStates.waiting_for_category, lambda message: message.text in category_keywords.keys())
async def handle_resume_category(message: Message, state: FSMContext):
    category = message.text
    await state.update_data(resume_category=category)
    await state.set_state(ResumeStates.waiting_for_subcategory)
    
    await message.answer(
        f"Выбери подкатегорию для {category}:\n"
        "Мы подберем актуальные вакансии для сравнения",
        reply_markup=get_subcategories_keyboard(category, message.from_user.id)
    )

@router.message(ResumeStates.waiting_for_subcategory, lambda message: any(
    message.text.replace("✅ ", "") in subcats 
    for cat in category_keywords.values() 
    for subcats in cat["subcategories"].keys()
))
async def handle_resume_subcategory(message: Message, state: FSMContext):
    subcategory = message.text.replace("✅ ", "")
    await state.update_data(resume_subcategory=subcategory)
    
    data = await state.get_data()
    category = data.get('resume_category')
    
    await message.answer(
        f"🔥 Отлично! Сейчас проанализируем твое резюме по параметрам:\n\n"
        f"• Категория: {category}\n"
        f"• Подкатегория: {subcategory}\n\n"
        "Пришли мне свое резюме в формате PDF",
        reply_markup=ReplyKeyboardRemove()
    )
    # Здесь можно добавить переход в следующее состояние для обработки файла

@router.message(ResumeStates.waiting_for_category, lambda message: message.text == "В главное меню")
@router.message(ResumeStates.waiting_for_subcategory, lambda message: message.text == "В главное меню")
async def cancel_resume_roast(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Возвращаемся в главное меню",
        reply_markup=main_keyboard
    )




# Бд ниже


async def hourly_db_update(bot: Bot):
    """Ежечасное обновление БД"""
    while True:
        await asyncio.sleep(3600)  # 1 час
        print(f"[{datetime.now()}] Запуск обновления БД...")
        print(selected_subcategories)
        await save_selected_subcategories()
        print('Данные загруженны')
        await send_personalized_vacancies(bot)  # Убедитесь, что router доступен в этой области видимости

    
        

async def start_background_tasks(bot: Bot):
    """Запуск фоновых задач при старте"""
    global selected_subcategories
    global selected_cities
    global all_cities
    global vacanciessss

    loaded_data, all_cities, selected_cities = await load_selected_subcategories()
    vacanciessss = await load_and_cache_vacancies()
    selected_subcategories.update(loaded_data)
    print(f"[{datetime.now()}] Загружено {len(loaded_data)} пользовательских выборов из БД")
    
    asyncio.create_task(hourly_db_update(bot))

# Сохраним в базу данных

async def save_selected_subcategories():
    if not selected_subcategories:
        return
    
    conn = await asyncpg.connect(
        host="pg4.sweb.ru",
        port=5433,
        database="maksimarkh",
        user="maksimarkh",
        password="Maksim1232145!"
    )
    
    try:
        for user_id, subcategories in selected_subcategories.items():
            await conn.execute(
                "UPDATE users SET new_category = $1 WHERE user_id = $2",
                json.dumps(list(subcategories), ensure_ascii=False),   # Преобразуем set в list для хранения
                str(user_id)
            )
        print(f"Успешно сохранено {len(selected_subcategories)} пользователей")

        for user_id, cities in selected_cities.items():
            await conn.execute(
                "UPDATE users SET cities = $1 WHERE user_id = $2",
                json.dumps(list(cities), ensure_ascii=False),  # Преобразуем set в JSON
                str(user_id)  
            )
        
        print(f"[{datetime.now()}] Успешно сохранены города для {len(selected_cities)} пользователей")
    
    except json.JSONEncodeError as e:
        print(f"[{datetime.now()}] Ошибка кодирования JSON: {e}")
    except asyncpg.PostgresError as e:
        print(f"[{datetime.now()}] Ошибка базы данных: {e}")
    except Exception as e:
        print(f"[{datetime.now()}] Неожиданная ошибка: {e}")

        
    finally:
        await conn.close()



# При перезапуске
async def load_selected_subcategories() -> dict:
    """
    Загружает сохраненные подкатегории из базы данных
    Возвращает словарь в формате {user_id: set(subcategories)}
    """
    conn = None
    try:
        conn = await asyncpg.connect(
            host="pg4.sweb.ru",
            port=5433,
            database="maksimarkh",
            user="maksimarkh",
            password="Maksim1232145!"
        )
        
        # Загружаем данные из базы
        records = await conn.fetch(
            "SELECT user_id, new_category FROM users WHERE new_category IS NOT NULL"
        )
        city_list = await conn.fetch(
            "SELECT distinct location FROM vacans"
        )


        city_list = [record['location'] for record in city_list]
        city_list = [city for city in city_list if city is not None]

        city_for_users = await conn.fetch(
            "SELECT user_id, cities FROM users WHERE cities IS NOT NULL"
        )


        # Формируем словарь selected_subcategories
        loaded_data = {}
        for record in records:
            try:
                if record['new_category']:
                    # Декодируем JSON и преобразуем список в set
                    loaded_data[record['user_id']] = set(json.loads(record['new_category']))
            except json.JSONDecodeError as e:
                print(f"Ошибка декодирования для user_id {record['user_id']}: {e}")
                continue
        print(f"Успешно загружено {len(loaded_data)} записей из БД")

        loaded_data_city = {}
        for record in city_for_users:
            try:
                if record['cities']:
                    # Декодируем JSON и преобразуем список в set
                    loaded_data_city[record['user_id']] = set(json.loads(record['cities']))
            except json.JSONDecodeError as e:
                print(f"Ошибка декодирования для user_id {record['user_id']}: {e}")
                continue
                
        print(f"Успешно загружено {len(loaded_data_city)} записей из БД")
        return loaded_data, city_list, loaded_data_city
        
    except Exception as e:
        print(f"Ошибка при загрузке из БД: {e}")
        return {}
    finally:
        if conn:
            await conn.close()



# Загрузка актуальных вакансий

async def load_and_cache_vacancies():
    """
    Загружает вакансии и пользовательские выборки из БД,
    возвращает кортеж (vacancies_cache, user_selections)
    """
    conn = None
    try:
        conn = await asyncpg.connect(
            host="pg4.sweb.ru",
            port=5433,
            database="maksimarkh",
            user="maksimarkh",
            password="Maksim1232145!"
        )
        
        # 1. Загрузка вакансий
        records = await conn.fetch(
            "SELECT id, title, company, skills, location, experience, new_category, date, link FROM vacans WHERE date >= CURRENT_DATE - INTERVAL '1 day'"
        )
        
        # Кэшируем вакансии
        vacancies = {
            str(record['id']): {
                'title': record['title'],
                'company': record['company'],
                'skills': record['skills'],
                'location': record['location'],
                'experience': record['experience'],
                'categories': record['new_category'].split("|")[1],
                'date': record['date'],
                'link': record['link']
            }
            for record in records
        }
    
        
        return vacancies
        
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        return {}, {}
    finally:
        if conn:
            await conn.close()



from datetime import datetime, timedelta



# Глобальный словарь для хранения времени последней рассылки
last_send_time = {}
send_vacancies = {}

async def send_personalized_vacancies(bot: Bot):
    """Рассылает только новые вакансии, появившиеся с последней проверки"""
    try:
        current_time = datetime.now()
        
        # 1. Фильтруем только свежие вакансии
        fresh_vacancies = {
            vid: v for vid, v in vacanciessss.items()
            if datetime.strptime(str(v['date']), '%Y-%m-%d %H:%M:%S') >= current_time - timedelta(hours=24)
        }
        
        if not fresh_vacancies:
            print(f"{current_time}: Нет новых вакансий для рассылки")
            return
            
        # 2. Для каждого пользователя фильтруем вакансии
        for user_id, user_categories in selected_subcategories.items():
            user_cities = selected_cities.get(user_id, set())
            
            matched_vacancies = [
                v for v in fresh_vacancies.values()
                if (v['location'] in user_cities and
                    any(cat in v['categories'] for cat in user_categories))
            ]

            previously_sent_links = {vac['link'] for vac in send_vacancies.get(user_id, [])}  # Извлекаем ссылки ранее отправленных вакансий
            new_matched_vacancies = [vac for vac in matched_vacancies if vac['link'] not in previously_sent_links]

            
            if new_matched_vacancies:
                try:
                    for vac in matched_vacancies:
                        message = ["🔔 <b>Новые вакансии:</b>\n"]
                        message.append(
                                f"✨ <b>{vac['title']}</b>\n"
                                f"🏛 <i>{vac['company']}</i>\n\n"
                                f"🌍 <b>Локация:</b> {vac['location']}\n"
                                f"📆 <b>Опыт:</b> {vac['experience']}\n"
                                f"💼 <b>Навыки:</b> {', '.join(vac['skills'][:10])}{'...' if len(vac['skills']) > 10 else ''}\n\n"
                                f"🔗 <a href='{vac['link']}'>Подробнее о вакансии</a>\n"
                        )
                    
                    # Получаем бота из роутера
    
                        await bot.send_message(
                        chat_id=user_id,
                        text="".join(message),
                        parse_mode="HTML"
                        )
                    
                    last_send_time[user_id] = current_time
                    if user_id not in send_vacancies:
                        send_vacancies[user_id] = []  # Initialize if this is the first time for this user

                    send_vacancies[user_id].extend(new_matched_vacancies)
                    
                except Exception as e:
                    print(f"Ошибка отправки пользователю {user_id}: {e}")
                    
    except Exception as e:
        print(f"Критическая ошибка в рассылке: {e}")




import asyncpg

async def load_vacancies_for_analysis(vacancy_category):
    """
    Загружает вакансии и пользовательские выборки из БД,
    возвращает кортеж (vacancies_cache, user_selections)
    """
    conn = None
    try:
        conn = await asyncpg.connect(
            host="pg4.sweb.ru",
            port=5433,
            database="maksimarkh",
            user="maksimarkh",
            password="Maksim1232145!"
        )
        
        # 1. Загрузка вакансий
        records = await conn.fetch(
            f"SELECT title, salary, skills, location, experience, link FROM vacans WHERE new_category like '%{vacancy_category}'"
        )
        
        return records
        
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        return {}, {}
    finally:
        if conn:
            await conn.close()


async def hot_resume(pdf_text, vacancy_category,  temp):
    vacancies = await load_vacancies_for_analysis(vacancy_category)
    
    prompt = f"""
        Ты — HR-эксперт с 10+ лет опыта в IT-рекрутинге. 
        Проанализируй резюме для позиции {vacancy_category} и дай рекомендации, которые увеличат шансы на отклик на 50%. 

        **Жесткие правила:**
        1. Только факты из резюме (не додумывай)
        2. Сравнивай с вакансиями {vacancies}
        3. Пиши как личный консультант (без шаблонов)
        4. Макс. 2500 символов
        5. Не используй курсив, используй теги <b> для выделения жирного текста.

        **Структура ответа (Telegram-форматирование):**
        🎯 <b>Главная проблема</b>: 1-2 предложения
        📊 <b>Число подходящих вакансий</b>: "За последнюю неделю было X подходящих вашему описанию вакансий"
        💼 <b>Соответствие роли</b>: 3 пункта (совпадение/нехватка)
        💰 <b>Зарплатный потолок</b>: "Без доработок: X ₽ | С исправлениями: Y ₽". Если вакансий меньше 5, то пропусти этот пункт.
        🛠 <b>ТОП-3 исправления</b> (конкретные примеры):
        1. Заменить "фраза из резюме" → "оптимизированная версия"
        2. Добавить навык "самый частый skill из вакансий"
        3. Удалить "нерелевантный пункт"
        📈 <b>Быстрый чек</b>: "После правок +% откликов"
        🔗 <b>Ресурсы</b>: Совет что необходимо выучить
        4. Примеры вакансий за последнюю неделю: ссылки только из текстов вакансий, который тебе прислали.

        Резюме:
        {pdf_text}
        """

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
            "X-Title": "<YOUR_SITE_NAME>",      # Optional
        },
        model="deepseek/deepseek-r1-0528:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temp,  # 🔥 Указываем температуру (диапазон: 0.0–2.0)
        # Другие параметры:
        # max_tokens=4000,  # Ограничение длины ответа
        # top_p=0.9,        # Альтернатива температуре
    )
    return completion.choices[0].message.content


