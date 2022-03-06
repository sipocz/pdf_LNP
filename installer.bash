# working directory creaton
mkdir /home/opc/nlp_root

# install environment
sudo yum install python3.8
sudo yum install virtualenv

#create environment
virtualenv -p /usr/bin/python3.8 /home/opc/nlp_root


cd /nlp_root
source /home/opt/nlp_root/bin/activate
python -m pip install pymongo
python -m pip install gensim
python -m pip install flask
