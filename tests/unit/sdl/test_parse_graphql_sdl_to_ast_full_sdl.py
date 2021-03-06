from lark.tree import Tree
from lark.lexer import Token

from tartiflette.sdl.builder import parse_graphql_sdl_to_ast


def test_parse_graphql_sdl_to_ast_full_sdl():
    # Inspired by the Kitchen sink example of the GraphQL Js repository
    full_sdl = """
    enum Episode @link_db(table: "movies.slug") {
        A_NEW_HOPE,
        THE_EMPIRE_STRIKES_BACK,
        RETURN_OF_THE_JEDI,
        THE_PHANTOM_MENACE,
        ATTACK_OF_THE_CLONES,
        REVENGE_OF_THE_SITH,
    }
    
    interface Character {
        id: String!
        name: String
        friends: [Character]
        appearsIn: [Episode] @default(value: A_NEW_HOPE)
    }
    
    interface Creature {
        name: String
        species: String
    }
    
    interface Vehicle {
        id: String!
        name: String
        owner: Owner
    }
    
    interface Location {
        id: String!
        name: String
        coordinates(default: [Float] = [0.0, 0.0, 0.0]): [Float]
    }
    
    type Planet implements Location {
        id: String!
        atmosphere: String
    }
    
    union Owner = Organization | Character  # This should cover most ownership cases
    
    type Organization {
        id: String!
        name: String
        members: [Character]
    }
    
    type Human implements Character & Creature {
        id: String!
        name: String
        friends: [Character]
        appearsIn: [Episode]
        homePlanet: Location
    }
    
    type Droid implements Character {
        id: String!
        name: String
        friends: [Character] @deprecated(reason: "Droids can't have friends. Use the acquaintances field.")
        acquaintances: [Character]
        appearsIn: [Episode]
        primaryFunction: String
    }
    
    type Query {
        hero(episode: Episode): Character
        human(id: String!): Human
        droid(id: String!): Droid
        characters(filter: FilterCharacters): [Characters]
        planet(id: String!): Planet
    }
    
    input FilterCharacters {
        limit: Int
        sinceEpisode: Episode
    }

    \"\"\"
    A custom scalar to represent time in the StarWars universe.
    It should support nanoseconds and conversion to/from a flick.
    \"\"\"
    scalar Date
    
    extend type Human {
        born: Date @limit(min: 0)
    }
    
    extend type Droid {
        produced: Date
    }
    
    extend input FilterCharacters {
        existsSince: Date
    }
    """
    expected = Tree('document', [
        Tree('type_system_definition', [
            Tree('type_definition', [
                Tree('enum_type_definition', [
                    Token('ENUM', 'enum'),
                    Tree('name', [
                        Token('IDENT', 'Episode'),
                    ]),
                    Tree('directives', [
                        Tree('directive', [
                            Tree('name', [
                                Token('IDENT', 'link_db'),
                            ]),
                            Tree('arguments', [
                                Tree('argument', [
                                    Tree('name', [
                                        Token('IDENT', 'table'),
                                    ]),
                                    Tree('value', [
                                        Tree('string_value', [
                                            Token('STRING', '"movies.slug"'),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                    Tree('enum_values_definition', [
                        Tree('enum_value_definition', [
                            Tree('enum_value', [
                                Tree('name', [
                                    Token('IDENT', 'A_NEW_HOPE'),
                                ]),
                            ]),
                        ]),
                        Tree('enum_value_definition', [
                            Tree('enum_value', [
                                Tree('name', [
                                    Token('IDENT', 'THE_EMPIRE_STRIKES_BACK'),
                                ]),
                            ]),
                        ]),
                        Tree('enum_value_definition', [
                            Tree('enum_value', [
                                Tree('name', [
                                    Token('IDENT', 'RETURN_OF_THE_JEDI'),
                                ]),
                            ]),
                        ]),
                        Tree('enum_value_definition', [
                            Tree('enum_value', [
                                Tree('name', [
                                    Token('IDENT', 'THE_PHANTOM_MENACE'),
                                ]),
                            ]),
                        ]),
                        Tree('enum_value_definition', [
                            Tree('enum_value', [
                                Tree('name', [
                                    Token('IDENT', 'ATTACK_OF_THE_CLONES'),
                                ]),
                            ]),
                        ]),
                        Tree('enum_value_definition', [
                            Tree('enum_value', [
                                Tree('name', [
                                    Token('IDENT', 'REVENGE_OF_THE_SITH'),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        Tree('type_system_definition', [
            Tree('type_definition', [
                Tree('interface_type_definition', [
                    Token('INTERFACE', 'interface'),
                    Tree('name', [
                        Token('IDENT', 'Character'),
                    ]),
                    Tree('fields_definition', [
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'id'),
                            ]),
                            Tree('type', [
                                Tree('non_null_type', [
                                    Tree('named_type', [
                                        Tree('name', [
                                            Token('IDENT', 'String'),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'name'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'String'),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'friends'),
                            ]),
                            Tree('type', [
                                Tree('list_type', [
                                    Tree('type', [
                                        Tree('named_type', [
                                            Tree('name', [
                                                Token('IDENT', 'Character'),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'appearsIn'),
                            ]),
                            Tree('type', [
                                Tree('list_type', [
                                    Tree('type', [
                                        Tree('named_type', [
                                            Tree('name', [
                                                Token('IDENT', 'Episode'),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                            Tree('directives', [
                                Tree('directive', [
                                    Tree('name', [
                                        Token('IDENT', 'default'),
                                    ]),
                                    Tree('arguments', [
                                        Tree('argument', [
                                            Tree('name', [
                                                Token('IDENT', 'value'),
                                            ]),
                                            Tree('value', [
                                                Tree('enum_value', [
                                                    Tree('name', [
                                                        Token('IDENT', 'A_NEW_HOPE'),
                                                    ]),
                                                ]),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        Tree('type_system_definition', [
            Tree('type_definition', [
                Tree('interface_type_definition', [
                    Token('INTERFACE', 'interface'),
                    Tree('name', [
                        Token('IDENT', 'Creature'),
                    ]),
                    Tree('fields_definition', [
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'name'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'String'),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'species'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'String'),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        Tree('type_system_definition', [
            Tree('type_definition', [
                Tree('interface_type_definition', [
                    Token('INTERFACE', 'interface'),
                    Tree('name', [
                        Token('IDENT', 'Vehicle'),
                    ]),
                    Tree('fields_definition', [
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'id'),
                            ]),
                            Tree('type', [
                                Tree('non_null_type', [
                                    Tree('named_type', [
                                        Tree('name', [
                                            Token('IDENT', 'String'),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'name'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'String'),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'owner'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'Owner'),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        Tree('type_system_definition', [
            Tree('type_definition', [
                Tree('interface_type_definition', [
                    Token('INTERFACE', 'interface'),
                    Tree('name', [
                        Token('IDENT', 'Location'),
                    ]),
                    Tree('fields_definition', [
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'id'),
                            ]),
                            Tree('type', [
                                Tree('non_null_type', [
                                    Tree('named_type', [
                                        Tree('name', [
                                            Token('IDENT', 'String'),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'name'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'String'),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'coordinates'),
                            ]),
                            Tree('arguments_definition', [
                                Tree('input_value_definition', [
                                    Tree('name', [
                                        Token('IDENT', 'default'),
                                    ]),
                                    Tree('type', [
                                        Tree('list_type', [
                                            Tree('type', [
                                                Tree('named_type', [
                                                    Tree('name', [
                                                        Token('IDENT', 'Float'),
                                                    ]),
                                                ]),
                                            ]),
                                        ]),
                                    ]),
                                    Tree('default_value', [
                                        Tree('value', [
                                            Tree('list_value', [
                                                Tree('value', [
                                                    Tree('float_value', [
                                                        Token('SIGNED_FLOAT', '0.0'),
                                                    ]),
                                                ]),
                                                Tree('value', [
                                                    Tree('float_value', [
                                                        Token('SIGNED_FLOAT', '0.0'),
                                                    ]),
                                                ]),
                                                Tree('value', [
                                                    Tree('float_value', [
                                                        Token('SIGNED_FLOAT', '0.0'),
                                                    ]),
                                                ]),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                            Tree('type', [
                                Tree('list_type', [
                                    Tree('type', [
                                        Tree('named_type', [
                                            Tree('name', [
                                                Token('IDENT', 'Float'),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        Tree('type_system_definition', [
            Tree('type_definition', [
                Tree('object_type_definition', [
                    Token('TYPE', 'type'),
                    Tree('name', [
                        Token('IDENT', 'Planet'),
                    ]),
                    Tree('implements_interfaces', [
                        Token('IMPLEMENTS', 'implements'),
                        Tree('named_type', [
                            Tree('name', [
                                Token('IDENT', 'Location'),
                            ]),
                        ]),
                    ]),
                    Tree('fields_definition', [
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'id'),
                            ]),
                            Tree('type', [
                                Tree('non_null_type', [
                                    Tree('named_type', [
                                        Tree('name', [
                                            Token('IDENT', 'String'),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'atmosphere'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'String'),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        Tree('type_system_definition', [
            Tree('type_definition', [
                Tree('union_type_definition', [
                    Token('UNION', 'union'),
                    Tree('name', [
                        Token('IDENT', 'Owner'),
                    ]),
                    Tree('union_member_types', [
                        Tree('named_type', [
                            Tree('name', [
                                Token('IDENT', 'Organization'),
                            ]),
                        ]),
                        Tree('named_type', [
                            Tree('name', [
                                Token('IDENT', 'Character'),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        Tree('type_system_definition', [
            Tree('type_definition', [
                Tree('object_type_definition', [
                    Token('TYPE', 'type'),
                    Tree('name', [
                        Token('IDENT', 'Organization'),
                    ]),
                    Tree('fields_definition', [
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'id'),
                            ]),
                            Tree('type', [
                                Tree('non_null_type', [
                                    Tree('named_type', [
                                        Tree('name', [
                                            Token('IDENT', 'String'),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'name'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'String'),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'members'),
                            ]),
                            Tree('type', [
                                Tree('list_type', [
                                    Tree('type', [
                                        Tree('named_type', [
                                            Tree('name', [
                                                Token('IDENT', 'Character'),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        Tree('type_system_definition', [
            Tree('type_definition', [
                Tree('object_type_definition', [
                    Token('TYPE', 'type'),
                    Tree('name', [
                        Token('IDENT', 'Human'),
                    ]),
                    Tree('implements_interfaces', [
                        Token('IMPLEMENTS', 'implements'),
                        Tree('named_type', [
                            Tree('name', [
                                Token('IDENT', 'Character'),
                            ]),
                        ]),
                        Tree('named_type', [
                            Tree('name', [
                                Token('IDENT', 'Creature'),
                            ]),
                        ]),
                    ]),
                    Tree('fields_definition', [
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'id'),
                            ]),
                            Tree('type', [
                                Tree('non_null_type', [
                                    Tree('named_type', [
                                        Tree('name', [
                                            Token('IDENT', 'String'),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'name'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'String'),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'friends'),
                            ]),
                            Tree('type', [
                                Tree('list_type', [
                                    Tree('type', [
                                        Tree('named_type', [
                                            Tree('name', [
                                                Token('IDENT', 'Character'),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'appearsIn'),
                            ]),
                            Tree('type', [
                                Tree('list_type', [
                                    Tree('type', [
                                        Tree('named_type', [
                                            Tree('name', [
                                                Token('IDENT', 'Episode'),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'homePlanet'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'Location'),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        Tree('type_system_definition', [
            Tree('type_definition', [
                Tree('object_type_definition', [
                    Token('TYPE', 'type'),
                    Tree('name', [
                        Token('IDENT', 'Droid'),
                    ]),
                    Tree('implements_interfaces', [
                        Token('IMPLEMENTS', 'implements'),
                        Tree('named_type', [
                            Tree('name', [
                                Token('IDENT', 'Character'),
                            ]),
                        ]),
                    ]),
                    Tree('fields_definition', [
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'id'),
                            ]),
                            Tree('type', [
                                Tree('non_null_type', [
                                    Tree('named_type', [
                                        Tree('name', [
                                            Token('IDENT', 'String'),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'name'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'String'),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'friends'),
                            ]),
                            Tree('type', [
                                Tree('list_type', [
                                    Tree('type', [
                                        Tree('named_type', [
                                            Tree('name', [
                                                Token('IDENT', 'Character'),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                            Tree('directives', [
                                Tree('directive', [
                                    Tree('name', [
                                        Token('IDENT', 'deprecated'),
                                    ]),
                                    Tree('arguments', [
                                        Tree('argument', [
                                            Tree('name', [
                                                Token('IDENT', 'reason'),
                                            ]),
                                            Tree('value', [
                                                Tree('string_value', [
                                                    Token('STRING', '"Droids can\'t have friends. Use the acquaintances field."'),
                                                ]),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'acquaintances'),
                            ]),
                            Tree('type', [
                                Tree('list_type', [
                                    Tree('type', [
                                        Tree('named_type', [
                                            Tree('name', [
                                                Token('IDENT', 'Character'),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'appearsIn'),
                            ]),
                            Tree('type', [
                                Tree('list_type', [
                                    Tree('type', [
                                        Tree('named_type', [
                                            Tree('name', [
                                                Token('IDENT', 'Episode'),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'primaryFunction'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'String'),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        Tree('type_system_definition', [
            Tree('type_definition', [
                Tree('object_type_definition', [
                    Token('TYPE', 'type'),
                    Tree('name', [
                        Token('IDENT', 'Query'),
                    ]),
                    Tree('fields_definition', [
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'hero'),
                            ]),
                            Tree('arguments_definition', [
                                Tree('input_value_definition', [
                                    Tree('name', [
                                        Token('IDENT', 'episode'),
                                    ]),
                                    Tree('type', [
                                        Tree('named_type', [
                                            Tree('name', [
                                                Token('IDENT', 'Episode'),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'Character'),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'human'),
                            ]),
                            Tree('arguments_definition', [
                                Tree('input_value_definition', [
                                    Tree('name', [
                                        Token('IDENT', 'id'),
                                    ]),
                                    Tree('type', [
                                        Tree('non_null_type', [
                                            Tree('named_type', [
                                                Tree('name', [
                                                    Token('IDENT', 'String'),
                                                ]),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'Human'),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'droid'),
                            ]),
                            Tree('arguments_definition', [
                                Tree('input_value_definition', [
                                    Tree('name', [
                                        Token('IDENT', 'id'),
                                    ]),
                                    Tree('type', [
                                        Tree('non_null_type', [
                                            Tree('named_type', [
                                                Tree('name', [
                                                    Token('IDENT', 'String'),
                                                ]),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'Droid'),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'characters'),
                            ]),
                            Tree('arguments_definition', [
                                Tree('input_value_definition', [
                                    Tree('name', [
                                        Token('IDENT', 'filter'),
                                    ]),
                                    Tree('type', [
                                        Tree('named_type', [
                                            Tree('name', [
                                                Token('IDENT', 'FilterCharacters'),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                            Tree('type', [
                                Tree('list_type', [
                                    Tree('type', [
                                        Tree('named_type', [
                                            Tree('name', [
                                                Token('IDENT', 'Characters'),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'planet'),
                            ]),
                            Tree('arguments_definition', [
                                Tree('input_value_definition', [
                                    Tree('name', [
                                        Token('IDENT', 'id'),
                                    ]),
                                    Tree('type', [
                                        Tree('non_null_type', [
                                            Tree('named_type', [
                                                Tree('name', [
                                                    Token('IDENT', 'String'),
                                                ]),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'Planet'),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        Tree('type_system_definition', [
            Tree('type_definition', [
                Tree('input_object_type_definition', [
                    Token('INPUT', 'input'),
                    Tree('name', [
                        Token('IDENT', 'FilterCharacters'),
                    ]),
                    Tree('input_fields_definition', [
                        Tree('input_value_definition', [
                            Tree('name', [
                                Token('IDENT', 'limit'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'Int'),
                                    ]),
                                ]),
                            ]),
                        ]),
                        Tree('input_value_definition', [
                            Tree('name', [
                                Token('IDENT', 'sinceEpisode'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'Episode'),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        Tree('type_system_definition', [
            Tree('type_definition', [
                Tree('scalar_type_definition', [
                    Tree('description', [
                        Token('LONG_STRING', '"""\n    A custom scalar to represent time in the StarWars universe.\n    It should support nanoseconds and conversion to/from a flick.\n    """'),
                    ]), Token('SCALAR', 'scalar'),
                    Tree('name', [
                        Token('IDENT', 'Date'),
                    ]),
                ]),
            ]),
        ]),
        Tree('type_system_definition', [
            Tree('type_extension', [
                Tree('object_type_extension', [
                    Token('EXTEND', 'extend'),
                    Token('TYPE', 'type'),
                    Tree('name', [
                        Token('IDENT', 'Human'),
                    ]),
                    Tree('fields_definition', [
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'born'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'Date'),
                                    ]),
                                ]),
                            ]),
                            Tree('directives', [
                                Tree('directive', [
                                    Tree('name', [
                                        Token('IDENT', 'limit'),
                                    ]),
                                    Tree('arguments', [
                                        Tree('argument', [
                                            Tree('name', [
                                                Token('IDENT', 'min'),
                                            ]),
                                            Tree('value', [
                                                Tree('int_value', [
                                                    Token('SIGNED_INT', '0'),
                                                ]),
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        Tree('type_system_definition', [
            Tree('type_extension', [
                Tree('object_type_extension', [
                    Token('EXTEND', 'extend'),
                    Token('TYPE', 'type'),
                    Tree('name', [
                        Token('IDENT', 'Droid'),
                    ]),
                    Tree('fields_definition', [
                        Tree('field_definition', [
                            Tree('name', [
                                Token('IDENT', 'produced'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'Date'),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        Tree('type_system_definition', [
            Tree('type_extension', [
                Tree('input_object_type_extension', [
                    Token('EXTEND', 'extend'),
                    Token('INPUT', 'input'),
                    Tree('name', [
                        Token('IDENT', 'FilterCharacters'),
                    ]),
                    Tree('input_fields_definition', [
                        Tree('input_value_definition', [
                            Tree('name', [
                                Token('IDENT', 'existsSince'),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Tree('name', [
                                        Token('IDENT', 'Date'),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
    ])

    assert parse_graphql_sdl_to_ast(full_sdl) == expected
