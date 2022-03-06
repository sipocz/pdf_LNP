#from asyncio.windows_events import NULL
from flask import Flask, send_from_directory, send_file
from flask import render_template_string
from flask import render_template,request
from werkzeug.utils import secure_filename
from gensim.models import Doc2Vec
import pymongo
from collections import Counter
import json
import os

from os import getenv
import platform
import requests


app = Flask(__name__,static_folder="static")

os_str=platform.platform()
if "Windows" in os_str:
    _OS_="windows"
else:
    _OS_="linux"




#--------------------------------------------------
#  GLOBAL CONSTANTS
#--------------------------------------------------





if _OS_== "windows":
    _AI_Search_Engine_="http://192.168.2.6:5001/query/"
    _mongo_conn_=f"mongodb+srv://{getenv('mongo_usr')}:{getenv('mongo_pwd')}@cluster0.fuant.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
else:
    _AI_Search_Engine_="http://192.168.2.6:5001/query/"
    
#--------------------------------------------------




def statistic(inp:list,best_n=3):
    fname_list=[ i["fname"] for i in inp]
    cc=Counter(fname_list)
    return cc.most_common(best_n)




def get_mongo_fileurl(fname:str):
    '''
    MONGODB adatbázisból filename alapján url visszaadása
    '''
    # print("Mongo_start")
    _PDF_DB_="PDF_DB"
    _FILE_LOCATION_COLLECTION_="ABB_file_location"
    client = pymongo.MongoClient(_mongo_conn_)
    mydb = client[_PDF_DB_]
    col=mydb[_FILE_LOCATION_COLLECTION_]


    cursor=col.find({"fname":fname})
    out_list=[]
    for out in cursor:
        out_list.append(out)
    #print("Mongo end")
    return(out_list)

#print("**** MONGODB  ****")  # DEBUG
#print(get_mongo_fileurl("3BSE041434-600_A_en_System_800xA_6.0_System_Guide_Technical_Data_and_Configuration")) # DEBUG


def path_splitter(url):
    '''
    url-t felbontja fájlnévre és az elérési út többi részére
    '''
    import pathlib
    split_up = url.split("/")
    out=[i+"/" for i in split_up[:-1]  ]
    out="".join(out) 
    return(out)


@app.route('/')
def root():
    outstr=render_template("login.html")
                                 
    return outstr


@app.route('/download/<fname>')
def download(fname):
    '''
    ez a kód fut, ha rányomunk egy fájl url-re. 
    '''
    
    #print("-------------- DOWNLOAD --------------")
    #print(f"fname:{fname}")
    
    #print(f"PATH:{app.instance_path}")
    ret=get_mongo_fileurl(fname)
    #print(ret)
    url=ret[0]["url"]
    directory=path_splitter(url)
    #print(f"directory:{directory}")
    return send_file(directory+fname+".pdf",as_attachment=False)



@app.route('/query_str', methods=['POST'])
def query2():
    '''
    A keresőszavak alapján csatlakozik AI_Search_Engine-hez
    

    '''


    _query=request.form["query_str"]
    print(_query) #DEBUG
    
    AI_Search_Engine_URL=_AI_Search_Engine_+_query
    print(AI_Search_Engine_URL) #DEBUG
    req = requests.get(AI_Search_Engine_URL)
    # print(type(req)) #DEBUG
    processed_text = req.text

    # print(type(processed_text))#DEBUG

    print(processed_text)
    json_string=processed_text
    req_dict=json.loads(json_string)


    # print("------- REQ_DICT -----") #DEBUG
    # print(req_dict) #DEBUG
    # print("______________") #DEBUG
    req_list=list(req_dict.values())



    #print("++++++ REQ_ LIST +++++++++") #DEBUG
    #print(req_list) #DEBUG
    # megkeressük a fájlok elérési útvonalát
    # itt nem is kell, mert majd megkeressük a donload előtt
    #for req_list_item in req_list:
    #    req_list_item["url"]=get_mongo_fileurl(req_list_item["fname"])[0]["url"]

    #print("------ REQ LIST -----") #DEBUG
    #print(req_list)  #DEBUG

    # A három legtöbbször előforduló fájl megkeresése a találati listából
    # nem biztos, hogy ez lesz a legjobb találat!  
    best_3=statistic(req_list)
    #print("******************") #DEBUG
    
    # print(best_3) #DEBUG



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
                                 _query=None,
                                 
                                 
                                 )
    
    return outstr



if __name__ == '__main__':
   porto = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=porto)