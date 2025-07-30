import logging
import json
import time

import requests
from bs4 import BeautifulSoup

final_links = []

class LegoProductParser:
    """Класс для парсинга данных товаров LEGO"""
    
    def __init__(self):
        """Инициализация парсера товаров"""
        
        self.all_products = []
    
    def extract_product(self, url):
        """Парсит данные одного товара"""
        
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Создаем словарь для данных товара
            product_data = {"url": url}
            
            # Извлекает Название товара
            title = soup.find('h1')
            if title:
                product_data["title"] = title.get_text(strip=True)
            
            # Цена со скидкой по карте
            price_with_discount = soup.find('span', class_='ds-text ds-text_weight_bold ds-text_color_price-term ds-text_typography_headline-3 ds-text_headline-3_tight ds-text_headline-3_bold')
            if price_with_discount:
                product_data["price_with_card"] = price_with_discount.get_text(strip=True)
            
            # Цена со скидкой с оплатой не по карте
            main_price = soup.find('span', class_='ds-text ds-text_weight_reg ds-text_color_text-secondary ds-text_typography_text ds-text_text_tight ds-text_text_reg')
            if main_price:
                product_data["price_without_card"] = main_price.get_text(strip=True)
            
            # Цена без скидки
            default_price = soup.find('span', class_='ds-text ds-text_decoration_line-through ds-text_weight_med ds-text_color_text-secondary ds-text_typography_lead-text ds-text_lead-text_tight ds-text_lead-text_med')
            if default_price:
                product_data["price_without_discount"] = default_price.get_text(strip=True)
            
            # Характеристики
            characteristics = {}
            char_blocks = soup.find_all('div', class_='_3rW2x _1o0tA _1MOwX _2eMnU')
            
            for i, block in enumerate(char_blocks[:5]):
                spans = block.find_all('span')
                
                if len(spans) >= 2:
                    key = spans[0].get_text(strip=True)
                    value = spans[1].get_text(strip=True)
                    characteristics[key] = value
            
            # Добавляем характеристики в словарь
            product_data["characteristics"] = characteristics
            
            # Возвращаем обычный словарь
            return product_data
            
        except Exception as e:
            logging.info(f"Ошибка при парсинге {url}: {e}")
            return {"url": url, "error": str(e)}
    
    def count_prices(self, product_data):
        """Подсчитывает количество найденных цен"""
        
        price_count = 0
        if "price_with_card" in product_data:
            price_count += 1
        if "price_without_card" in product_data:
            price_count += 1
        if "price_without_discount" in product_data:
            price_count += 1
        
        return price_count
    
    def extract_all_products(self):
        """Парсит все товары из списка ссылок"""
        
        global final_links
        
        total_links = len(final_links)
        
        logging.info(f"Начинаем парсинг {total_links} товаров...")
        
        for i, url in enumerate(final_links, 1):
            logging.info(f"\nПарсинг товара {i}/{total_links}")
            logging.info(f"URL: {url[:70]}...")
            
            product_data = self.extract_product(url)
            self.all_products.append(product_data)
            
            # Показываем краткую информацию
            if "title" in product_data:
                logging.info(f"Название: {product_data['title'][:50]}...")
            
            if "characteristics" in product_data:
                logging.info(f"Характеристик найдено: {len(product_data['characteristics'])}")
            
            # Подсчитываем количество найденных цен
            price_count = self.count_prices(product_data)
            logging.info(f"Цен найдено: {price_count}")
            
            time.sleep(1)
        
        return self.all_products
    
    def save_to_json(self, filename="all_lego_products.json"):
        """Сохраняет все товары в JSON файл"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.all_products, f, ensure_ascii=False, indent=2)
        
        logging.info(f"\nДанные сохранены в файл: {filename}")
        return len(self.all_products)