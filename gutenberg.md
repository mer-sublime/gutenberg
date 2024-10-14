# Gutendex

https://gutendex.com/

The goal is to implement an app that allows to ingest data from gutendex and then query it.

Please keep in mind that your code must be functional and ready for production. That means that you
should use good development practices like testing and a modular and scalable design.

We expect you to develop the project in Python with a recent web framework like Django, FastAPI, Flask
and an ORM (if not included in your chosen framework).

Please read this document completely before starting.

## Data model and ingestion

Implement a data model allowing to store and manage useful informations from gutendex.

For now we are only interested in books written in French.

Write a script, a job or a command to fetch data from gutendex and store them in your own database.

## API `authors`

Implement an API to query the list of authors ranked in descending order based on the sum of
the download count of all their books from your database.

An author has to be described with the fields below:

* name (string): the author name
* date (string): a formated string like "birth_date - death_date" or n/a if unvailable
* number_of_books: the total number of books written or co-written by the author
* number_of_bookshelves: the total number of bookshelves where the author appears
* total_download_count: the sum of the download count of all auhtor's book

Here is an example of the API result:

```
{
    ...

    "results": [
        {
            "name": "Victor Michel",
            "date": "1797 - 1877",
            "number_of_books": 30,
            "number_of_bookshelves": 6,
            "total_download_count": 852
        },
        {
            "name": "Jean de Rose",
            "date": "n/a - 1304",
            "number_of_books": 14,
            "number_of_bookshelves": 4,
            "total_download_count": 345
        },
        {
            "name": "Guillaume",
            "date": "n/a",
            "number_of_books": 4,
            "number_of_bookshelves": 1,
            "total_download_count": 47
        }
    ],

    ...

}
```