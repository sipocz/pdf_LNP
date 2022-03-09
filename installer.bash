# https://cloud.oracle.com/compute/instances?region=eu-frankfurt-1
# IP: 130.61.29.20:5000
# IP: 10.0.0.214


# working directory creation
mkdir /home/opc/nlp_root
cd /home/opc/nlp_root
mkdir brain
cd brain
# download brain files:

wget --user ftpuser@protonix.hu  --password xxxxxxxx ftp://protonix.hu/public_ftp/ABB_Doc_220227_2_brain.model
wget --user ftpuser@protonix.hu  --password xxxxxxxx ftp://protonix.hu/public_ftp/ABB_Doc_220227_2_brain.model.dv.vectors.np
cd /home/opc/nlp_root
mkdir doc
cd doc
wget --user ftpuser@protonix.hu  --password xxxxxxxx ftp://protonix.hu/public_ftp/ABB.zip  # letölti a teljes könyvtárat?
unzip ABB.zip



# install environment
sudo yum install python3.8
sudo yum install virtualenv



#create environment
virtualenv -p /usr/bin/python3.8 /home/opc/nlp_root
cd /home/opc/nlp_root
source bin/activate


cd /nlp_root
source /home/opt/nlp_root/bin/activate
python -m pip install pymongo
python -m pip install gensim
python -m pip install flask
python -m pip install requests
# PNG generator
python3 -m pip install --upgrade Pillow
python -m pip install --upgrade pymupdf


# enable port on firewall
sudo firewall-cmd --add-port=5000/tcp --permanent
sudo firewall-cmd --add-port=5002/tcp --permanent
sudo firewall-cmd --reload

# download application from GIT
cd /home/opc/git/pdf_NLP 
sudo git pull https://github.com/sipocz/pdf_NLP.git





