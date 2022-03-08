#!/bin/bash
# run_png_generator.sh
echo "hello PNG generator"
cd /home/opc/nlp_root
source ./bin/activate
python --version
cd /home/opc/git/pdf_NLP

export mongo_usr=pdfaidata
export mongo_pwd=***********

python png_generator.py


--------------------------

#!/bin/bash
# run_ai_search_engine.sh
echo "hello AI Search Engine"
cd /home/opc/nlp_root
source ./bin/activate
python --version
cd /home/opc/git/pdf_NLP

export mongo_usr=pdfaidata
export mongo_pwd=***********

python AI_Search_Engine.py

----------------------------


#!/bin/bash
echo "hello python"
cd /home/opc/nlp_root
source ./bin/activate
python --version
cd /home/opc/git/pdf_NLP/Flask

export mongo_usr=pdfaidata
export mongo_pwd=************

python server.py












