# About the Project

Magneto wants to recruit as many mutants as possibleso he can fight the X-Men.
He has hired you to develop a project that detects if a human is a mutant based on his DNA
sequence.

For that he has asked you to create a program with support to check a DNA, whether
it is mutant or not.

So this projects was devided in layers where you'll find:

## A decoupled library for Genetics purposes

In this library we'll have to support to follow the contracts to create objects
with the correct states to check whether a generic sequence inside a DNA is
mutant.

Check for [Genetics Library](library/gnetics/README.md)

## Domain/Application Layers - Persistent Steps and Statistics

Magneto wants to know in details how the recruiting process is running.
So, every time a DNA is checked, we have support to persist the genetic sequence
and the final result whether the DNA is mutant.

He can also request a report to better making strategical decisions, checking
for the statistics of the DNA being checked in the system.

## Communication Layer

So we implemented a way to communicate with system using REST Api. So, his soldiers
can have the following supports:

### Checking DNA

```http request
ṔOST: /mutant

{“dna”: ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]}
```
Once the system received the data, it returns whether the sequence is correct
as mutant or not, responding with the following statuses:

- **200:** yes, it is a mutant DNA;
- **403:** no, it is not mutant DNA;


### Retrieving statistics

```http request
GET: /status
```

From this resource you'll get:

- number of human DNA checked in the system;
- number of mutant DNA checked in the system;
- ratio number of success finding soldiers;

## Other Implementations

I implemented persistence using **Sqlite3** and Filesystem cache.

# How to use the System

## Requirements 
Set up pipenv software in you environment:
- Python 3.8; 
- Make;
- Git;
- Sqlite drive;

## Steps

* **Step 1:** clone the repository;
* **Step 2:** rename file `.env-sample` to `.env`;
* **Step 3:** run command `$ make db_up` to build database;
* **Step 4:** run command `$ ./manage.py runserver` to start server;

Now you'll be able to make requests in the endpoints.

# Tests and Coverage

## Running tests:

```bash
$ ./manage.py test
```

## Coverage report

```bash
$ coverage run ./manage.py test myapp
```

And then:

```bash
$ coverage report
```
or 

```bash
$ coverage html
```