Exam Study Guide 
================

The exam will cover Units 1 through 6 and homeworks 1 through 5. 

* Python: programming and best practices

  * Writing code with: functions, loops, if-then, data structures, types
  * Code organization: functions, classes, modules, libraries (packages), imports
  * Maintaining package dependencies with ``uv``
  * Logging
  * Programmatic testing
* Data formats, primarily JSON 

  * What are the functions to read JSON from strings and from files? 
  * What kinds of data types can be serialized into JSON? What is an example of a data type that cannot be 
  serialized into JSON? 
  * What are the functions for writing Python objects to JSON? 
* Pydantic data models 

  * Building classes from ``BaseModel``, specifying types of fields. 
  * Building classes from other classes
* Containers, specifically Docker 
  
  * Describe the concepts of Docker container, image, volume and network. 
  * What a Dockerfile is used for and some basic instructions including ``FROM``, ``RUN``, ``COPY``, ``ENV``
* APIs and FastAPI 

  * The basic HTTP methods GET, POST, PUT, DELETE
  * HTTP headers and the meaning of ``Content-type`` and ``Content-length``
  * HTTP response codes and the meaning of a 200 level, 400 level and 500 level response
  * Basics of using ``curl`` and ``requests`` to make HTTP requests to a server. 
  * RESTful HTTP API architecture, including URL paths as collections, single items, and subcollections, and 
    HTTP verbs for actions. 
  * Building HTTP APIs with FastAPI, including: 
  
    * The ``app`` object and the ``@app`` decorators
    * Specifying request and response types 
    * Specifying and working with URL path parameters 
    * Specifying and working with URL query parameters


Example Exam Questions 
----------------------

.. warning:: 

  This set of example questions is **not** intended to be a comprehensive study guide. Rather,
  it is only intended to give you a sense of the format of questions you will be asked. 
  Be sure to review all of the topics in the previous section. 

Short Answer 
^^^^^^^^^^^^
1. (True/False) A docker container is built from a Docker volume? 
2. (True/False) An HTTP header is formatted as a name-value pair. 
3. (True/False) If an API server is overloaded with too many requests from clients, it should return a 400-level error response. 
4. (True/False) A Python library available in the standard library, such as the ``json`` library, must be installed using a tool like ``uv`` from PyPI, the Python Package Index. 
5. (True/False) In Python, logs can be set at different levels to distinguish the severity or importance of the message being logged.
6. (True/False) In Python, a decorator returns a function.
7. (True/False) The HTTP method for creating a resource is PUT.
8. (True/False) Containers deployed to some server do NOT share an operating system.
9. (True/False) In order to define a new pydantic model, you must create a class that extends pydantic's ``BaseModel``
10. (True/False) In python ``json.loads`` converts a JSON-serialized string into a dictionary.
11. (True/False) You can defined nested paydantic models. i.e., a ShoppingCart model have an attribute ``items`` which is a list of ShoppingCartItem models.
12. (True/False) FastAPI ignore type hints in routes
13. (True/False) Pydantic models can NOT extend of pydantic models. Ex. Given model Animal(BaseModel), you can define a model like Dog(Animal).
14. (True/False) A standard endpoint for an HTTP server will have both a route ("/products") and an HTTP verb
15. (True/False) In Python, you can use the ``type`` function to inspect the type of any object
16. (True/False) If you some code within an ``if`` statement like ``if __name__ == "__main__":``, when the module that contains this code is imported, the code within that ``if`` statement will run.
17. (True/False) When testing your code using ``pytest``, you should prefix your test function names with ``test_``


Multiple choice
^^^^^^^^^^^^^^^

* **When working with a Dockerfile (select all that apply):**

a) Use the ``COPY`` instruction to make a copy of a container. 
b) The ``FROM`` instruction is used to define a pre-existing image as the starting point or base for the new image. 
c) Use the ``docker build`` command to build the image defined by the Dockerfile. 
d) Use the ``RUN`` instruction to run containers from the built image. 

*  **Which of thehe following Python objects are JSON-serializable (select all that apply):**

a) A single string, such as ``"abc"``
b) Boolean values, including ``True`` and ``False``
c) The contents of an image file, such as a ``jpg`` file, read from disk using ``file.open()``.
d) The following list: ``[ {"a": 1, "key": True}, 7, "Another string", {"key": "value"}]``

* **Which of the following HTTP methods should be used when creating a new resource:**

a) GET
b) PUT
c) PATCH
d) DELETE
e) POST
   
* **Which of the following status codes should be returned when a user makes a mistake.**

a) 100
b) 200
c) 300
d) 400
e) 500

* **Complete the following decorator for a route that should return a list of courses**: ``@app.______(“/courses”)``

a) get
b) GET
c) post
d) POST
e) list
f) LIST

* **In your FastAPI application, a user requests a resource that does not exist so you raise the following** ``Exception``. ``raise HTTPException(status_code=_________)``. **Complete the exception:**

a) 500
b) 200
c) 400
d) 404
e) 201

* **To see the headers when making a request using the command line utility** ``curl`` **, you must use which of the following flags:**

a) -X
b) -d
c) -v
d) -\-help
e) -\-show-headers

Code Analysis 
^^^^^^^^^^^^^
1. What will be the output of the following code?

.. code-block:: python3 

    data = [{"a": 1, "b": 2}, {"a": 3, "b": -1}, {"a": 4, "b": 1}]
    def f(key):
        tot = 0
        for item in data:
            val = item[key]
            tot += val
        return tot

    print(f("b"))

Writing Code: Part 1
^^^^^^^^^^^^^^^^^^^^

Given the following code:

.. code-block:: python3 

  def get_data():
    return {
      "products": [
        {"id": 1, "name": "Apple", "price": .50},
        {"id": 2, "name": "Banana", "price": 10.00},
        {"id": 3, "name": "Coconut", "price": 4.50},
        {"id": 4, "name": "Pear", "price": 2.50},
        {"id": 5, "name": "Lettuce", "price": 1.50},
      ]
    }

Write a function that:
  1. Takes a single argument that is a list of product dictionaries
  2. Sums the value of all products
  3. and returns that sum as a float
  4. contains type hints for the argument and the return type

Call that function with the data returned from ``get_data`` and prints the result to stdout

Writing Code: Part 2
^^^^^^^^^^^^^^^^^^^^

Given the following code:

.. code-block:: python3 
  
  from pydantic import BaseModel
  from fastapi import FastAPI, HTTPException


  app = FastAPI()

  class Product(BaseModel):
    id: int
    name: str
    price: float

  def get_data():
    return {
      "products": [
        {"id": 1, "name": "Apple", "price": .50},
        {"id": 2, "name": "Banana", "price": 10.00},
        {"id": 3, "name": "Coconut", "price": 4.50},
        {"id": 4, "name": "Pear", "price": 2.50},
        {"id": 5, "name": "Lettuce", "price": 1.50},
      ]
    }


Write 2 FastAPI routes.

**Route 1**
  1. Converts the data returned by ``get_data`` into a list of pydantic models
  2. Returns a list of products

.. code-block:: python3 
  
  @app.____("/_______________")
  def list_products():
    # Fill in the code below

**Route 2**
  1. Converts the data returned by ``get_data`` into a list of pydantic models
  2. Returns a single product by the specified ``id``
  3. Raises an ``HTTPException`` with the correct status code if no product is found with the provided ``id``.

.. code-block:: python3 
  
  @app.____("/_______________/{___}")
  def get_product_by_id(___: ___):
    # Fill in the code below

.. note::
  
  FastAPI allows you to return the pydantic models directly. The framework will serialize it for you