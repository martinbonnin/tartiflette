from functools import lru_cache, partial

from tartiflette.parser.cffi import Visitor
from tartiflette.parser.exceptions import (
    UnknownVariableException, TatifletteException
)
from .nodes.field import NodeField
from .nodes.fragment_definition import NodeFragmentDefinition
from .nodes.variable_definition import NodeVariableDefinition


async def _default_resolver(ctx, execution_data):
    try:
        return getattr(execution_data.parent_result, execution_data.name)
    except AttributeError:
        raise TatifletteException(
            "Parent < %s > doesn't contain expected attribute < %s >" %
            (execution_data.parent_result, execution_data.name)
        )


class TartifletteVisitor(Visitor):

    # TODO is usefull only for debug, will
    # be removed when everythings works
    # Same as path information
    @staticmethod
    @lru_cache(maxsize=10)
    def create_node_name(gql_type, name):
        node_name = gql_type
        if name:
            node_name = node_name + "(%s)" % name
        return node_name

    def __init__(self, variables=None, schema_definition=None):
        super(TartifletteVisitor, self).__init__()
        self.path = ""
        self._events = [
            {
                "default": self._in,
                "Argument": self._on_argument_in,
                "Field": self._on_field_in,
                "Variable": self._on_variable_in,
                "IntValue": self._on_value_in,
                "StringValue": self._on_value_in,
                "BooleanValue": self._on_value_in,
                "FloatValue": self._on_value_in,
                "NamedType": self._on_named_type_in,
                "ListType": self._on_list_type_in,
                "NonNullType": self._on_non_null_type_in,
                "VariableDefinition": self._on_variable_definition_in,
                "FragmentDefinition": self._on_fragment_definition_in
            }, {
                "default": self._out,
                "Argument": self._on_argument_out,
                "Field": self._on_field_out,
                "VariableDefinition": self._on_variable_definition_out,
                "FragmentDefinition": self._on_fragment_definition_out,
                "FragmentSpread": self._on_fragment_spread_out
            }
        ]
        self._depth = 0
        self.nodes = []
        self._vars = variables if variables else {}
        self._current_node = None
        self._current_argument_name = None
        self._current_type_condition = None
        self._current_fragment_definition = None
        self._fragments = {}
        self._schema_definition = schema_definition

    def _on_argument_in(self, element):
        self._current_argument_name = element.name

    def _on_argument_out(self, _):
        self._current_argument_name = None

    def _on_value_in(self, element):
        try:
            self._current_node.default_value = element.get_value()
            return
        except AttributeError:
            # Not a vardef so consider it a field
            pass

        self._current_node.arguments.update(
            {
                self._current_argument_name: element.get_value()
            }
        )

    def _on_variable_in(self, element):
        try:
            self._current_node.var_name = element.name
            return
        except AttributeError:
            # Cause it's not a var def so try as a field
            pass

        try:
            var_name = element.name
            self._current_node.arguments.update(
                {
                    self._current_argument_name: self._vars[var_name]
                }
            )
        except KeyError:
            raise UnknownVariableException(var_name)

    def _find_resolver(self, name):
        try:
            return self._schema_definition.get_resolver(name)
        except KeyError:
            pass

        try:
            return self._schema_definition.get_resolver(
                "%s.%s" % (self._current_node.name, name)
            )
        except (KeyError, AttributeError):
            # AttributeError for no Parent
            # KeyError no resolver
            pass

        return _default_resolver

    def _add_node(self, node):
        try:
            self.nodes[self._depth - 1]
        except IndexError:
            self.nodes.append([])

        self.nodes[self._depth - 1].append(node)

    def _on_field_in(self, element):
        self._depth = self._depth + 1

        node = NodeField(
            self._find_resolver(element.name), element.get_location(),
            self.path, element.name, self._current_type_condition
        )

        node.parent = self._current_node
        self._current_node = node
        self._add_node(node)

    def _on_field_out(self, _):
        self._depth = self._depth - 1
        self._current_node = self._current_node.parent

    def _on_variable_definition_in(self, element):
        node = NodeVariableDefinition(
            self.path, element.get_location(), element.name
        )
        node.parent = self._current_node
        self._current_node = node

    def _validate_type(self, varname, a_value, a_type):
        if not isinstance(a_value, a_type):
            raise TypeError(
                "Given value for < %s > is not type < %s >" %
                (varname, a_type)
            )

    def _validates_vars(self):
        # validate given var are okay
        name = self._current_node.var_name
        if name not in self._vars:
            dfv = self._current_node.default_value
            if not dfv and not self._current_node.is_nullable:
                raise UnknownVariableException(name)
            self._vars[name] = dfv
            return None

        a_type = self._current_node.var_type
        a_value = self._vars[name]

        if self._current_node.is_list:
            if type(a_value) != list:
                raise TypeError("Expecting List for < %s > values" % name)
            for val in a_value:
                self._validate_type(name, val, a_type)
            return None

        self._validate_type(name, val, a_type)
        return None

    def _on_variable_definition_out(self, _):
        self._validates_vars()
        # now the VariableDefinition Node is useless so kill it
        self._current_node = self._current_node.parent

    def _on_named_type_in(self, element):
        try:
            self._current_node.var_type = element.name
        except AttributeError:
            pass

    def _on_list_type_in(self, _):
        try:
            self._current_node.is_list = True
        except AttributeError:
            pass

    def _on_non_null_type_in(self, _):
        self._current_node.is_nullable = False

    def _on_fragment_definition_in(self, element):
        nfd = NodeFragmentDefinition(
            self.path,
            element.get_location(),
            element.name,
            type_condition=element.get_type_condition()
        )

        if element.name in self._fragments:
            raise TatifletteException(
                "Fragment < %s > is already define" % element.name
            )

        self._fragments[element.name] = nfd
        self._current_fragment_definition = nfd

    def _on_fragment_definition_out(self, _):
        self._current_fragment_definition = None

    def _on_fragment_spread_out(self, element):
        cfd = self._fragments[element.name]
        self._current_type_condition = cfd.type_condition
        for saved_callback in cfd.callbacks:
            saved_callback()  ## Simulate calling a the right place.
        self._current_type_condition = None

    def _in(self, element):
        self.path = self.path + "/%s" % TartifletteVisitor.create_node_name(
            element.graphql_type, element.name
        )

        try:
            self._events[self.IN][element.graphql_type](element)
        except KeyError:
            pass

    def _out(self, element):
        self.path = "/".join(self.path.split("/")[:-1])

        try:
            self._events[self.OUT][element.graphql_type](element)
        except KeyError:
            pass

    def update(self, event, element):
        self.skip_child = False
        self.event = event

        if element.graphql_type in ['SelectionSet']:
            return  #cause we don't care.

        if not self._current_fragment_definition or \
                element.graphql_type == 'FragmentDefinition':
            # Always execute FragmentDefinitions Handlers,
            # never exec if in fragment.
            self._events[self.event]["default"](element)
        else:
            self._current_fragment_definition.callbacks.append(
                partial(self._events[self.event]["default"], element)
            )