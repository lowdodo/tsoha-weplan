# tsoha-weplan
tietokannat ja web ohjelmointi kurssi 2023 


**Weþlan - joukon yhteinen suunnittelualusta**

Sovelluksessa on tarkoitus pystyä yhdessä jollain porukalla, esim. ainejärjestö, kaveriporukka tai kämppikset, suunnitella yhteisiä tapahtumia/juhlia/tai vaikka viikkosiivousta. Muiden prosessin näkeminen on tarkoitus olla kilpailuhenkinen lisäys suunnitelmaan, ja ehkä myöhemmin lisätä ulkoasussa siihen pelimäisiä piirteitä (hahmoja???)

**Käynnistysohjeet**
loonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

DATABASE_URL= "postgresql:///lowdodo"
SECRET_KEY="f3ea2ebfbd91ed3df061f4c56bf9645c"
Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
Määritä vielä tietokannan skeema komennolla

$ psql < tables.sql HUOM minulla ei lue schema
Nyt voit käynnistää sovelluksen komennolla

$ flask run

Voi olla, että joudut muuttamaan joidenkin tietokantojen nimiä, esim. users on helposti sama, kuin joillain muilla. Katso tähän ohjeet meilistä tai vertaisarvioinnin ohjeet moocista! 



Sovelluksen ominaisuuksia: 

- käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- käyttäjä näkee tilaston kaikkien käyttäjien viikon yhteenlasketut aktiivisuuspisteet, listan yhteisistä suunnitelmista, ja voi liittyä suunnittelualueelle.
- käyttäjä voi lukea ja lisätä suunnittelualueella osasuunnitelmia, merkata osasuunnitelmia tehdyksi sekä nähdä tilaston muiden (ja omansa) käyttäjien edistymisen sillä suunnittelualueella.
- kuka vain käyttäjä voi saada osallisen ylläpitäjyyden luomalla uuden suunnitelman, tällöin hän on ylläpitäjä tälle suunnittelualueelle.
- osaylläpitäjä pystyy hylkäämään suunnittelualueeltaan osasuunnitelmia, lisäämään tekstimateriaalia kuten kuvauksia, poistamaan käyttäjiä suunnitelmasta ja tekemään kaikkea mitä käyttäjäkin.
- osaylläpitäjä voi lisätä toisille ylläpitäjyysoikeuksia niin, että käyttäjästä tulee osaylläpitäjä samalle suunnittelualueelle. 
- pääylläpitäjä: kaiken kuratoija, pääsee käsiksi kaikkiin käyttäjiin ja suunnitelmiin ja muokata asiatonta sisältöä

  


**Viikko 2**
- luotiin kirjautuminen, rekisteröityminen ja logout. Testattu luomalla käytättäjä Testikäyttäjä ss: 1234 jolla kirjauduttiin, poistuttiin ja kirjauduttiin uudestaan
- luotiin etusivu, rekisteröitymissivu, plans sivu ja erilliset sivut suunnitelmille
- tietokannat käyttäjille, suunnitelmille ja alisuunnitelmille, testattu sillä, että käyttäjää pystyi käyttämään, suunnitelmia katsomaan. Alisuunnitelmat eivät toimi vielä.



