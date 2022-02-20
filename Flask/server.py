from asyncio.windows_events import NULL
from flask import Flask, send_from_directory, send_file
from flask import render_template_string
from flask import render_template,request
from werkzeug.utils import secure_filename
from gensim.models import Doc2Vec
import pymongo
from collections import Counter

import os
app = Flask(__name__,static_folder="static")

import requests

_AI_Search_Engine_URL_="http://192.168.2.6:5001/query/virus%20database%20update%20automatic"
req = requests.get(_AI_Search_Engine_URL_)
txt=req.text
print(txt)

def statistic(inp:list,best_n=3):
    fname_list=[ i["fname"] for i in inp]
    cc=Counter(fname_list)
    return cc.most_common(best_n)




def get_mongo_fileurl(fname:str):
    '''
    MONGODB adatbázisból filename alapján url visszaadása
    '''
    print("Mongo_start")
    _PDF_DB_="PDF_DB"
    _FILE_LOCATION_COLLECTION_="ABB_file_location"
    client = pymongo.MongoClient("mongodb+srv://pdfaidata:pdfaidatapwd@cluster0.fuant.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    mydb = client[_PDF_DB_]
    col=mydb[_FILE_LOCATION_COLLECTION_]


    cursor=col.find({"fname":fname})
    out_list=[]
    for out in cursor:
        out_list.append(out)
    print("Mongo end")
    return(out_list)

print("**** MONGODB  ****")  # DEBUG
print(get_mongo_fileurl("3BSE041434-600_A_en_System_800xA_6.0_System_Guide_Technical_Data_and_Configuration")) # DEBUG


def path_splitter(url):
    import pathlib
    split_up = url.split("/")
    out=[i+"/" for i in split_up[:-1]  ]
    out="".join(out) 
    return(out)


@app.route('/')
def hello_world():
    outstr=render_template("login.html")
                                 
    return outstr


@app.route('/download/<fname>')
def download(fname):
    print("-------------- DOWNLOAD --------------")
    print(f"fname:{fname}")
    
    print(f"PATH:{app.instance_path}")
    ret=get_mongo_fileurl(fname)
    print(ret)
    url=ret[0]["url"]
    directory=path_splitter(url)
    print(f"directory:{directory}")
    return send_file(directory+fname+".pdf",as_attachment=False)



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
    print("------- REQ_DICT -----")
    print(req_dict)
    print("______________")
  
    
   


    req_list=list(req_dict.values())



    print("++++++ REQ_ LIST +++++++++")
    print(req_list)

    for req_list_item in req_list:
        req_list_item["url"]=get_mongo_fileurl(req_list_item["fname"])[0]["url"]

    print("------ REQ LIST -----")
    print(req_list)


    best_3=statistic(req_list)
    print("******************")
    
    print(best_3)



    query_txt=_query



    if processed_text!="aaa":
        outstr=render_template("query.html",
                                 _query=req_list,
                                 _query_text=query_txt,
                                 _best_3=best_3
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
                                 
                                 
                                 )
    
    return outstr



if __name__ == '__main__':
   porto = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=porto)