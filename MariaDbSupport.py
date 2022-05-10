# %%
import mariadb
from os import getenv

# %%
from pandas import DataFrame

# %%
class MariaDbSupport:
    '''

    MARIADB interface

    '''


# -----------------------------------
    
    def __init__(self,user,pwd,host,database,port=3306):
        
        self.user=user
        self.pwd=pwd
        self.host=host
        self.database=database
        self.port=port
        self.dms=False
        self.connected=False

# -----------------------------------

    def count(self,table) -> int:
        self.cur.execute("SELECT count(*) from " + table)
        o=self.cur.next()
        return o[0]

# -----------------------------------

    def debug_mode(self,value:bool=True) -> None:
        '''
        Az osztályt debug üzemmódba teszi.(default=True) Több kiírás jelenik neg a kimeneten 
            ha bemeneti értéke False: a debug móde kikapcsolásra kerül
            az osztály létrehozásakor a debug mód ki van kapcsolva 
        '''
        self.dms=value #Debug_mode_state

# -----------------------------------

    def connect(self,db) -> None:
        '''
        Adatbázis kapcsolódás
        '''
        if not self.connected:
            self.conn=mariadb.connect(user=self.user,password=self.pwd,host=self.host,port=self.port,database=db)
            self.cur=self.conn.cursor()
            self.connected=True
        else:
            print("Connected!!")

# -----------------------------------

    def disconnect(self) -> None:
        '''
        zárja a kapcsoaltokat
        '''
        if self.connected:
            self.cur.close()
            self.conn.close()
            self.connected=False
        else:
            print("disconencted")

# -----------------------------------

    def to_csv(self,table:str,fname:str):
        
        from pandas import DataFrame 

        '''
        MARIADB adatbázis táblából adatok mentése csvbe
        '''
        
        # print("Mongo_start")
        
        if self.dms:
            print("to_csv")
        
        self.cur.execute("SELECT * from "+table)
        description=self.cur.description
        cols=[i[0] for i in  description]


        df  = DataFrame(self.cur)
        df.columns=cols
        if self.dms:
            print(df.head())
        df.to_csv(fname,index=False)
        df=None
        if self.dms:
            print("to_csv exit")
        return        

# -----------------------------------
    
    def upload_from_csv(self,table:str,fname:str,init=False):
        
        '''
        MARIADB  adatbázis táblába collection feltöltése fname csv-ből
        '''
        
        from  pandas import DataFrame,read_csv 
        
        
        
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


        df=read_csv(fname)
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

# -----------------------------------
             
    def get_selection(self,table,id):
        '''
        MARIADB adatbázisból id alapján data visszaadása
        '''
        sql_str='SELECT * from '+table+' WHERE _id = "'+id+'"'
        if self.dms:
            print(sql_str)
        self.cur.execute(sql_str)
        out=self.cur.fetchall()
        print(out)
        return(out)
    
# -----------------------------------

    def get_fileurl(self,table:str, fname:str):
        
        '''
        MARIADB adatbázisból fname alapján url visszaadása
        '''

        sql_str='SELECT url from '+table+' WHERE fname = "' +fname+'"'
        self.cur.execute(sql_str)
        out=self.cur.fetchall()
        if self.dms:
            print(sql_str)
            print(out[0][0])
        return(out)


            
        

# %%
if __name__=="__main__":
    
    maria_usr=getenv('maria_nlp_user')
    maria_pwd=getenv('maria_nlp_pwd')
    maria_host="217.144.54.147"
    database="NLP_ABB"
    table="ABB_pdf"
    table_url="ABB_file_location"

    #csvData="E:/Backup/20220506/pdf_file_location.csv"
    #toARCH="E:/Backup/20220506/MARIADB_pdf_file_location.csv"




    mdb=MariaDbSupport(maria_usr,maria_pwd,maria_host,database)
    
    mdb.connect(database)
    mdb.debug_mode()
    sel=mdb.get_selection(table,"12")
    sel=mdb.get_fileurl(table_url,"e81ab01r1110")
    
    mdb.disconnect()
    
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

