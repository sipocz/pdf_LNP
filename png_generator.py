# %%
# pip
# !pip install Pillow 


from PIL import Image
from PIL import ImageDraw
import pymongo
from bson.objectid import ObjectId
import fitz as pymupdf
import platform
import os
from os import getenv


# %%


_mongo_conn_=f"mongodb+srv://{getenv('mongo_usr')}:{getenv('mongo_pwd')}@cluster0.fuant.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# %%

os_str=platform.platform()
if "Windows" in os_str:
    _OS_="windows"
else:
    _OS_="linux"




#---------------------------------------------------#
#  GLOBAL CONSTANTS                                 #
#---------------------------------------------------#



_PDF_DB_="PDF_DB"
_FILE_LOCATION_COLLECTION_="ABB_file_location"
_SENTENCE_LOCATION_COLLECTION_="ABB_pdf"


if _OS_== "windows":
    _AI_Search_Engine_="http://192.168.2.6:5001/query/"
    _mongo_conn_=f"mongodb+srv://{getenv('mongo_usr')}:{getenv('mongo_pwd')}@cluster0.fuant.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    _OUTFILE_PATH_="D:/ABB/png/"
    _DOC_ROOT_="D:/"
else:
    _AI_Search_Engine_="http://10.0.0.214:5001/query/"
    _OUTFILE_PATH_="/home/opc/nlp_root/doc/ABB/png/"
    _DOC_ROOT_="/home/opc/nlp_root/doc/"
#--------------------------------------------------




# %%

def get_mongo_selection_data(id):
    '''
    MONGODB adatbázisból id alapján data visszaadása
    '''
    # print("Mongo_start")

    client = pymongo.MongoClient(_mongo_conn_)
    print(_mongo_conn_) #DEBUG
    mydb = client[_PDF_DB_]
    col=mydb[_SENTENCE_LOCATION_COLLECTION_]


    cursor=col.find_one({"_id":id})
    print("** get_mongo_selection_data Cursor:",cursor) #DEBUG
    return(cursor)


# %%
def get_mongo_fileurl(fname:str):
    '''
    *** TASK: PNG OUTPUT
    
    MONGODB adatbázisból filename alapján url visszaadása
    '''
    # print("Mongo_start")
    client = pymongo.MongoClient(_mongo_conn_)
    mydb = client[_PDF_DB_]
    col=mydb[_FILE_LOCATION_COLLECTION_]


    cursor=col.find({"fname":fname})
    out_list=[]
    for out in cursor:
        out_list.append(out)
    #print("Mongo end")
    return(out_list)


# %%
def fname_separator(fname):
    '''
    *** TASK: PNG OUTPUT
    input: fname egy fájl neve
    return: megadott fname file könyvtára, fole neve, és kiterjesztése  
    '''
    import os
    temp = os.path.splitext(fname)
    out = (os.path.dirname(fname),os.path.basename(temp[0]), temp[1])
    
    return(out)

# %%
def text_drawer(fname,rmatrix,delta=2, index=None):
    '''
    *** TASK : PNG OUTPUT  
    desc: fname png file-ban rmatrix alapján index pozícióban lévő elemet kiemeli delta vastag kerettel
    
    fname:png file neve 
    rmatrix: keretsruktura
    delta: a keret vastagsága
    index: melyik elemet kell kiemelni 


    '''
    
    png_fname=str(rmatrix["_id"])+".png"
    # png generalas
    # print(rmatrix) #DEBUG

    page_number=rmatrix["page"]
    f = pymupdf.open(fname)
    page=f.load_page(page_number)
    page_pix=page.get_pixmap()
    page_pix.save(_OUTFILE_PATH_+png_fname)
    
    _file_name_expander_="_rect"

    
    inner_gap=3
    (xdir,xfname,xext)=fname_separator(png_fname)
    outfname=xdir+xfname+_file_name_expander_+xext
    # print(f'file name:',png_fname) #DEBUG
    img=Image.open(_OUTFILE_PATH_+png_fname)
    Drawer = ImageDraw.Draw(img)
    x1=rmatrix["pos0"]
    y1=rmatrix["pos1"]
    x2=rmatrix["pos2"]
    y2=rmatrix["pos3"]
    Drawer.rectangle((x1-delta-inner_gap, y1-delta-inner_gap, x2+delta+inner_gap, y2+delta+inner_gap), outline="green",width=5,)
    img.save(_OUTFILE_PATH_+outfname)
    
    # print("Text_drawer:",_OUTFILE_PATH_+outfname) #DEBUG
    return(_OUTFILE_PATH_+outfname)

# %%
def xpng(search_text):
    print("search text:",search_text ) #DEBUG
    mongo_sentence_pos=get_mongo_selection_data(int(search_text))
    print("mongo_sentence_pos:",mongo_sentence_pos) # DEBUG
    file_data=get_mongo_fileurl(mongo_sentence_pos["fname"])
    #print ("file_data=",file_data) #DEBUG
    file_name=file_data[0]["url"]
    #print("file_name=",file_name)
    if file_name[1]==":":   #a windows D:blabla még benne van a file nevében!!
        file_name=_DOC_ROOT_+file_name[3:]
    out=text_drawer(file_name,mongo_sentence_pos)    


    return (out)

# %%
from flask import Flask, send_file


app = Flask(__name__)

@app.route('/png/<search_text>')
def query(search_text):
    print("search_text:",search_text) #DEBUG
    fname=xpng(search_text)
    
    #print(f"fileName:{fname}") #DEBUG

    
    return send_file(fname,as_attachment=False)




@app.route('/')
def root():
    return 'Hello, World!'

# %%

if __name__ == '__main__':
   porto = int(os.environ.get("PORT", 5002))
   app.run(host="0.0.0.0", port=porto)

# %%



