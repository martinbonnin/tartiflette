from random import randint
from tartiflette.resolver import Resolver
from tartiflette.tartiflette import Tartiflette

from base64 import b64encode

_SCHEMA_SDL = """
    type Query {
        library: Library
    }

    type Library {
        books: [Book]
    }

    type Book {
        id: String
        title: String
        numberOfPages: Int
    }
"""

TTFTT = Tartiflette(_SCHEMA_SDL)

class Book:
    def __init__(self, title):
        self.title = title

    def collect_value(self):
        return {"title": self.title}

@Resolver("Book.numberOfPages", schema=TTFTT.schema_definition)
async def resolver_pages(request_ctx, execution_data):
    print("resolver_pages of", request_ctx, execution_data)
    return randint(0, 256)


@Resolver("Library.books", schema=TTFTT.schema_definition)
async def resolver_books(request_ctx, execution_data):
    print("resolver_library", request_ctx, execution_data)
    return [Book("Title1"), Book("Title2")]
