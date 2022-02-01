import requests
from bs4 import BeautifulSoup
import time
from random import randrange
import json

headers = {
	'accept': '',
	'user-agent' : ''
}


def get_artical_urls(url):
	s = requests.Session()
	response = s.get(url=url, headers=headers)

	soup = BeautifulSoup(response.text, 'lxml')
	#get pagination count
	pagination_count = int(soup.find('div', class_='class').find_all('a')[-3].text)

	#links list
	articles_urls_list = []
	#get links from all page
	for page in range(1, pagination_count + 1):
		response = s.get(url=f'!!url!!{page}',headers=headers)
		soup = BeautifulSoup(response.text, 'lxml')


		articles_divs = soup.find_all('div', class_='class') #get articles
		for div in articles_divs:
			tag_a = div.find_all('a')[1]
			link = tag_a.get('href')
			articles_urls_list.append('!!url!!'+link)

		time.sleep(randrange(2,5))
		print(f'Обработал {page} из {pagination_count}')

	with open('urls.txt','w') as file:
		for url in articles_urls_list:
			file.write(f'{url}\n')

	return 'Работа по сбору ссылок завершена!'

def get_data(file_path):
	with open(file_path) as file:
		urls_list = [line.strip() for line in file.readlines()]

	urls_count = len(urls_list)

	s = requests.Session()
	result_data = []

	for url in urls_list[:5]:
		response = s.get(url=url, headers=headers)
		soup = BeautifulSoup(response.text, 'lxml')
		#get data
		product_title = soup.find('div', class_='class').find('h1').text.strip()
		main_img = f"!!url!!{soup.find('a', class_='class').get('attr')}"
		price = soup.find('p', class_='class').find_all('span')[1].text.strip()
		description = soup.find('div', id='id').text.strip().replace('\n','<br>')
		#data append
		result_data.append(
			{
				'original_url': url,
				'title': product_title,
				'main_img': main_img,
 				'price': price,
				'description': description
			}
		)

		#data save
		with open('result.json', 'w') as file:
			json.dump(result_data, file, indent=4, ensure_ascii=False)


def main():
	#for begin start the `get_artical_urls`, late start the `get_data`
	#get_artical_urls(url='url')
	get_data('urls.txt')

if (__name__ == "__main__"):
	main()