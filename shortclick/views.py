from .models import User, Website, Webpage, Ticket, Transit
from .utils import *
from flask import Flask, request, session, redirect, url_for, render_template, flash
import random as rand
import json
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
    return 'Live'

@app.route('/user/create', methods=['POST', 'GET'])
def new_user_no_ticket():
    if request.method == 'GET':
        response = User(None).create()
        resp = '{"token": "'+response[0]+'", "auth" : "'+response[1]+'"}'
    else:
        resp = 'Not functional'
    return resp

@app.route('/get_suggestion/<token>', methods=['POST'])
def get_suggestion(token):
    if request.method == 'POST':
        data = request.get_json(force=True)
        auth = data["stack"]["auth"]
        website_uri = data["stack"]["website"][0]
        website_page = data["stack"]["website"][1]
        # if User(token).verify_password(auth):
                        

# Conditions
# Interaction within 3 hours
# 
# Transit(token, timestamp()).create()
# @app.route('/add_website', methods=['POST'])
# def show_links():

@app.route('/add_website', methods=['POST'])
def add_website():
    response = ''
    if request.method == 'POST':
        data = request.get_json(force=True)
        token = data["stack"]["token"]
        # print('token [x] : {0}'.format(token))
        auth = data["stack"]["auth"]
        website_uri = data["stack"]["website"][0]
        website_page = data["stack"]["website"][1]
        if User(token).verify_password(auth):
            previous_page = get_most_recent_page(token)
            current_ts = timestamp()

            Website(website_uri).create()
            recent_page_visit = get_most_recent_specific_page(token, website_page)
            overload_flag = True
            if(recent_page_visit != []):
                time_dif = time_diff(recent_page_visit[0]['v.timestamp'],current_ts)
                if(time_dif[0]*60+time_dif[1]) < 2:
                    overload_flag = False

            if (recent_page_visit == [] or not overload_flag):
                site_visit(token, website_uri)
                
                if not website_uri == website_page:

                    Webpage(website_page).create()
                    page_visit(token, website_page)
                    Website(website_uri).has_webpage(website_page)
                    
                    if website_page != previous_page[0] and time_diff(previous_page[1], current_ts)[0] < 3*60:
                        transit = Transit(token, timestamp())
                        page_from = Webpage(previous_page[0]).exists()
                        page_to = Webpage(website_page).exists()
                        transit.create(page_from, page_to)


            resp = 'Added'
        else:
            resp = 'Doesn\'t exist'
    return resp


@app.route('/ticket/create', methods=['GET'])
def create_ticket():
    response = ''
    if request.method == 'GET':
        return json_resp(Ticket(None).create())

@app.route('/ticket/exist', methods=['POST'])
def exist_ticket():
    response = ''
    if request.method == 'POST':
        data = request.get_json(force=True)
        ticket_tok = data["stack"]["ticket"]
        if None != Ticket(ticket_tok).exists():
            response = 'True'
        else:
            response = 'False'
        return response

def json_resp(json_item):
    return app.response_class(
            response=json.dumps(json_item),
            status=200,
            mimetype='application/json'
        )
