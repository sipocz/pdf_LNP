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
    - speedtest 20db lekérdezés 15sec :-(


# 20220211 19:03
## Related: Corpus_generator.ipynb 
    - corpus generator: metainfo kinyerés
    - block alapú megközelítés --> rövid mondatokat eredményez! Nem jó, mert elveszik a kontextus. kombinálni kell a metainfó adatokkal (rectangle maximalization :-)

# 20220212 10:33
## Related: több 
    - model mentés, visszatöltés -> a model tanítása és a felhasználása különválasztható
    - git problémák eliminálása
    - rectangle maximalization design :-) 
    - mongodb database configuration
    - corpus_generator / all_text_drawer:
        kiválasztott pdf oldalon az eredmény bejelölése OK
    - corpus_generator
        mongodb connection  (teszt a linux-on)
    - basic HTML design
        hibajavítás, szinek, css

# 20220213 10:20
## Related: több
    - Projekt ötletfal felépítése
    - AI_Search_Engine.ipynb készítée
    - AI_learning.ipynb készítése

# 20220214 18:50
## Related: több
    - pdf download
    - index_Redesign.html kialakítása iframe struktura

# 20220216 18:00
## Related: több
    - 
    - FLASK webserver kialakítása


# 20220218 18:00
## Related: több
    - Flask klient-server megoldás
    - FLASK AI_SEARCH_Engine rest API kialakítása
    - (web) Server oldali flask módosítás api hívások beépítésa
 

# 20220219 11:00
## Related: több
    - HTML update
    - css update
    - rest-api
    - keresőmezőben a korábbi keresés megjelenítése
    - best 3 jelenjen meg a listában (a legtöbbször előforduló a keresésben) ez lehet nem a legjobb eredményt adja. :-(
    - icon a HTML oldalon

# 20220220 10:00
## Related: több
    - mongodb kapcsolat kialakítása a fájl url lekérdezése miatt
    - Fájl url ijntegrálása HTML-be
    - Fájl letöltés tesztje, fájl megnyitása
    - Mongodb keresés optimalizálás
    - flask static fájlmegosztás megoldás keresés, fálj küldés a fájlrendszerből    


# 20220221 21:41
## Related: több
    - server oldalra átjön minden infó a AI_search_engine-től
    - id alapján fog keresni a PNG generator
    




