from .utils import *
from .models import *
import numpy as np

url = "bolt://localhost:7687"
graph = Graph(url + '/db/data/')

def perform_query(token, web_url, domain, state):
	four_order_on_site = graph.data('MATCH (w:Webpage {url: {url}}) <-[]-('+state+')-[]->(w5:Webpage) '+
	'MATCH v=(w)-[r:TRANSIT {token: {tok}}]->'+
	'(w2)-[t:TRANSIT {token: {tok}}]->(w3)-[last_minus_one:TRANSIT {token: {tok}}]->(w4)-[:TRANSIT {token: {tok}}]->(w5) '+
	'WHERE w <> w5 AND w2 <> w5 AND w3 <> w5 AND w4 <> w5 MATCH (w5)-[last_one:TRANSIT {token: {tok}}]->(w6) '+
	'WITH AVG(last_one.timelaps) as avgl_time, COUNT(distinct v) as requests, w5 RETURN w5.url AS urly,'+
	' requests, avgl_time ORDER BY avgl_time DESC UNION MATCH (w:Webpage {url: {url}})'
	+' <-[]-('+state+')-[]->(w4:Webpage) MATCH v=(w)-[r:TRANSIT {token: {tok}}]->'+
	'(w2)-[t:TRANSIT {token: {tok}}]->(w3)-[:TRANSIT {token: {tok}}]->(w4) WHERE w <> w4 AND w2 <> w4 AND w3 <> w4 MATCH (w4)-[last_one:TRANSIT {token: {tok}}]->(w5) '+
	'WITH AVG(last_one.timelaps) as avgl_time, COUNT(distinct v) as requests, w4 RETURN w4.url AS urly, requests, avgl_time '+
	'ORDER BY avgl_time DESC UNION MATCH (w:Webpage {url: {url}}) <-[]-('+state+')-[]->(w3:Webpage) '+
	'MATCH v=(w)-[r:TRANSIT {token: {tok}}]->(w2)-[t:TRANSIT {token: {tok}}]->(w3) WHERE w <> w3 AND w2 <> w3 '+
	'MATCH (w3)-[last_one:TRANSIT {token: {tok}}]->(w4)  WITH AVG(last_one.timelaps) as avgl_time, COUNT(distinct v) as requests, w3 '+
	'RETURN w3.url AS urly, requests, avgl_time ORDER BY avgl_time DESC '+
	'UNION MATCH (w:Webpage {url: {url}}) <-[]-('+state+')-[]->(w2:Webpage) '+
	'MATCH v=(w)-[r:TRANSIT {token: {tok}}]->(w2) WHERE w <> w2 '+
	'MATCH d=(w2)-[last_one:TRANSIT {token: {tok}}]->(w3)  WITH AVG(last_one.timelaps) as avgl_time, COUNT(distinct v) as requests,'+
	' w2 RETURN w2.url AS urly, requests, avgl_time ORDER BY avgl_time DESC', tok=token, url=web_url, dom=domain)
	return four_order_on_site
def get_recommendation(token, web_url, domain):

	# First order Example:
	# result_to = graph.data('MATCH (w2:Webpage)-[r:TRANSIT {token: {tok}}]->(w:Webpage  {url: {url}}) WITH w2, count(r) as rels WHERE rels > 0 RETURN rels, w2.url ORDER BY rels DESC', tok=token, url=web_url)
	# result_to_second = graph.data('MATCH v=(w:Webpage  {url:{url}})-[r:TRANSIT {token:{tok}}]-()-[t:TRANSIT {token:{tok}}]-(w2:Webpage) WITH w2, count(r) as rels WHERE rels > 0 RETURN rels, w2.url ORDER BY rels DESC', tok=token, url=web_url)
	# result_from = graph.data('MATCH v=()-[]-(w:Webpage  {url:"https://www.facebook.com/phocquard"})-[r:TRANSIT {token: {tok}}]->(w2:Webpage) WITH w2, count(r) as rels WHERE rels > 0 RETURN rels, w2.url ORDER BY rels DESC')
	
	all_elements = []
	# First order, multiple scope Example:
	# first_order_on_page = graph.data('MATCH (w:Webpage {url: {url}}) <-[]-(web:Website)-[]-> (w2:Webpage) MATCH v=(w)-[r:TRANSIT {token: {tok}}]->(w2) WITH w2, count(r) as rels WHERE rels > 0 RETURN rels, w2.url ORDER BY rels DESC', tok=token, url=web_url)
	# first_order_all = graph.data('MATCH v=(w:Webpage {url: {url}})-[r:TRANSIT {token: {tok}}]->(w2) WITH w2, count(r) as rels WHERE rels > 0 RETURN rels, w2.url ORDER BY rels DESC', tok=token, url=web_url)
	# if len(first_order_on_page) < 1:
	# 	first_order_on_page = first_order_all[:]
	# all_elements.extend(first_order_on_page)
	# sorted_array = []
	# for item in all_elements:
	# 	sorted_array.append(item['w2.url'])

	# recommendation = sorted_array
	# Restriction : site, domain, all
	states = ['web:Website', 'web:Website {domain: "'+domain+'"}', '']
	
	filtered_name_sort = []
	four_order_on_site = []
	for s in states:
		if len(filtered_name_sort) < 2:
			four_order_on_site.extend(perform_query(token, web_url, domain, s))
			four_order_on_site.sort(key=lambda x: x['avgl_time'], reverse=True)
			name_sort = sorted(four_order_on_site, key=lambda x: x['urly'], reverse=True)
			filtered_name_sort = []
			for idx, e in enumerate(name_sort):
				if idx > 0 and e['urly'] == name_sort[idx-1]['urly']:
					if e['requests'] > name_sort[idx-1]['requests']:
						del filtered_name_sort[len(filtered_name_sort)-1]
					else:
						continue
				filtered_name_sort.append(e)
			four_order_on_site = filtered_name_sort


	filtered_name_sort.sort(key=lambda x: x['avgl_time']*x['requests'], reverse=True)
	recommendation = [e['urly'] for e in filtered_name_sort]

	return recommendation


