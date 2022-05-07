# %%
import mariadb
from os import getenv

# %%
from pandas import DataFrame

# %%
class MariaDbSupport:
    
    def __init__(self,user,pwd,host,database,port=3306):
        
        self.user=user
        self.pwd=pwd
        self.host=host
        self.database=database
        self.port=port
        self.dms=False
        self.connected=False



    def count(self,table):
        '''
        Megadott tábla méretét adja vissza
        '''
        self.cur.execute("SELECT count(*) from " + table)
        o=self.cur.next()
        return o[0]



    def debug_mode(self,value:bool=True):
        '''
        Az osztályt debug üzemmódba teszi.(default=True) Több kiírás jelenik neg a kimeneten 
            ha bemeneti értéke False: a debug móde kikapcsolásra kerül
            az osztály létrehozásakor a debug mód ki van kapcsolva 
        '''
        self.dms=value #Debug_mode_state



    def connect(self,db):
        '''
        Adatbázis kapcsolódás
        '''
        if not self.connected:
            self.conn=mariadb.connect(user=self.user,password=self.pwd,host=self.host,port=self.port,database=db)
            self.cur=self.conn.cursor()
            self.connected=True
        else:
            print("Conencted!!")



    def disconnect(self):
        '''
        zárja a kapcsoaltokat
        '''
        if self.connected:
            self.cur.close()
            self.conn.close()
            self.connected=False
        else:
            print("disconencted")



    def to_csv(self,table:str,fname:str):
        import pandas as pd
        
        '''
        MARIADB adatbázis táblából adatok mentése csvbe
        '''
        
        # print("Mongo_start")
        
        if self.dms:
            print("to_csv")
        
        self.cur.execute("SELECT * from "+table)
        description=self.cur.description
        cols=[i[0] for i in  description]


        df  = pd.DataFrame(self.cur)
        df.columns=cols
        if self.dms:
            print(df.head())
        df.to_csv(fname,index=False)
        df=None
        if self.dms:
            print("to_csv exit")
        return        



    
    def upload_from_csv(self,table:str,fname:str,init=False):
        
        '''
        MARIADB  adatbázis táblába collection feltöltése fname csv-ből
        '''
        from  pandas import DataFrame 
        
        
        
        if self.dms:
            print("Upload_start")
        
        if not self.connected:
            print("Not Connected!")
            return
        
        if init:
            self.cur.execute("delete from " + table )
            self.conn.commit()
            
            if self.dms:
                print("Init")


        df=pd.read_csv(fname)
        if self.dms:
            print(df.head())

        
        self.cur.execute("SELECT * from "+table)

        description=self.cur.description
        cols=[i[0] for i in  description]
        cols_str=str(cols).replace("'","")
        cols_str=str(cols_str).replace("[","(").replace("]",")")
        
        if self.dms:
            print(cols_str)

        list_of_dict=df.to_dict('records')

        for i,element in enumerate(list_of_dict):
            
            o=str(list(element.values())).replace("[","(").replace("]",")")
            sql_cmd=f"INSERT INTO {table} {cols_str} VALUES "+o
            if self.dms:
                print(sql_cmd)
            self.cur.execute(sql_cmd)
            if i % 10000==0:
                self.conn.commit()
                if self.dms:
                    print(i, end="_ _")
        self.conn.commit()    
            
        

        

# %%
if __name__=="__main__":
    pass
    #maria_usr=getenv('maria_nlp_user')
    #maria_pwd=getenv('maria_nlp_pwd')
    #maria_host="217.144.54.147"
    #database="NLP_ABB"
    #table="ABB_file_location"
    #csvData="E:/Backup/20220506/pdf_file_location.csv"
    #toARCH="E:/Backup/20220506/MARIADB_pdf_file_location.csv"


    #mdb=MariaDbSupport(maria_usr,maria_pwd,maria_host,database)
    
    #mdb.connect(database)
    #mdb.debug_mode()
    #mdb.upload_from_csv(table,csvData,init=True)
    #mdb.disconnect()
    
    #mdb.connect(database)
    #mdb.debug_mode()
    #mdb.to_csv(table,toARCH)
    #mdb.disconnect()
    #table="ABB_pdf"
    #toARCH="E:/Backup/20220506/MARIADB_pdf_metadata.csv"
    #mdb.connect(database)
    #mdb.debug_mode()
    #mdb.to_csv(table,toARCH)
    #mdb.disconnect()

    #table="ABB_pdf"
    #csvData="E:/Backup/20220506/pdf_metadata.csv"
    #mdb.connect(database)
    #mdb.debug_mode(False)

    '''
    #upload from csv
    mdb.upload_from_csv(table,csvData,init=True)
    '''
    #print(mdb.count(table))
    #mdb.to_csv(table,"E:/Backup/20220506/MARIADB_pdf_metadata.csv")

    #mdb.disconnect()








