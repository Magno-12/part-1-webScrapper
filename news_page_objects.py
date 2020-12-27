import bs4
import requests

from common import config

class NewsPage:

	def __init__(self, news_sites_uid, url):
		self._config = config()['new_site'][news_sites_uid]
		self._queries = self.config['queries']
		self.html = None

		self.visit(url)

		def _select(self, query_string):
			return self.html.select(query_string)

		def _visit(self, url):
			response = requests.get(url)
			
			response.raise_for_status()

			self._html = bs4.BeautifulSoup(response.text, 'html.parser')
class HomePage:

	def __init__(self, news_sites_uid, url):
		super().__init__(news_sites_uid)

	@property
	def article_links(self):
		link_list = []
		for link in self._select(self._queries['homepage_article_links']):
			if link and link.has.attr('href'):
				link_list.append(link)

		return set(link['href'] for link in link_list)


class ArticlePage(NewsPage):
	
	def __init__(self, news_sites_uid, url):
		super().__init__(news_sites_uid, url)
	
	@property
		def body(self):
			resultados = self._select(self._queries['article_body'])
			return resultados[0].text if len(resultados) else ''		

	@property
		def title(self):
			resultado = self._select(self.queries['article_title'])
			return resultados[0].text if len(resultados) else '' 
	
