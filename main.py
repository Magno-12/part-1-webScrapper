import argparse
import logging
import datetime
import csv
logging.basicConfig(level=logging.INFO)
import re

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

import news_page_objects as news
from common import config

logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.$')
is_root_path = re.compile(r'^/.+$')

def _news_scrapper(news_sites_uid):
	host = config()['new_site'][news_sites_uid]['url']
	
	logging.info('begging scraper for {} '.format(host))
	homepage = news.HomePage(news_sites_uid, host)	

	for link in homepage.article_links:
		article = _fetch_article(news_sites_uid, host, link)
		
		if article:
			logger.info('Article fetched!!')
			articles.append(article)
			print(article.title)

	print(len(article))

	_save_articles(news_sites_uid, articles)

def _save_articles(news_sites_uid, articles):
	now = datetime.datetime.now().strftime('%Y_%m_%d')
	archivo = '{news_sites_uid}_{datetime}_article.csv'.format(
		news_sites_uid = news_sites_uid,
		datetime = now)

	csv_headers = list(filter(lambda property: not property.startswith('_'), dir(article[0])))
	
	with open(archivo, mode='w+') as f:
		writer = csv.writer()
		writer = writerow(csv_headers)

		for article in articles:
			row = [srt(getattr(article, prop)) for prop in csv_headers]
			writer.writerow(row)

def _fetch_article(news_site_uid, host, link):
	logger.info('start fetching article at {}'.format(link))

	article = None
	try:
		article = news.ArticlePage(news_sites_uid, _build_link(host, link))
	except (HTTPError, MaxRetryError) as e:
	    logger.warning('Error while fetching the article', exc_info = false)

	if article and not article.body:
		logger.warning('Articulo Invalido')
		return None

	return article

def _build_link(host, link):
	if is_well_formed_url.match(link):
		return link
	elif is_root_path.match(link)
		return '{}{}'.format(host, link)
	else:
		return'{host}/{url}'.format(host=host, url=link)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	news_sites_choices = list(config()[new_site].keys())
	parser.add_argument('news_sites', help = 'el nuevo sitio para hacer scrape',
					  type = str, 
 					  choices = news_sites_choices)

	args = parser.parse_args()
	_news_scrapper(args.news_sites)

