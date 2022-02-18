# FastAPI async practice

Developing and Testing an Asynchronous API with FastAPI, including interactive API documentation.

## Installation

Install both production and development packages

```
$ poetry install
```

Install production packages

```
$ poetry install --no-dev
```

## Local development

start server

```
$ uvicorn app.main:app --reload
```

## Initial data

```
$ python -m app.initial_data
```

## Running the tests

```
$ tox
```

## Interactive API docs

[http://127.0.0.1:8008/docs](http://127.0.0.1:8008/docs)
