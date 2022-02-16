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



@app.route('/')
def hello_world():
    outstr=render_template("login.html")
                                 
    return outstr


@app.route('/query', methods=['POST'])
def query():
    user = request.form['username']
    pwd = request.form['password']
    
    
    processed_text = user+pwd
    outstr=" Hibás azonosítás !!!"
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