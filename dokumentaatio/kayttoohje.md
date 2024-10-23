# Ohjelman Käyttöohje

## Asennus

1. Lataa ohjelman viimeisin versio.
2. Asenna tarvittavat riippuvuudet:
    ```bash
    poetry install
    ```

## Käyttö

### Ohjelman käynnistys- ja käyttöohje

Käynnistys komennolla:
```bash
poetry run invoke start
```

Testit suoritetaan komennolla:
```bash
poetry run invoke test
```

Testikattavuusraportin generointi komennolla:
```bash
poetry run invoke coverage-report
```

Pylint tarkistus komennolla:
```bash
poetry run invoke lint
```

### Asetukset

Voit muokata ohjelman asetuksia `settings.py`-tiedostossa. Esimerkki:
```py
DRAW_IN_PROGRESS = True
DRAWING_FREQ = 1
```