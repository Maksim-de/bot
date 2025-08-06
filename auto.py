import asyncpg
import requests


import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

async def update_count(user_id, count) -> tuple:
    conn = None
    try:
        conn = await asyncpg.connect(
            host="pg4.sweb.ru",
            port=5433,
            database="maksimarkh",
            user="maksimarkh",
            password="Maksim1232145!"
        )
        
        # 1. Получаем текущее значение count из базы данных
        current_count = await conn.fetchval(
            "SELECT count FROM users WHERE user_id = $1",
            str(user_id)
        )
        
        # Если записи нет, current_count будет None, тогда устанавливаем 0
        if current_count is None:
            current_count = 0
        
        # 2. Вычисляем новое значение
        new_count = current_count + int(count)
        
        # 3. Обновляем запись в базе данных
        await conn.execute(
            "UPDATE users SET count = $1 WHERE user_id = $2",
            new_count, str(user_id)
        )
        return {'message': "ok"}

    except Exception as e:
        print(f"Error in update_users: {e}")
        return {'message': f"{e}"}
    finally:
        if conn:
            await conn.close()
            
async def get_users():
    conn = None
    try:
        conn = await asyncpg.connect(
            host="pg4.sweb.ru",
            port=5433,
            database="maksimarkh",
            user="maksimarkh",
            password="Maksim1232145!"
        )
        
        users = await conn.fetch(
            "SELECT user_id, access_token, resume_id, new_category_auto, location_auto, experience_auto FROM users where resume_id is not Null"
        )

        result = [dict(user) for user in users]

        return {'message': result}

    except Exception as e:
        print(f"Error in update_users: {e}")
        return {'message': f"{e}"}
    finally:
        if conn:
            await conn.close()


async def load_vacancies_for_send(vacancy_categories, locations, experiences):
    """
    Загружает вакансии по нескольким категориям, локациям и уровням опыта
    Args:
        vacancy_categories: список или строка категорий (разделенных запятыми)
        locations: список или строка локаций (разделенных запятыми)
        experiences: список или строка уровней опыта (разделенных запятыми)
    Returns:
        Список словарей с вакансиями
    """
    def prepare_input(param):
        """Преобразует входной параметр в список"""
        if isinstance(param, str):
            return [item.strip() for item in param.split('\n')]
        elif isinstance(param, (list, tuple)):
            return list(param)
        return [str(param)]
    
    categories = vacancy_categories[1:-1].replace('"', '').replace("'", "").split(',')

    locations_list = locations[1:-1].replace('"', '').replace("'", "").split(',')

    exp_levels = experiences[1:-1].replace('"', '').replace("'", "").split(',')

    
    conn = None
    try:
        conn = await asyncpg.connect(
            host="pg4.sweb.ru",
            port=5433,
            database="maksimarkh",
            user="maksimarkh",
            password="Maksim1232145!"
        )
        
        # Формируем условия для SQL запроса
        category_conditions = " OR ".join([f"new_category LIKE '%{cat}%'" for cat in categories])
        location_conditions = " OR ".join([f"location LIKE '%{loc}%'" for loc in locations_list])
        experience_conditions = " OR ".join([f"experience LIKE '%{exp}%'" for exp in exp_levels])
        
        query = f"""
        SELECT link 
        FROM vacans 
        WHERE ({category_conditions})
          AND ({location_conditions})
          AND ({experience_conditions})
          AND date >= CURRENT_DATE - INTERVAL '4 day'
          AND source LIKE 'hh'
        """

        print(query)
        
        records = await conn.fetch(query)
        return [dict(record) for record in records]
        
    except Exception as e:
        print(f"Ошибка при загрузке вакансий: {e}")
        return []
    finally:
        if conn:
            await conn.close()

async def send_vacanc(access_token, resume_id, vacancy_id):

    url = "https://api.hh.ru/negotiations"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mr.JobHunter/1.0 (maksim.arkhipov.020@mail.ru)"
    }

    # Теперь используем multipart/form-data вместо JSON
    files = {
        'vacancy_id': (None, str(vacancy_id)),
        'resume_id': (None, str(resume_id)),
        'message': (None, 'Добрый день, заинтересовала вакансия. Предлагаю обсудить детали!')
    }

    response = requests.post(url, headers=headers, files=files)
    return response
async def main():
    try:
        logger.info("Запуск рассылки...")
        users = await get_users()
        for user in users['message']:
            logger.info(f"Обработка юзера {user}")
            vacanc_for_user = await load_vacancies_for_send(user['new_category_auto'], user['location_auto'], user['experience_auto'])
            logger.info(f"Загружено вакансий {len(vacanc_for_user)}")
            cou = 0
            for vacancy in vacanc_for_user[:25]:
                try:
                    otvet = await send_vacanc(user['access_token'], user['resume_id'], vacancy)
                    cou +=1
                except Exception as e:
                    logger.info(f"ошибка {e}")
            print(cou)
            await update_count(user['user_id'], cou)
            
    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)

if __name__ == "__main__":
    await main()


