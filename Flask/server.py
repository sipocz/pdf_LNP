from asyncio.windows_events import NULL
from flask import Flask
from flask import render_template_string
from flask import render_template,request
from werkzeug.utils import secure_filename
from gensim.models import Doc2Vec
import pymongo
from collections import Counter

import os
app = Flask(__name__)

import requests

_AI_Search_Engine_URL_="http://192.168.2.6:5001/query/virus%20database%20update%20automatic"
req = requests.get(_AI_Search_Engine_URL_)
txt=req.text
print(txt)

def statistic(inp:list,best_n=3):
    fname_list=[ i["fname"] for i in inp]
    cc=Counter(fname_list)
    return cc.most_common(best_n)



@app.route('/')
def hello_world():
    outstr=render_template("login.html")
                                 
    return outstr

@app.route('/query_str', methods=['POST'])
def query2():
    _query=request.form["query_str"]
    print(_query)

    
    _AI_Search_Engine_URL_="http://192.168.2.6:5001/query/"+_query
    print(_AI_Search_Engine_URL_)
    req = requests.get(_AI_Search_Engine_URL_)
    print(type(req))
    processed_text = req.text

    print(type(processed_text))

    import json
    json_string=processed_text
    req_dict=json.loads(json_string)
    print(req_dict)
 
    #best_3=statistic(req_dict)


    req_list=list(req_dict.values())
    print(req_list)
    query_txt=_query
    if processed_text!="aaa":
        outstr=render_template("query.html",
                                 _query=req_list,
                                 _query_text=query_txt,
                                 #_best_3=best_3
                                 )
    
    return outstr





@app.route('/query', methods=['POST'])
def query():
    user = request.form['username']
    pwd = request.form['password']
    #_query=request.form["query_str"]
    #print(_query)
    processed_text = user+pwd
    outstr=" Hibás azonosítás !!!"
    if processed_text=="aaa":
        outstr=render_template("query_1.html",
                                 _query=NULL,
                                 _best_3=NULL
                                 
                                 )
    
    return outstr



if __name__ == '__main__':
   porto = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=porto)