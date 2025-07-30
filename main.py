import logging

from services.parser_service import LegoParserService


def setup_logging():
    """Настройка логирования"""
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )


def main():
    """Главная функция для запуска парсинга"""
    
    setup_logging()
    
    parser_service = LegoParserService()
    
    # Запуск парсинга товаров LEGO
    parser_service.start_parsing()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Парсинг прерван пользователем")
        logging.warning("Парсинг прерван пользователем")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        logging.error(f"Критическая ошибка в main: {e}")