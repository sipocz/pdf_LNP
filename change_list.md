# 20220207
## Related: ABB_sentences_NLP.ipynb
    - sentence corpus előállítása
    - Doc2vec teszt

# 20220208
## Related: ABB_sentences_NLP.ipynb
    - Doc2vec similarity próba


# 20220210
## Related: ABB_sentences_NLP.ipynb
    - Doc2vec similarity próba 2. 
    - Doc2Vec(corpus_file=sentence_corpus_file,vector_size=200,epochs=60,dm=0)  dm=0 meglepően jó eredmények, még rövid keresőszavak esetén is

# 20220210 20:33
## Related: ABB_sentences_NLP.ipynb,mongotest.ipynb
    - Doc2vec similarity próba 3. 
    - File metadata összegyűjtés majd adatbázis építés
    - Mongodb test 4M record ingyenesen elérhető
    - speedtest 20db lekérdezés 15sec


# 20220211 19:03
## Related: Corpus_generator.ipynb 
    - corpus generator: metainfo kinyerés
    - block alapú megközelítés --> rövid mondatokat eredményez! Nem jó, mert elveszik a kontextus. kombinálni kell a metainfó adatokkal (rectangle maximalization :-)

# 20220212 10:33
## Related: ABB_sentences_NLP.ipynp
    - model mentés, visszatöltés -> a model tanítása és a felhasználása különválasztható
    - git problémák eliminálása
    - rectangle maximalization design
