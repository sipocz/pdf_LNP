class MongoDbSupport:
    
    def __init__(self,connection_str:str):
        
        self._connection_str_=connection_str
        self.dms=False  


    def to_csv(self,db:str,coll:str,fname:str):
        
        '''
        MONGODB adatbázisból id alapján data visszaadása
        '''
        # print("Mongo_start")
        if self.dms:
            print("to_csv")
        import pymongo
        import pandas as pd
    
        client = pymongo.MongoClient(self._connection_str_)
        mydb = client[db]   #DB 
        col=mydb[coll]      #Collection

        cursor=col.find()
            
        cursor_list=list(cursor)

        df  = pd.DataFrame(cursor_list)
        #print(df.head())
        df.to_csv(fname,index=False)
        df=None
        if self.dms:
            print("to_csv exit")
        return(col)

    def kill_collection(self,db:str,coll:str):
        
        '''
        MONGODB adatbázis collection törlése
        '''
        if self.dms:
            print("Mongo_kill_collection ")
        import pymongo
        import pandas as pd
    
        client = pymongo.MongoClient(self._connection_str_)
        mydb = client[db]   #DB 
        col=mydb[coll]      #Collection
        col.drop()

        return(col)


    def upload_from_csv(self,db:str,coll:str,fname:str):
        
        '''
        MONGODB adatbázisba collection feltöltése fname csv-ből
        '''
        if self.dms:
            print("Upload_start")
        import pymongo
        import pandas as pd
    
        client = pymongo.MongoClient(self._connection_str_)
        mydb = client[db]   #DB 
        col=mydb[coll]      #Collection
        #print(df.head())
        df=pd.read_csv(fname)
        if self.dms:
            print(df.head())
        list_of_dict=df.to_dict('records')
        col.insert_many(list_of_dict)
        if self.dms:
            print("exit upload")
        return(col)

    def debug_mode(self,value:bool=True):
        '''
        Az osztályt debug üzemmódba teszi.(default=True) Több kiírás jelenik neg a kimeneten 
            ha bemeneti értéke False: a debug móde kikapcsolásra kerül
            az osztály létrehozásakor a debug mód ki van kapcsolva 
        '''
        self.dms=value #Debug_mode_state






if __name__=="__main__":
    from os import getenv
    _mongo_conn_=f"mongodb+srv://{getenv('mongo_usr')}:{getenv('mongo_pwd')}@cluster0.fuant.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

    _PDF_DB_="PDF_DB"
    _FILE_LOCATION_COLLECTION_="ABB_file_location"
    _META_INFO_="ABB_pdf"


    from os import getenv

    _mongo_conn_=f"mongodb+srv://{getenv('mongo_usr')}:{getenv('mongo_pwd')}@cluster0.fuant.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

    mc=MongoDbSupport(_mongo_conn_)
    mc.debug_mode()
    #mc.to_csv(_PDF_DB_,_FILE_LOCATION_COLLECTION_,"d:/Backup/20220305/pdf_file_location.csv")
    #mc.to_csv(_PDF_DB_,_META_INFO_,"d:/Backup/20220305/pdf_metadata.csv")
    mc.kill_collection(_PDF_DB_,_FILE_LOCATION_COLLECTION_)
    mc.upload_from_csv(_PDF_DB_,_FILE_LOCATION_COLLECTION_,"d:/Backup/20220305/pdf_file_location.csv")
    