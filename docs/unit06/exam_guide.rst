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
3. (True/False) If an API server is overloaded with too many requests from clients, it should return 
   a 400-level error response. 
4. (True/False) A Python library available in the standard library, such as the ``json`` library, must 
   be installed using a tool like ``uv`` from PyPI, the Python Package Index. 
5. (True/False) In Python, logs can be set at different levels to distinguish the severity or importance 
   of the message being logged. 
6. Multiple choice 

  * When working with a Dockerfile (select all that apply):

   a) Use the ``COPY`` instruction to make a copy of a container. 
   b) The ``FROM`` instruction is used to define a pre-existing image as the starting point or base for the 
      new image. 
   c) Use the ``docker build`` command to build the image defined by the Dockerfile. 
   d) Use the ``RUN`` instruction to run containers from the built image. 

  *  Which of thehe following Python objects are JSON-serializable (select all that apply):

   a) A single string, such as ``"abc"``
   b) Boolean values, including ``True`` and ``False``
   c) The contents of an image file, such as a ``jpg`` file, read from disk using ``file.open()``.
   d) The following list: ``[ {"a": 1, "key": True}, 7, "Another string", {"key": "value"}]``
   
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