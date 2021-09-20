import scrapy  
from scrapy.crawler import Crawler
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import pandas as pd
from tqdm import tqdm

query = input("Enter Search Query:")
query = '+'.join(query.split())
urls = ['https://manipal.pure.elsevier.com/en/persons/?search='+query+'&searchBy=PartOfNameOrTitle']
names, ranks, institutes, site_links, emails = [], [], [], [], []

class MAHE_Scraper(scrapy.Spider):
	global urls, names, ranks, institutes, site_links, emails
	name = 'MAHE_Scraper'
	custom_settings = {
    	'LOG_ENABLED': False,
    }
	def parse(self, response):
		data = response.css('.rendering_person_short').getall()
		for panel in data:
			panel = panel.replace('<div class="rendering rendering_person rendering_short rendering_person_short"><h3 class="title"><a rel="Person" href="', "")
			site_link = panel[:panel.index('" class="link person"><span>')]
			panel = panel[panel.index('" class="link person"><span>')+len('" class="link person"><span>'):]
			name = panel[:panel.index('</span></a></h3><ul class="relations email"><li class="email"><a href="mailto:')].strip()
			panel = panel[panel.index('</span></a></h3><ul class="relations email"><li class="email"><a href="mailto:')+len('</span></a></h3><ul class="relations email"><li class="email"><a href="mailto:'):]
			email = panel[:panel.index('" class="link"><span>')].strip()
			panel = panel[panel.index('" class="link"><span>')+len('" class="link"><span>'):]
			panel = panel[panel.index('class="link organisation"><span>')+len('class="link organisation"><span>'):]
			institute = panel[:panel.index('</span></a><span class="minor dimmed">')]
			panel = panel[panel.index('</span></a><span class="minor dimmed">')+len('</span></a><span class="minor dimmed">'):]
			rank = panel[:panel.index('</span></li></ul><p class="type"><span class="family">')]
			panel = panel[panel.index('</span></li></ul><p class="type"><span class="family">')+len('</span></li></ul><p class="type"><span class="family">'):]
			names.append(name)
			site_links.append(site_link)
			emails.append(email.replace("%20", ""))
			institutes.append(institute)
			ranks.append(rank)
		yield None

process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
process.crawl(MAHE_Scraper, start_urls=urls)
process.start()

df = pd.DataFrame({'name': names, 'email': emails, 'site_link': site_links, 'institute': institutes, 'rank': ranks})
df.to_csv('Current.csv', index=False)