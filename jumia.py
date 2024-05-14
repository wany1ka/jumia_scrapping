import requests
from bs4 import BeautifulSoup
import csv
def scrape_jumia_products(url):
    jumia = requests.get(url)
    soup = BeautifulSoup(jumia.content, 'html.parser')
    products = soup.find_all('article', class_='prd _box _hvr')
    data = []
    for product in products:
        try:
            product_name = product.find('div', class_='name').text.strip()
        except AttributeError:
            product_name = 'product'
        try:
            brand_name = product.find('a', class_='brand').text.strip()
        except AttributeError:
            brand_name = 'product'
        try:
            price = product.find('div', class_='prc').text.strip()
        except AttributeError:
            price = 'product'
        try:
            discount = product.find('div', class_='bdg _dsct').text.strip()
        except AttributeError:
            discount = 'product'
        try:
            total_reviews = int(product.find('span', class_='total_reviews').text.strip())
        except (AttributeError, ValueError):
            total_reviews = 0
        popularity = "High" if total_reviews >= 100 else "Low"
        product_data = {
            'Product Name': product_name,
            'Brand Name': brand_name,
            'Price (Ksh)': price,
            'Discount (%)': discount,
            'Total Reviews': total_reviews,
            'Popularity': popularity
        }
        data.append(product_data)
    csv_file_path = 'jumia_products.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Product Name', 'Brand Name', 'Price (Ksh)', 'Discount (%)', 'Total Reviews', 'Popularity']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)
    print(f"Jumia products data saved to '{csv_file_path}'")
if __name__ == "__main__":
    jumia_url = 'https://www.jumia.co.ke/'
    scrape_jumia_products(jumia_url)