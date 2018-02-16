# OpenSpy

Программа обращается к сервису авиаданных [OpenSky](https://opensky-network.org/apidoc/index.html)
и выводит список самолетов, находящихся в заданном радиусе от центральной точки.

## Требования

* Python >= 3.5.
* Библиотека [Requests](http://docs.python-requests.org/en/master/).
* Библиотека [Nose](http://nose.readthedocs.io/en/latest/) для тестирования.

## Установка

```
$ pip install -r requirements.txt
```

Или:

```
$ python setup.py develop
```

Рекомендуется [Python virtual environment](https://docs.python.org/3/tutorial/venv.html).

## Тестирование

Из корневой директории проекта:

```
$ nosetests tests/
```

Если нужен подробный лог:

```
$ python tests/test_opensky.py
```

## Запуск

Без аргументов ищет рейсы в радиусе  450км от Парижа.

```
$ python opensky.py
```

Рейсы в радиусе  1000км от Москвы:

```
$ python opensky.py --lat=55.75 --lon=37.58 --range=1000
```

Список доспупных опций:

```
$ python opensky.py --help
```

**ВАЖНО:**: **Долгота** принимает отрицательные значения к востоку от Гринвича и
положительные — к востоку.

### Результаты

* **callsign**: позывной;
* **distance**: расстояние от центра, км.;
* **lat**: широта, гр.
* **lon**: долгота, гр.
* **ts**: Unix timestamp

Пример:
```json
[
    {
        "callsign": "IRA733",
        "distance": 361.9615208814126,
        "lat": 50.028,
        "lon": 7.0035,
        "ts": 1518778459
    },
    {
        "callsign": "JAF2LD",
        "distance": 243.9117114389107,
        "lat": 50.4967,
        "lon": 4.5822,
        "ts": 1518778231
    },
    {
        "callsign": "RYR3TH",
        "distance": 293.57203020859276,
        "lat": 47.3241,
        "lon": -0.8665,
        "ts": 1518778459
    }
]
```

#### Логгирование

Уровень логгинга управляется переменной среды **DEBUG_OPENSKY**

| степень     | значение  |
|-------------|-----------|
| умеренный   | 1         |
| подробный   | > 1       |
| минимальный | < 1       |
