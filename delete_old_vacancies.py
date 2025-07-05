import psycopg2
from datetime import datetime, timedelta
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def delete_old_vacancies():
    conn = psycopg2.connect(
        host="pg4.sweb.ru",
        port=5433,
        database="maksimarkh",
        user="maksimarkh",
        password="Maksim1232145!"
    )
    cursor = conn.cursor()

    try:
        # Вычисляем дату, которая была 8 дней назад
        ten_days_ago = datetime.now() - timedelta(days=8)
        
        # Удаляем записи старше 10 дней
        cursor.execute("DELETE FROM vacans WHERE date < %s", (ten_days_ago,))
        
        # Получаем количество удаленных записей
        deleted_count = cursor.rowcount
        
        conn.commit()
        print(f"Удалено {deleted_count} записей старше 8 дней")
        
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при удалении старых записей: {e}")
        
    finally:
        cursor.close()
        conn.close()

# Пример вызова функции
def main():
    try:
        logger.info("Запуск удаления...")
        delete_old_vacancies()
        logger.info("Вакансии удалены")
        
    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)

if __name__ == "__main__":
    main()
