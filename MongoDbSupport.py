class MongoDbSupport:
    
    def __init__(self,connection_str:str):
        
        self._connection_str_=connection_str
        self.dms=False
        self.connected=False  

# -----------------------------------

    def count(self,coll:str) -> int:
        mydb = self.mydb    #DB 
        col=mydb[coll]      #Collection
        return col.count_documents({})

# -----------------------------------

    def connect(self,db) -> None:
        from pymongo import MongoClient
        
        '''
        Adatbázis kapcsolódás
        '''
        if not self.connected:
            self.client = MongoClient(self._connection_str_)
            
            self.mydb = self.client[db]   #DB 
            self.connected=True
            return
        else:
             print("Connected!!")

# -----------------------------------

    def disconnect(self) -> None:
        from pymongo import MongoClient
        '''
        zárja a kapcsolatokat
        '''
        if self.connected:            
            self.client.close()
            self.mydb=None
            self.connected=False
        else:
            print("Disconnected")
        
# -----------------------------------

    def to_csv(self,coll:str,fname:str):
        
        '''
        MONGODB adatbázisból id alapján data visszaadása
        '''
        # print("Mongo_start")
        if self.dms:
            print("to_csv")
        import pymongo
        import pandas as pd
    
        mydb = self.mydb    #DB 
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

# -----------------------------------

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

# -----------------------------------

    def upload_from_csv(self,db:str,coll:str,fname:str):
        
        '''
        MONGODB adatbázisba collection feltöltése fname csv-ből
        Még nincs átírva
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

# -----------------------------------

    def debug_mode(self,value:bool=True):
        '''
        Az osztályt debug üzemmódba teszi.(default=True) Több kiírás jelenik neg a kimeneten 
            ha bemeneti értéke False: a debug móde kikapcsolásra kerül
            az osztály létrehozásakor a debug mód ki van kapcsolva 
        '''
        self.dms=value #Debug_mode_state

# -----------------------------------
    
    def regenerate_from_csv(self,db:str,coll:str,fname:str):
        
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

# -----------------------------------

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
    mc.connect(_PDF_DB_)
    print(mc.count(_FILE_LOCATION_COLLECTION_))
    mc.to_csv(_META_INFO_,"E:/Backup/20220508/Mongodb_pdf_file_location.csv")

    print(mc.connected)
    
    mc.disconnect()
    print(mc.connected)
    
    




    #mc.to_csv(_PDF_DB_,_FILE_LOCATION_COLLECTION_,"E:/Backup/20220508/pdf_file_location.csv")
    #mc.to_csv(_PDF_DB_,_META_INFO_,"E:/Backup/20220508/pdf_metadata.csv")
    #mc.kill_collection(_PDF_DB_,_FILE_LOCATION_COLLECTION_)
    #mc.upload_from_csv(_PDF_DB_,_FILE_LOCATION_COLLECTION_,"d:/Backup/20220305/pdf_file_location.csv")
    
    #mc.kill_collection(_PDF_DB_,_META_INFO_)
    #mc.upload_from_csv(_PDF_DB_,_META_INFO_,"d:/corpus/_META_ABB_sentences_20220313_233000.txt")

    #mc.regenerate_from_csv(_PDF_DB_,_META_INFO_,"d:/Backup/20220305/p")
    '''
    fname="d:/Backup/20220305/pdf_metadata.csv"
    import pandas as pd
    df=pd.read_csv(fname)
    df=df.astype({"pos0":"int32","pos1":"int32","pos2":"int32","pos3":"int32"})

    print(df.head())
    df.to_csv("d:/Backup/20220312/pdf_metadata.csv",index=False)
    '''
    