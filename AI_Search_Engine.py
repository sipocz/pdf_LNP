# %%
# AI search engine 
#Dev by S.L.
# -------------
# 2022.02.13.
# -------------

# Dependencies:
# platform
# gensim


# %%
import platform
from gensim.models import Doc2Vec
import pymongo


# %%
import os
from os import getenv
_mongo_conn_=f"mongodb+srv://{getenv('mongo_usr')}:{getenv('mongo_pwd')}@cluster0.fuant.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


# %%

os_str=platform.platform()
if "Windows" in os_str:
    _OS_="windows"
else:
    _OS_="linux"

# %%
if _OS_== "linux":
    _modelpath_="/home/opc/nlp_root/brain/"
    _model_name_="ABB_Doc_220312_1_brain.model"  
else:
    
    _modelpath_="D:/brain/"
    _model_name_="ABB_Doc_220312_1_brain.model"


# %%
mongo_client = pymongo.MongoClient(_mongo_conn_)
mongo_db = mongo_client.test
_MONGODB_="PDF_DB"
_MONGOCOLL_="ABB_pdf"
mongo_db = mongo_client[_MONGODB_]
mongo_col=mongo_db[_MONGOCOLL_]

mongo_col.create_index("index")

# %%
doc_model=None

# %%
doc_model=Doc2Vec.load(_modelpath_+_model_name_)

# %%
def AI_searching(search_text:str, topn:int=20):
    search_text=search_text.lower()
    search_list=search_text.split(" ")
    # print(f"input vector:  {search_list}") #DEBUG
    model1=doc_model.infer_vector(search_list,epochs=4220)
    ans=doc_model.dv.similar_by_vector(model1,topn=topn)
    # debug
    # print(ans)
    #for i in range(topn):
    #    print(f"{i:2}-->similarity:{ans[i][1]*100:3.3} --> index: {ans[i][0]}")
    # end debug
    return(ans)


# %%
def get_pos_info(indexlist:list):
    out=[]
    for actual_index in indexlist:
        cursor=mongo_col.find({"index":actual_index})
        for element in cursor:
            out.append(element)
            #print(element) #DEBUG
    return(out)
            

# %%
def print_document_name(result,ans):
    out={}
    #print("----result----")
    #print(result)
    for i,result_index in enumerate(result):
        strout=f"{i:3} .. {ans[i][1]*100:3.3}% .. {result_index['fname']+'.pdf':120} .. page:{result_index['page']:4}"
        #print(strout) #debug
        id=result_index['_id']
        #print(id)  #DEBUG
        out[int(i)]={ "id":str(id),"percent":round(ans[i][1]*100,1), "fname":result_index['fname'], "page":result_index['page'],"pos0":int(result_index['pos0']),"pos1":int(result_index['pos1']),"pos2":int(result_index['pos2']),"pos3":int(result_index['pos3'])}
    return(out)   

# %%
def _query(search_text:str, topn=40):
    search_list=search_text.lower().split(" ")
    model1=doc_model.infer_vector(search_list,epochs=1288)
    ans=doc_model.dv.similar_by_vector(model1,topn=topn)
    #print("-------------------------") #DEBUG
    #print(f"search: {search_list} , ANS: {ans}") #DEBUG
    indexes=[ans[i][0] for i,_ in enumerate(ans)]
    result_list=get_pos_info(indexes)
    result=print_document_name( result_list,ans)
    return(result,result_list) 
    

# %%
from flask import Flask
app = Flask(__name__)


@app.route('/query/<search_text>')
def query(search_text):
    # print(search_text) #DEBUG
    result,result_list=_query(search_text, topn=50)
    return result



@app.route('/')
def root():
    return 'Hello, World!'

# %%

if __name__ == '__main__':
   porto = int(os.environ.get("PORT", 5001))
   app.run(host="0.0.0.0", port=porto)


