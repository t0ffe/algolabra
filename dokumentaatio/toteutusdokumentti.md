# Toteutusdokumentti

## Ohjelman yleisrakenne
Ohjelma koostuu useista moduuleista, jotka yhdessä toteuttavat reitinhakualgoritmit `A*` ja `JPS`. Pääkomponentit ovat:
- `pathfinding.py`: Sisältää `A*`-algoritmin ja `JPS`-algoritmin toteutuksen.
- `ui.py`: Toteuttaa piirtämisen pygame kirjastolla.
- `main.py`: Käynnistää ohjelman.
- `helpers.py`: Apufunktioita, kuten ruudukon käsittely.
- `app.py`: Hallitsee Pygame-ympäristön alustamisen ja pääsilmukan käsittelyn.

<!-- ## Saavutetut aika- ja tilavaativuudet
 A*-algoritmin aika- ja tilavaativuudet ovat:
 - Aikavaativuus: O(b^d), missä b on haarautumissuhde ja d on syvyys.
 - Tilavaativuus: O(b^d), koska algoritmi tallentaa kaikki solmut muistiin. 

 JPS-algoritmin aika- ja tilavaativuudet ovat:
- Aikavaativuus: O(k), missä k on hyppyjen määrä.
- Tilavaativuus: O(k), koska algoritmi tallentaa vain hyppypisteet muistiin. 

## Suorituskyky- ja O-analyysivertailu
A*-algoritmi on yleisesti tehokas ja tarkka, mutta sen suorituskyky heikkenee suurilla ja monimutkaisilla kartoilla. JPS parantaa A*-algoritmin suorituskykyä vähentämällä tutkittavien solmujen määrää, erityisesti avoimilla alueilla. JPS:n suorituskyky on parempi, koska se hyppää useiden solmujen yli kerralla, mikä vähentää laskentakustannuksia.-->

## Työn mahdolliset puutteet ja parannusehdotukset
- Algoritmien optimointi: Nykyiset toteutukset voisivat hyötyä lisäoptimoinneista, kuten paremmista tietorakenteista.
- Käyttöliittymä: Käyttöliittymä voisi olla käyttäjäystävällisempi ja tarjota enemmän visualisointeja algoritmien toiminnasta.
- Testaus: Lisää yksikkötestejä ja suorituskykytestejä tarvitaan kattavamman testauksen varmistamiseksi.
- Algoritmit: Vertailussa vain A* ja JPS. Muita reitinhakualgoritmeja, kuten Dijkstra, BFS, Fringe ei ole toteutettu tai vertailtu.

## Laajojen kielimallien käyttö
Tässä projektissa on käytetty ChatGPT:tä apuna koodin selittämisessä ja dokumentoinnissa. Kaikki LLM:ien tuottama teksti on tarkistettu / muokattu ennen käyttöä. Claude 3.5 Sonnet on auttanut algoritmien toiminnan selittämisessä.

## Viitteet
- [Jump Search Algorithm in Python – A Helpful Guide with Video](https://blog.finxter.com/jump-search-algorithm-in-python-a-helpful-guide-with-video/)
- [Online Graph Pruning for Pathfinding on Grid Maps](https://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf)
- [A Visual Explanation of Jump Point Search](https://zerowidth.com/2013/a-visual-explanation-of-jump-point-search/)