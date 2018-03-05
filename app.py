from __future__ import print_function
import json
import os
from watson_developer_cloud import ConversationV1
from flask_cors import CORS
import general
from flask import Flask, request, url_for, send_from_directory
from flask_restful import Resource, Api, reqparse
from flask_jsonpify import jsonify
import psycopg2


con = None
 
try:
    con = psycopg2.connect("host='localhost' dbname='elearn-bot' user='postgres' password='arunkr'")   
    cur = con.cursor()
    cur.execute("SELECT * FROM Products")
 
    while True:
        row = cur.fetchone()
 
        if row == None:
            break
 
        print("Product: " + row[1] + "\t\tPrice: " + str(row[2]))


    con.commit()
except ImportError:
    if con:
        con.rollback()
 
    print("Error")   
    sys.exit(1)
 
finally:   
    if con:
        con.close()


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
            # try:
            #         try:
                        if os.getenv("conversation_workspace_id") is not None:
                            workspace_id = os.getenv("conversation_workspace_id")


                        #Making Conversation API call
                        # if request.args.get("context"):
                        #     context = json.loads(request.args.get("context"))
                        #     response = conversation.message(workspace_id='CONVERSATION_WORKSPACE_ID', input={ 'text': text}, context=json.dumps(context))
                        # else:
                        #     response = conversation.message(workspace_id='CONVERSATION_WORKSPACE_ID', input={'text': text })
                        response = conversation.message(workspace_id=CONVERSATION_WORKSPACE_ID, input={'text': text })
                        response = conversation.message(workspace_id=CONVERSATION_WORKSPACE_ID, input={ 'text': text}, context=response['context'])

                        #response = {'system': {'_node_output_map': {'node_5_1519388492197': [0]}, 'dialog_stack': ['node_5_1519388492197'], 'dialog_turn_counter': 2, 'dialog_request_counter': 2, 'branch_exited_reason': 'fallback', 'branch_exited': True}, 'conversation_id': 'd3be666e-e91f-4333-818a-92b08abe8521'}
                        #response = response['context']
                        headers = {
                            'Content-Type': 'application/json',
                        }
                        params = (
                            ('version', '2016-07-11'),
                        )
                        #print(response["context"])
                        #data = '{"input": {"text": "what brand sentiment changes do you recommend"}, "context": {'system': {'dialog_stack': ['node_5_1519388492197'], 'dialog_request_counter': 1, '_node_output_map': {'node_5_1519388492197': [0]}, 'dialog_turn_counter': 1}, 'conversation_id': 'd3be666e-e91f-4333-818a-92b08abe8521'}}'
                        #new = Template('{"input": {"text": $text}}')#, "context": $resp}')
                        #data = (new.substitute(text='"'+text+'"'))#,resp=json.dumps(response)))
                        #data = str(json.dumps(data))
                        #print(data)
                        #data = '{"input": {"text": "Do you have anybody in mind?"}, "context": {"conversation_id":"d3be666e-e91f-4333-818a-92b08abe8521","system":{"dialog_stack":["node_5_1519388492197"],"dialog_turn_counter":1,"dialog_request_counter":1,"_node_output_map":{"node_5_1519388492197":[0]}}}}'
                        #a = data
                        #print(a)
                        #if request.args.get("context"):
                        #    context = json.loads(request.args.get("context"))
                        #    new = Template('{"input": {"text": $text}, "context": $resp}')
                        #    data = (new.substitute(text='"'+text+'"',resp=json.dumps(context)))
                        #    response = requests.post('https://gateway.watsonplatform.net/conversation/api/v1/workspaces/783e1f0e-a27d-4ae2-b599-9a5ca33278d5/message?version=2016-07-11', headers=headers, data=data, auth=('2d224928-ad1e-4195-9972-930ed7beac79', 't6soWgeuLK3n'))
                        #   response = response.json()
                        #else:
                            #context = json.loads(request.args.get("context"))
                        #    new = Template('{"input": {"text": $text}}')#, "context": $resp}')
                        #    data = (new.substitute(text='"'+text+'"'))#,resp=json.dumps(context)))
                        #    response = requests.post('https://gateway.watsonplatform.net/conversation/api/v1/workspaces/783e1f0e-a27d-4ae2-b599-9a5ca33278d5/message?version=2016-07-11', headers=headers, data=data, auth=('2d224928-ad1e-4195-9972-930ed7beac79', 't6soWgeuLK3n'))
                        #    response = response.json()
                        con = psycopg2.connect("host='localhost' dbname='elearn-bot' user='postgres' password='arunkr'")   
                        cur = con.cursor()
                        cur.execute("SELECT * FROM Products")
                        row = cur.fetchone()
                        # print(row[1])
                        # colnames = [desc[0] for desc in curs.description]
                        
                        # while True:
                        #     row = cur.fetchone()
                        
                        #     if row == None:
                        #         break
                        
                        #     print("Product: " + row[1] + "\t\tPrice: " + str(row[2]))


                        

                        print(response["output"]["text"][0])
                        return response["output"]["text"][0] + row[1]

                        con.commit()
                        
                            
                                
                            
                                # words = response_speech.split()
                                # print(words)
                                # if "google" in response_speech:
                                #     google_regression()
                                # elif "apple" in response_speech:
                                #     apple_regression()                        
                        # else:
                              
                        #     print("You said {}".format(value))
            #         except sr.UnknownValueError:
            #             print("Oops! Didn't catch that")
            #         except sr.RequestError as e:
            #             print("Uh oh! Couldn't request results from Watson Speech Recognition service; {0}".format(e))
            # except KeyboardInterrupt:
            #     pass
		                 

api.add_resource(Hello, '/conversation/<text>')

if __name__ == "__main__":
    app.run(debug=True)