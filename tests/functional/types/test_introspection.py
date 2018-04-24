from unittest.mock import Mock

import pytest

from tartiflette import Resolver
from tartiflette.tartiflette import Tartiflette


@pytest.mark.asyncio
async def test_tartiflette_execute_introspection_output():
    schema_sdl = """
    type Test {
        field1: String
    }

    type Query {
        objectTest: Test
    }
    """

    ttftt = Tartiflette(schema_sdl)

    @Resolver("Query.objectTest", schema=ttftt.schema)
    async def func_field_resolver(*args, **kwargs):
        return {"field1": "Test"}

    result = await ttftt.execute("""
    query Test{
        __type(name: "Test") {
            name
            kind
        }
    }
    """)

    assert """{"data":{"__type":{"name":"Test","kind":"OBJECT"}}}""" == result
