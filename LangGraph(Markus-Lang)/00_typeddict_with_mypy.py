from typing import TypedDict

"""
TypeDict
TypeDict (technically TypedDict) is part of Python's typing module and provides a way to define dictionaries with specific keys and value types.
How it works:

You define a structure that specifies which keys a dictionary should have and what type each value should be
It's used only for static type checking (during development or with tools like mypy)
It doesn't perform any runtime validation

"""

"""
Pydantic
Pydantic is a data validation library that enforces type hints at runtime.
How it works:

Define models with type annotations
Pydantic validates data when instances are created
It converts data to the right types when possible
It raises validation errors at runtime when data doesn't match

"""

#without one of these , a normal dictionary will have no 
# type checking . 

class Person(TypedDict):
    name: str
    age: int


person: Person = {
    "name": "John",
    "Age": 50,
    "job_title": "Manager",
}  # Type-safe dictionary, static linters like mypy can detect this
