from bs4 import BeautifulSoup
from sys import argv

import urllib
import json

#teste12345624
#74H4IHRA.

proxies = {'http': 'http://localhost:8090'}

# Paginacao -> adicionar p3_popular_desc na url
for n in range(0, 4):

	startURL = 'http://steamcommunity.com//market/search/render/?query=&start='+ str(float(n * 10)) +'&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=570'
	print startURL
	strItem = urllib.urlopen(startURL, proxies=proxies).read()
	jsonHTML = json.loads(strItem)
	r = jsonHTML['results_html']

	soup = BeautifulSoup(r)
	count = 0;
	arrayItens = [];

	# Adicionando itens no array os itens estao paginados
	for itens in soup.find_all('a', class_='market_listing_row_link'):
	    arrayItens.append(itens.get('href'))

	arrayItensID = [];
	# Entrando item a item para verificar a media

	def getItemPriceAVG( ID ):
		statsHtml = urllib.urlopen('http://steamcommunity.com//market/itemordershistogram?country=BR&language=brazilian&currency=1&item_nameid='+ID+'&two_factor=0', proxies=proxies).read()
		d = json.loads(statsHtml)
		#print "Maxima = " + str(d['graph_max_x'])
		#print "Minima = " + str(d['graph_min_x'])
		return (float(d['graph_max_x']) + float(d['graph_min_x'])) / 2.0

	def getItemID( html ):
		indexOf = html.find('Market_LoadOrderSpread( ')
		indexOfId = html.find(' );', indexOf)
		return html[ indexOf + len('Market_LoadOrderSpread( '): indexOfId ];

	def getLances( html , avg ):
		itemSoup = BeautifulSoup(html)
		for lance in itemSoup.find_all('span', class_='market_listing_price market_listing_price_without_fee'):
			if lance.getText().find('USD') > -1:
				preco =  lance.getText().replace('USD', '').replace('$', '').strip()
				desconto = 100 - (float(preco) * 100 / float(avg))
				print "Preco = " + str(preco) + " Desconto = " + str(desconto)


	for item in arrayItens:
		urlDecode=urllib.unquote(item).decode('utf8')
		print "Name    = " + urlDecode.split('/')[6]
		itemHtml = urllib.urlopen(str(urlDecode), proxies=proxies).read()
		itemId = getItemID(itemHtml)
		print "ItemID  = " + getItemID(itemHtml)
		itemAVG = getItemPriceAVG(itemId)
		print "ItemAVG = " + str(itemAVG)
		getLances(itemHtml, itemAVG)
		arrayItensID.append(itemId)

	print arrayItensID
 

print "Finalizado"