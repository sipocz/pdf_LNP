from os import getenv

# globalis konfigurációk itt kezdődnek

_DB_="MariaDB"
_FILE_LOCATION_="ABB_file_location"
_META_INFO_="ABB_pdf"



#-------------------------------------

if _DB_=="MariaDB":

    maria_usr=getenv('maria_nlp_user')
    maria_pwd=getenv('maria_nlp_pwd')
    maria_host="217.144.54.147"
    _PDF_DB_="NLP_ABB"
    table="ABB_pdf"
    table_url="ABB_file_location"

    import MariaDbSupport as db
    mdb=db.MariaDbSupport(maria_usr,maria_pwd,maria_host,_PDF_DB_)
    mdb.connect(_PDF_DB_)
    print(mdb.count(_META_INFO_))
    mdb.disconnect()
elif _DB_=="MongoDB":
    _PDF_DB_="PDF_DB"
    import MongoDbSupport as db
    _mongo_conn_=f"mongodb+srv://{getenv('mongo_usr')}:{getenv('mongo_pwd')}@cluster0.fuant.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


    mc=db.MongoDbSupport(_mongo_conn_)
    print(mc.count(_PDF_DB_,_META_INFO_))
    
