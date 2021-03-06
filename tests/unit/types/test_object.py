from collections import OrderedDict

from tartiflette.types.field import GraphQLField
from tartiflette.types.object import GraphQLObjectType


def test_graphql_object_init():
    obj = GraphQLObjectType(name="Name",
                            fields=OrderedDict([
                                ("test", GraphQLField(name="arg", gql_type="Int")),
                                ("another", GraphQLField(name="arg", gql_type="String")),
                            ]),
                            interfaces=["First", "Second"],
                            description="description")

    assert obj.name == "Name"
    assert obj.fields == OrderedDict([
        ("test", GraphQLField(name="arg", gql_type="Int")),
        ("another", GraphQLField(name="arg", gql_type="String")),
    ])
    assert obj.interfaces == ["First", "Second"]
    assert obj.description == "description"


def test_graphql_object_repr():
    obj = GraphQLObjectType(name="Name",
                            fields=OrderedDict([
                                ("test", GraphQLField(name="arg", gql_type="Int")),
                                ("another", GraphQLField(name="arg", gql_type="String")),
                            ]),
                            interfaces=["First", "Second"],
                            description="description")

    assert obj.__repr__() == "GraphQLObjectType(" \
                             "name='Name', " \
                             "fields=OrderedDict([" \
                                "('test', GraphQLField(name='arg', " \
                                    "gql_type='Int', arguments=OrderedDict(), " \
                                    "resolver=None, description=None)), " \
                                "('another', GraphQLField(name='arg', " \
                                    "gql_type='String', arguments=OrderedDict(), " \
                                    "resolver=None, description=None))]), " \
                             "interfaces=['First', 'Second'], " \
                             "description='description')"
    assert obj == eval(repr(obj))


def test_graphql_object_eq():
    obj = GraphQLObjectType(name="Name",
                            fields=OrderedDict([
                                ("test", GraphQLField(name="arg", gql_type="Int")),
                                ("another", GraphQLField(name="arg", gql_type="String")),
                            ]),
                            interfaces=["First", "Second"],
                            description="description")

    ## Same
    assert obj == obj
    assert obj == GraphQLObjectType(name="Name",
                                    fields=OrderedDict([
                                        ("test", GraphQLField(name="arg", gql_type="Int")),
                                        ("another", GraphQLField(name="arg", gql_type="String")),
                                    ]),
                                    interfaces=["First", "Second"],
                                    description="description")
    # Currently we ignore the description in comparing
    assert obj == GraphQLObjectType(name="Name",
                                    fields=OrderedDict([
                                        ("test", GraphQLField(name="arg", gql_type="Int")),
                                        ("another", GraphQLField(name="arg", gql_type="String")),
                                    ]),
                                    interfaces=["First", "Second"])

    ## Different
    assert obj != GraphQLObjectType(name="Name",
                                    fields=OrderedDict([
                                        ("another", GraphQLField(name="arg", gql_type="String")),
                                        ("test", GraphQLField(name="arg", gql_type="Int")),
                                        # We reversed the fields
                                    ]),
                                    interfaces=["First", "Second"])
    assert obj != GraphQLObjectType(name="Name",
                                    fields=OrderedDict([
                                        ("test", GraphQLField(name="arg", gql_type="Int")),
                                        ("another", GraphQLField(name="arg", gql_type="String")),
                                    ]),
                                    interfaces=[
                                        "Second"
                                        "First",
                                        # We reversed the interface fields
                                    ],
                                    description="description")
    assert obj != GraphQLObjectType(name="Name",
                                    fields=OrderedDict(),
                                    interfaces=["First", "Second"])
    assert obj != GraphQLObjectType(name="Name",
                                    fields=OrderedDict([
                                        ("test", GraphQLField(name="arg", gql_type="Int")),
                                        ("another", GraphQLField(name="arg", gql_type="String")),
                                    ]),
                                    interfaces=[])
    assert obj != GraphQLObjectType(name="OtherName",
                                    fields=OrderedDict([
                                        ("test", GraphQLField(name="arg", gql_type="Int")),
                                        ("another", GraphQLField(name="arg", gql_type="String")),
                                    ]),
                                    interfaces=["First", "Second"],
                                    description="description")
