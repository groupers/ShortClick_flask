import random as rand
from datetime import datetime
from py2neo import Graph, Node, Relationship
from .models import *
url = "bolt://localhost:7687"
graph = Graph(url + '/db/data/')

def randToken():
    """ Random token generator
    Returns:
        (string)
    """
    a = '0123456789abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVXYZ'
    return "".join([rand.choice(a) for _ in range(30)])

def time_diff(origin, to):
    b = datetime.fromtimestamp(to)
    a = datetime.fromtimestamp(origin)
    c = b - a 
    return divmod(c.days * 86400 + c.seconds, 60)

def timestamp():
    # epoch = datetime.utcfromtimestamp(0)
    # now = datetime.now()
    # delta = now - epoch
    return int(datetime.now().timestamp())

def date():
    return datetime.now().strftime('%Y-%m-%d')


def site_visit(token, uri):
    graph.run('MATCH (u:User {token: {t}}), (s:Website {uri:{s}}) CREATE (u)-[:VISITED {timestamp: {ts}}]->(s)', t=token, s=uri, ts=timestamp())


def page_visit(token, url):
    graph.run('MATCH (u:User {token: {t}}), (p:Webpage {url:{p}}) CREATE (u)-[:VISITED_PAGE {timestamp: {ts}}]->(p)', t=token, p=url, ts=timestamp())

# MATCH (u:User {id: $userId}), (p:Park {id: $parkId})
# CREATE (u)-[:VISITED {timestamp: $timestamp}]->(p)
def get_most_recent_page(token):
    result = graph.data('MATCH (u:User {token:{a}})-[v:VISITED_PAGE]->'+
        '(p:Webpage) RETURN p.url, v.timestamp ORDER BY v.timestamp DESC LIMIT 1', a=token)
    return (result[0]['p.url'],result[0]['v.timestamp'])

def get_most_recent_specific_page(token, url):
    result = graph.data('MATCH (u:User {token:{a}})-[v:VISITED_PAGE]->'+
        '(p:Webpage {url: {u}}) RETURN v.timestamp ORDER BY v.timestamp DESC LIMIT 1', a=token,u=url)
    return result
    # return (result[0]['p.url'],result[0]['v.timestamp'])
    # return result[0]['v.timestamp']