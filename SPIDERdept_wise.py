import scrapy  
from scrapy.crawler import Crawler
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import pandas as pd
from tqdm import tqdm

urls = ['https://manipal.edu/mit/department-faculty.html']
names, ranks, image_links, emails = [], [], [], []

class MAHE_Scraper(scrapy.Spider):
	global urls, names, ranks, image_links, emails
	name = 'MAHE_Scraper'
	custom_settings = {
    	'LOG_ENABLED': False,
    }
	def parse(self, response):
		data = response.css('.members-wp').getall()
		data = [i.strip() for i in data]
		for panel in data:
			panel = [i.strip() for i in panel.split("\n") if i.strip()!='']
			image_link = 'https://manipal.edu/'+panel[3].replace('<img alt="image" class="lazyload" data-src="', '').replace('">', '')
			name = panel[7].replace('<', '').replace('h4>', '').replace('/', '')
			rank = panel[8].replace('<p>', '').replace('</p>', '')
			email = panel[9].replace('<p>', '').replace('</p>', '')
			names.append(name)
			image_links.append(image_link)
			emails.append(email.replace("%20", ""))
			ranks.append(rank)
		yield None

process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
process.crawl(MAHE_Scraper, start_urls=urls)
process.start()

df = pd.DataFrame({'name': names, 'email': emails, 'image_links': image_links, 'rank': ranks})
df.to_csv('Department_Wise.csv', index=False)