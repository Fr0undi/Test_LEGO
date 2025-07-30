import requests
from bs4 import BeautifulSoup
import logging
import time


class LegoLinksParser:
    """Парсер для извлечения ссылок на товары LEGO"""
    
    def __init__(self):
        """Инициализация класса парсера ссылок на товары LEGO"""
        
        self.all_links_of_products = []
        self.page_number = 1

    def get_page_products(self):
        """Извлекает ссылки на товары"""
        
        url = f"https://market.yandex.ru/search?text=lego&hid=10470548&hid=10682526&rs=eJwzKlcy4WLJSU3PFzj26CGzEgsHgwALmGSAkBoMWQxV7MbmxkaWxuYNjPOPsnYxMnEwVrFyTOn8z7KBkeETIx8HgwSDAgsYsoApBgipwZDF3sC4_2hrFyMTB2MVK8eUzv8sGxgZPjHycTBIsCgAuQrzGntY_zJ6XdGx72XSm5hsP5XpWUyo_QomkCQAsNPc0Q%3D%3D&glfilter=7893318%3A3732937&page={self.page_number}"
        
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Находим блок со всеми товарами
        block = soup.find('section', class_='_3BHKe SerpLayout serverList-item _3M-aW')
        if not block:
            return False
        
        # Находим все товары
        products = block.find_all('div', class_='cia-cs _E9Rt _2u9AV')
        if not products:
            return False
        
        # Извлекаем ссылки на товары
        for product in products:
            link_element = product.find('a')
            if link_element and link_element.get('href'):
                href = link_element.get('href')
                if href.startswith('/'):
                    href = 'https://market.yandex.ru' + href
                self.all_links_of_products.append(href)
        
        logging.info(f"Страница {self.page_number}: найдено {len(products)} товаров")
        return True

    def collect_links(self):
        """Метод сбора ссылок на товары"""
        
        while len(self.all_links_of_products) < 100:
            if not self.get_page_products():
                break
            self.page_number += 1
            time.sleep(1)

    def remove_duplicates(self):
        """Оставляем уникальные ссылки и ставим ограничение до 100 товаров"""
        
        unique_links = list(set(self.all_links_of_products))
        return unique_links[:100]

    def print_links(self, links):
        """Выводит все ссылки с нумерацией"""
        
        logging.info(f"\nВсего уникальных ссылок: {len(links)}")
        for i, link in enumerate(links, 1):
            logging.info(f"{i}. {link}")