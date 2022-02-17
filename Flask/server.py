from flask import Flask
from flask import render_template_string
from flask import render_template,request
from werkzeug.utils import secure_filename
from gensim.models import Doc2Vec
import pymongo


import os
app = Flask(__name__)

import requests



output=['  0 .. 93.4% .. 3BSE078160 en R ABB Ability System 800xA 6.0.3.3 Product Catalog.pdf                                                     .. page:  53',
 '  1 .. 89.1% .. 3BSE035982-610_A_en_Control_AC_800M_Communication_Protocols.pdf                                                          .. page: 206',
 '  2 .. 88.8% .. 3BSE035981-600_A_en_System 800xA_Control_6.0_AC_800M_Binary_and_Analog_Handling.pdf                                      .. page:   5',
 '  3 .. 88.7% .. 3BSE035981-600_en_System 800xA_Control_6.0_AC_800M_Binary_and_Analog_Handling.pdf                                        .. page:   5',
 '  4 .. 88.5% .. 3BSE035981-600_en_System 800xA_Control_6.0_AC_800M_Binary_and_Analog_Handling.pdf                                        .. page:  78',
 '  5 .. 88.5% .. 3BSE038018-600_en_System_800xA_6.0_System_Guide_Functional_Description.pdf                                               .. page: 149',
 '  6 .. 88.2% .. 3BSE041488-511_-_en_Compact_Control_Builder_AC_800M_5.1.1_Binary_and_Analog_Handling.pdf                                 .. page:   5',
 '  7 .. 88.1% .. 3BSE025251-600_en_S800_I_O_CI840_Memory_Maps.pdf                                                                         .. page: 197',
 '  8 .. 88.0% .. 3BSE038018-510_H_en_System_800xA_5.1_System_Guide_Functional_Description.pdf                                             .. page: 172',
 '  9 .. 87.9% .. 2PAA112277-603_en_System_800xA_6.0_Release_Notes_Resolved_Issues.pdf                                                     .. page: 165',
 ' 10 .. 87.9% .. 3BSE035981-510_A_en_System_800xA_Control_5.1_AC_800M_Binary_and_Analog.pdf                                               .. page:  83',
 ' 11 .. 87.9% .. 3BDD013138R0001_-_en_System_800xA__AC_870P_-_Local_I_O.pdf                                                               .. page:   2',
 ' 12 .. 87.8% .. 3BSE082729_B_en_Select_IO_FCI_Ethernet.pdf                                                                               .. page:  62',
 ' 13 .. 87.8% .. 3BSE041488-600_A_en_Compact_Control_Builder_AC_800M_6.0_Binary_and_Analog_Handling.pdf                                   .. page:  58',
 ' 14 .. 87.7% .. 2PAA114363-510_B_en_System_800xA_5.1_RevE_Release_Notes_New_Functions_and_Known_Problems.pdf                             .. page: 147',
 ' 15 .. 87.7% .. 3BSE036959-600_en_S800_I_O_CI801_Memory_Maps.pdf                                                                         .. page: 181',
 ' 16 .. 87.7% .. 3BSE035981-510_A_en_System_800xA_Control_5.1_AC_800M_Binary_and_Analog.pdf                                               .. page:   6',
 ' 17 .. 87.7% .. 3BSE038018-510_H_en_System_800xA_5.1_System_Guide_Functional_Description.pdf                                             .. page:  16',
 ' 18 .. 87.6% .. 3BSE041488-511_-_en_Compact_Control_Builder_AC_800M_5.1.1_Binary_and_Analog_Handling.pdf                                 .. page:  55',
 ' 19 .. 87.6% .. ABB UNIVERSITY INDIA Course Catalog.pdf                                                                                  .. page:   3']

print(output[0])

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
                                 _query=output
                                 )
    
    return outstr











if __name__ == '__main__':
   porto = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=porto)