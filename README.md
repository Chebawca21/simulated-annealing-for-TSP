# simulated-annealing-for-TSP

# Instalacja
Zainstalowanie potrzebnych pakietów

```
$ pip install -r requirements.txt
```

# Uruchomienie
Wszystkie programy powinny być uruchamiane z głównego folderu projektu.
<br><br>

Uruchomienie pojedynczego algorytmu symulowanego wyżarzania

```
$ python src/train.py
```

<br>

Uruchomienie testu sprawdzającego dokładność algorytmu MDS przekształcającego macierz odległości na listę współrzędnych

```
$ python src/test_MDS.py
```

<br>

Uruchomienie generacji rysunków zdjęć, które zostały wykorzystane w pracy.
```
$ python images/draw_TSP.py
```

Dane z nazwami plików powinny być przekazane do klasy DataLoader w celu wydobycia z nich potrzebnych danych.

Parametry algorytmu symulowanego wyżarzania są podawana poprzez zmienne przy tworzeniu klasy SimulatedAnnealing.
<br><br>

# Kwantowe wyżarzanie
Poniższy program jest zapożyczony z innego repozytorium: https://github.com/pifparfait/GPS
<br>
Oryginalny autor kodu: Parfait Atchadé
```
$ python src/quantum/QA.py
```