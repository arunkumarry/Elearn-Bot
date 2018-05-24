import json
import os
from watson_developer_cloud import ConversationV1
from flask_cors import CORS
from flask import Flask, request, url_for, send_from_directory
from flask_restful import Resource, Api, reqparse
from flask_jsonpify import jsonify
import psycopg2
from psycopg2.extensions import AsIs
import wikipedia
from autocorrect import spell


app = Flask(__name__)


CONVERSATION_WORKSPACE_ID="229647e2-25a3-446c-9050-09eeda995c2d"
conversation = ConversationV1(
     username='cda73843-4a24-4d09-95dc-cc4448750f4c',
     password='3G0IcHpVqmJG',
     version='2017-04-21')

# Statuses for each action
STATUS_ERROR = 400
STATUS_SUCCESS = 200

api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

class Hello(Resource):           
	def get(self,text):


                        if os.getenv("conversation_workspace_id") is not None:
                            workspace_id = os.getenv("conversation_workspace_id")


                      

                        response = conversation.message(workspace_id=CONVERSATION_WORKSPACE_ID, input={'text': text})
                        
                        headers = {
                            'Content-Type': 'application/json',
                        }
                        params = (
                            ('version', '2016-07-11'),
                        )
                        con = psycopg2.connect("host='localhost' dbname='elearBot' user='postgres' password='arunkr'")   
                        cur = con.cursor()

                        cur.execute("SELECT name FROM Categories")
                        cat = cur.fetchall()
                        new_data_cat = (' '.join(w) for w in cat)

                        cur.execute("SELECT name FROM Agile")
                        agile = cur.fetchall()
                        new_data_agile = (' '.join(w) for w in agile)

                        cur.execute("SELECT name FROM PMP")
                        pmp = cur.fetchall()
                        new_data_pmp = (' '.join(w) for w in pmp)

                        if response["intents"] :

                            if response["intents"][0]["intent"] == "price" :
                                TABLE = response["entities"][0]["entity"]
                            
                                NAME = response["entities"][0]["value"]
                                SQL1 = 'SELECT price FROM %s' %TABLE
                                SQL2 = SQL1 + " " + "WHERE name = '%s'" %NAME
                                print(SQL2)

                                cur.execute(SQL2)
                                agile_and_scrum = cur.fetchone()
                                print(agile_and_scrum)
                       

                        print(response)

                        if response["intents"] :

                            if response["intents"][0]["intent"] == "show_me_courses" :

                            # print(response)
                                return response["output"]["text"][0] + ":" + '\n,'.join([str(x) for x in new_data_cat])

                        

                            if response["intents"][0]["intent"] == "show_me_agile" :

                                return response["output"]["text"][0] + '\n,'.join([str(x) for x in new_data_agile])

                            if response["intents"][0]["intent"] == "show_me_pmp" :

                                return response["output"]["text"][0] + '\n,'.join([str(x) for x in new_data_pmp])

                            if response["intents"][0]["intent"] == "price" :

                                return response["output"]["text"][0] + '\n,'.join([str(x) for x in agile_and_scrum])

                            else :
                                return response["output"]["text"][0]

                        else :

                            a = ''
                            for i in text.split(' '):
                                a += spell(i) + ' '

                            print(a)                            # return response["output"]["text"][0]
                            return wikipedia.summary(a, sentences=1) + "::" + "https://en.wikipedia.org/wiki/" + a
                        con.commit()

          

api.add_resource(Hello, '/conversation/<text>')

if __name__ == "__main__":
    app.run(debug=True)
