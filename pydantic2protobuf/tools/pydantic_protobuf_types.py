"""
https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types
"""
from pydantic.types import PositiveInt


class UInt32Value(PositiveInt):
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(protobuf="Convert to 'google.protobuf.UInt32Value'")

    @classmethod
    def validate(cls, v):
        return cls.validate(v)
