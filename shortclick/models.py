from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from .utils import *
import os
import uuid
from .utils import *

url = "bolt://localhost:7687"
# username = os.environ.get('NEO4J_USERNAME')
# password = os.environ.get('NEO4J_PASSWORD')
# username = "boss"
# password = "b.xqcTsircBHDx.szQ4ClgMJU4pZCh1"

graph = Graph(url + '/db/data/')

class Website:
    def __init__(self, uri):
        self.uri = uri

    def exists(self):
        return graph.find_one('Website', 'uri', self.uri)
    
    def create(self):
        w_exist = self.exists()
        if None == w_exist:
            website = Node('Website', uri=self.uri)
            graph.create(website)
        else:
            website = w_exist
        return website

    def has_webpage(self, url):
        website = graph.find_one('Website', 'uri', self.uri)
        webpage = graph.find_one('Webpage', 'url', url)
        if None != webpage and None != website:
            rel1 = Relationship(website,'HAS', webpage)
            graph.create(rel1)

class Webpage:
    def __init__(self, url):
        self.url= url

    def create(self):
        p_exist = self.exists()
        if None == p_exist:
            webpage = Node('Webpage', url=self.url)
            graph.create(webpage)
        else:
            webpage = p_exist
        return webpage

    def exists(self):
        return graph.find_one('Webpage', 'url', self.url)

class Ticket:
    def __init__(self, token):
        if not token == None:
            self.token = token

    def create(self):
        while True:
            rand_token = randToken()
            if not graph.find_one('Ticket', 'token', randToken()):
                self.token = rand_token
                break
            ticket = Node('Ticket', 'token', self.token)
            graph.create(ticket)
        return self.token

    def exists(self):
        return graph.find_one('Ticket', 'token', self.token)

class Transit:
    def __init__(self, user_token, timestamp):
        self.timestamp = timestamp
        self.user_token = user_token

    def create(self, webpage_from, webpage_to):
        pages_transit(webpage_from, webpage_to, self.user_token)

class User:
    def __init__(self, token):
        if not token == None:
            self.token = token

    def tell(self):
        user = self.find()
        return user['auth']

    def verify_password(self, auth):
        user = self.find()
        if user:
            return bcrypt.verify(auth, user['auth'])
        else:
            return False

    def find(self):
        user = graph.find_one('User', 'token', self.token)
        return user

    def create(self):
        rand_auth = randToken()
        while True:
            rand_token = randToken()
            if not graph.find_one('Ticket', 'token', rand_token):
                self.token = rand_token
            break
        user = Node('User', token=self.token, auth=bcrypt.encrypt(rand_auth))
        graph.create(user)
        return [rand_token, rand_auth]

    def add_visit_website(self, uri, timestamp):
        website = Website(uri).create()
        user = self.find()
        rel = Relationship(user, 'VISITED', website, timestamp=timestamp)
        graph.create(rel)
        return website

    def add_visit_webpage(self, website, url, timestamp):
        webpage = Webpage(url).create()
        user = self.find()
        rel = Relationship(user, 'VISITED_PAGE', webpage, timestamp=timestamp)
        graph.create(rel)
        if None != graph.find_one('Webpage', 'url', url):
            rel1 = Relationship(website, 'HAS', webpage)
            graph.create(rel1)
        return webpage

    # def register(self, auth):
    #     if not self.find():
    #         user = Node('User', token=self.token, auth=bcrypt.encrypt(auth))
    #         graph.create(user)
    #         return True
    #     else:
    #         return False
