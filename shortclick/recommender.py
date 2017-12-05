from .utils import *
from .models import *
import numpy as np

url = "bolt://localhost:7687"
graph = Graph(url + '/db/data/')
# First degree:
def get_recommendation(token, web_url):
	# First order (1)
	result_to = graph.data('MATCH (w2:Webpage)-[r:TRANSIT {token: {tok}}]->(w:Webpage  {url: {url}}) WITH w2, count(r) as rels WHERE rels > 0 RETURN rels, w2.url ORDER BY rels DESC', tok=token, url=web_url)
	# result_to_second = graph.data('MATCH v=(w:Webpage  {url:{url}})-[r:TRANSIT {token:{tok}}]-()-[t:TRANSIT {token:{tok}}]-(w2:Webpage) WITH w2, count(r) as rels WHERE rels > 0 RETURN rels, w2.url ORDER BY rels DESC', tok=token, url=web_url)
	# result_from = graph.data('MATCH v=()-[]-(w:Webpage  {url:"https://www.facebook.com/phocquard"})-[r:TRANSIT {token: {tok}}]->(w2:Webpage) WITH w2, count(r) as rels WHERE rels > 0 RETURN rels, w2.url ORDER BY rels DESC')
	
	all_elements = []
	first_order_on_page = graph.data('MATCH (w:Webpage {url: {url}}) <-[]-(web:Website)-[]-> (w2:Webpage) MATCH v=(w)-[r:TRANSIT {token: {tok}}]->(w2) WITH w2, count(r) as rels WHERE rels > 0 RETURN rels, w2.url ORDER BY rels DESC', tok=token, url=web_url)
	first_order_all = graph.data('MATCH v=(w:Webpage {url: {url}})-[r:TRANSIT {token: {tok}}]->(w2) WITH w2, count(r) as rels WHERE rels > 0 RETURN rels, w2.url ORDER BY rels DESC', tok=token, url=web_url)
	if len(first_order_on_page) < 1:
		first_order_on_page = first_order_all[:]
	all_elements.extend(first_order_on_page)


	# first_order_on_page_bidirectional = graph.data('MATCH (w:Webpage {url: {url}}) <-[]-(web:Website)-[]-> (w2:Webpage) MATCH v=(w)-[r:TRANSIT {token: {tok}}]-(w2) WITH w2, count(r) as rels WHERE rels > 0 RETURN rels, w2.url ORDER BY rels DESC', tok=token, url=web_url)
	# On page second order (2)
	# result_second_order_on_page =  graph.data('MATCH (w:Webpage {url:{url}}) <-[]-(web:Website)-[]-> (w2:Webpage) MATCH (w)-[r:TRANSIT {token:{tok}}]-()-[t:TRANSIT {token:{tok}}]->(w2) WITH w2, count(r) as rels WHERE rels > 0 RETURN rels, w2.url ORDER BY rels DESC', tok=token, url=web_url)
	four_order_on_site = graph.data('MATCH (w:Webpage {url: {url}}) <-[]-(web:Website)-[]->(w5:Webpage) '+
	'MATCH v=(w)-[r:TRANSIT {token: {tok}}]->'+
	'(w2)-[t:TRANSIT {token: {tok}}]->(w3)-[last_minus_one:TRANSIT {token: {tok}}]->(w4)-[:TRANSIT {token: {tok}}]->(w5) '+
	'WHERE w <> w5 AND w2 <> w5 AND w3 <> w5 AND w4 <> w5 MATCH (w5)-[last_one:TRANSIT {token: {tok}}]->(w6) '+
	'WITH AVG(last_one.timelaps) as avgl_time, COUNT(distinct v) as requests, w5 RETURN w5.url AS urly,'+
	' requests, avgl_time ORDER BY avgl_time DESC UNION MATCH (w:Webpage {url: {url}})'
	+' <-[]-(web:Website)-[]->(w4:Webpage) MATCH v=(w)-[r:TRANSIT {token: {tok}}]->'+
	'(w2)-[t:TRANSIT {token: {tok}}]->(w3)-[:TRANSIT {token: {tok}}]->(w4) WHERE w <> w4 AND w2 <> w4 AND w3 <> w4 MATCH (w4)-[last_one:TRANSIT {token: {tok}}]->(w5) '+
	'WITH AVG(last_one.timelaps) as avgl_time, COUNT(distinct v) as requests, w4 RETURN w4.url AS urly, requests, avgl_time '+
	'ORDER BY avgl_time DESC UNION MATCH (w:Webpage {url: {url}}) <-[]-(web:Website)-[]->(w3:Webpage) '+
	'MATCH v=(w)-[r:TRANSIT {token: {tok}}]->(w2)-[t:TRANSIT {token: {tok}}]->(w3) WHERE w <> w3 AND w2 <> w3 '+
	'MATCH (w3)-[last_one:TRANSIT {token: {tok}}]->(w4)  WITH AVG(last_one.timelaps) as avgl_time, COUNT(distinct v) as requests, w3 '+
	'RETURN w3.url AS urly, requests, avgl_time ORDER BY avgl_time DESC '+
	'UNION MATCH (w:Webpage {url: {url}}) <-[]-(web:Website)-[]->(w2:Webpage) '+
	'MATCH v=(w)-[r:TRANSIT {token: {tok}}]->(w2) WHERE w <> w2 '+
	'MATCH d=(w2)-[last_one:TRANSIT {token: {tok}}]->(w3)  WITH AVG(last_one.timelaps) as avgl_time, COUNT(distinct v) as requests,'+
	' w2 RETURN w2.url AS urly, requests, avgl_time ORDER BY avgl_time DESC', tok=token, url=web_url)
	

	sorted_array = []
	for item in all_elements:
		sorted_array.append(item['w2.url'])

	print(four_order_on_site)

	return sorted_array

	# Get top 10
	# first_order_rank : [()]

	#  Use time stamp of Usage, and how recent the page was visited.   === Inverse for increase == > Trend
	#  Decreasing weight for visit that was produced further away, Popularity trend decrease: hours(0.1),days(0.4),weeks(2),month(3.5),year(4)


	#  (4)
	# View timelapse
	# If user goes to point 3 from point 2 throught point 1 Where user spends more time on point 3 
	# View transition timestamp point 4 - point 3

	# Check on records  Allow user to send his "from page TRANSIT info" 

	# (3)
	# Give recommendation based on page visited just before and current.

	# (5)
	# Give recommendation based on click event.


