#!/usr/bin/env python2.6

"""Useful functions and classes with no obvious home."""

from itertools import chain
import sys

def flatten(lists):
    """Flatten the given lists."""
    return list(chain.from_iterable(lists))

def main_function(parse_arguments=None):
    """Usage:
    >>> @main_function(parse_arguments)
    >>> def main(options, arguments):
    ...     pass

    Before running the main function, the user-supplied parse_arguments()
    function is onvoked on sys.argv, and the results are passed to the main
    function.  Whatever value is returned by main() is the exit status of the
    program.
    """
    if parse_arguments is None:
        parse_arguments = lambda arguments: (None, arguments)
    def main_decorator(to_decorate):
        def decorated_main(arguments=None):
            if arguments is None:
                arguments = sys.argv
            options, arguments = parse_arguments(arguments)
            sys.exit(to_decorate(options, arguments))
        return decorated_main
    return main_decorator

def typecasted_arithmetic(cls):
    """If you are subclassing a type which overloads the arithmetic operators,
    the inherited functions generally return objects from the superclass.  If
    you wish to ensure that arithmetic operations produce the correct class,
    apply this decorator to your subclass."""
    unary_operators = ["__abs__", "__neg__", "__pos__"]
    binary_operators = ["__add__", "__div__", "__floordiv__", "__mul__",
                        "__radd__", "__rdiv__", "__rfloordiv__", "__rmul__",
                        "__rsub__", "__sub__"]
    def make_operator(function):
        def new_function(self, other):
            result = getattr(super(cls, self), function)(other)
            return cls.from_superclass(result)
        return new_function
    def make_unary_operator(function):
        def new_function(self):
            result = getattr(super(cls, self), function)()
            return cls.from_superclass(result)
        return new_function
    for operator in binary_operators:
        setattr(cls, operator, make_operator(operator))
    for operator in unary_operators:
        setattr(cls, operator, make_unary_operator(operator))
    return cls
