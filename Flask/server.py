from flask import Flask
from flask import render_template_string
from flask import render_template,request
from werkzeug.utils import secure_filename



import os
app = Flask(__name__)

import requests
from bs4 import  BeautifulSoup
app.logger.error('testing error log')
app.logger.info('testing info log')
app.config['UPLOAD_FOLDER']="./upload"

def ansicode(sti):
    outstr=""
    for i in sti:
        a=i
        if i=="á":
            a="a"
        if i=="Á":
            a="A"
        if i=="é":
            a="e"
        if i=="É":
            a="E"
        if i=="í":
            a="I"
        if i=="Í":
            a="I"
        if i=="ö":
            a="o"
        if i=="Ö":
            a="O"
        if i=="ő":
            a="o"
        if i=="Ő":
            a="O"
        if i=="ó":
            a="o"
        if i=="Ó":
            a="O"
        if i=="ü":
            a="u"
        if i=="Ü":
            a="u"
        if i=="ú":
            a="u"
        if i=="Ú":
            a="u"
        outstr=outstr+a
    return(outstr)








    























#render_template_string(html_template,ingatlan_com=ingatlan_com_table)

@app.route('/AI')

def getcity(city="bb"):
   outstr=render_template("html_template_city.html",
                                 city_name=city.capitalize(),
                                 ingatlanCom=ingatlan_com_querycity(city),
                                 ingatlantajolo=ingatlantajolo_querycity(city),
                                 ingatlannet=ingatlannet_querycity(city))
   outstr="Hello1"
   return outstr

@app.route('/arxiv/<query>')

def getarxiv(query="python"):
   outstr=render_template("html_template_arxiv.html",
                                 query_in=query,
                                 arxiv_in=arxiv_pages(query)
                                 )
                                 
   #print(outstr)
   return outstr

@app.route('/crypto')

def getcrypto(ticker=""):
    
   outstr=render_template("html_template_crypto.html",
                                 query_in=ticker,
                                 crypto_in=getallcoin()
                                 )
                                 
   #print(outstr)
   return outstr







@app.route('/')
def hello_world():
    outstr=render_template("login.html")
                                 
    return outstr

@app.route('/query', methods=['POST'])
def query():
    user = request.form['username']
    pwd = request.form['password']
    
    
    processed_text = user+pwd
    outstr=" ---------  ------------ INVALID"
    if processed_text=="aaa":
        outstr=render_template("query.html",
                                 #query_in=processed_text,
                                 #arxiv_in=arxiv_pages(processed_text.replace(" ","+"))
                                 )
    
    return outstr




@app.route('/BW_Colorizer', methods=['GET'])
def bwcolorizer():
    
    outstr=render_template("html_template_BWColorizer.html",
                                 
                                 )
    return outstr

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      fname="./upload"+"/"+f.filename
      fname2="./static/img/"+f.filename  

      f.save(fname2)
      outstr=render_template("html_template_BWColorizer_work.html",
                                 path2=fname2,
                                 )

      
      return outstr

@app.route('/cryptoprice')
def crypto_price():
    coins=["ETH","LTC","BTC"]
    outstr=""
    for coin in coins:
        urlstr=f"https://api.coinbase.com/v2/prices/{coin}-USD/spot"
        
        api=requests.get(urlstr)
        fback=api.json()
        price=fback["data"]["amount"]
        print (api.text)
        outstr+=f"--{coin}:{price}--"
    
    
      
    return outstr





@app.route('/login', methods = ['GET', 'POST'])
def login():
      outstr=render_template("html_google_login.html",
                                 
                                 )

      
      return outstr






if __name__ == '__main__':
   porto = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=porto)