import logging

from parsers import product_page
from parsers.product_page import LegoProductParser
from parsers.start_page import LegoLinksParser


class LegoParserService:
    """Сервис для парсинга товаров LEGO с Яндекс Маркета"""
    
    def __init__(self):
        """Инициализация сервиса парсинга"""
        
        self.links_parser = LegoLinksParser()
        self.product_parser = LegoProductParser()
    
    def start_parsing(self):
        """Запуск полного процесса парсинга"""
        
        logging.info("Запуск парсера товаров LEGO с Яндекс Маркета")
        
        # Сбор ссылок
        logging.info("Этап 1: Сбор ссылок на товары")
        self.links_parser.collect_links()
        final_links = self.links_parser.remove_duplicates()
        logging.info(f"Собрано {len(final_links)} уникальных ссылок")
        
        # Парсинг товаров
        logging.info("Этап 2: Парсинг данных товаров")
        
        # Передаем ссылки в парсер товаров
        product_page.final_links = final_links
        
        all_products = self.product_parser.extract_all_products()
        
        # Сохранение результатов
        logging.info("Этап 3: Сохранение результатов")
        saved_count = self.product_parser.save_to_json()
        
        logging.info(f"Парсинг завершен. Обработано {saved_count} товаров")