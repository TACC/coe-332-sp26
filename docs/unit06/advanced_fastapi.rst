Advanced FastAPI
================

We continue using FastAPI in this module with a look at more complex endpoints and data retrieval
functions for our REST API. After going through this module, students should be able to:

* Identify valid and invalid FastAPI route return types
* Use both Python built-in types (e.g. ``int``) and Pydantic data models to valid FastAPI 
  inputs and return types
* Extract Content-Type and other headers from Flask route responses
* Add query parameters to GET requests, and extract their values inside Flask routes
* Deal with errors from user-supplied input to an API and handle Python exceptions
* Handle multiple request methods to support CRUD operations

.. note::

   We will continue to work on the the individual student VMs. Like last time, it will be helpful for you to
   have two SSH terminals open to your VM at the same time so you can run your Flask application in
   one terminal and test it in the other.


Defining the URLs of Our API
----------------------------

One of our first goals for our API will be to provide an interface to a dataset. Since
the URLs in a REST API are defined by the "nouns" or collections of the
application domain, we can use a noun that represents our data.

For example, suppose we have the following dataset that represents the number of
students earning an undergraduate degree for a given year:

.. code-block:: python3

   def get_data():
       return [ {'id': 0, 'year': 1990, 'degrees': 5818},
                {'id': 1, 'year': 1991, 'degrees': 5725},
                {'id': 2, 'year': 1992, 'degrees': 6005},
                {'id': 3, 'year': 1993, 'degrees': 6123},
                {'id': 4, 'year': 1994, 'degrees': 6096} ]


In this case, one collection described by the data is "degrees". So, let's
define a route, ``/degrees``, that by default returns all of the data points.

EXERCISE 1
~~~~~~~~~~

Create a new file, ``degrees_api.py`` to hold a FastAPI application then do the
following:

1) Import the FastAPI class and instantiate a FastAPI application
   object.
2) Copy the ``get_data()`` method above into the application
   script.
3) Add a route (``/degrees``) which responds to the HTTP ``GET`` request and
   returns the complete list of data returned by ``get_data()``. 

In a separate Terminal use ``curl`` to test out your new route. Does it work as
expected?

.. tip::

   Refer back to the `Intro to FastAPI material <intro_to_fastapi.html>`_ if
   you need help remembering the boiler-plate code.


EXERCISE 2
~~~~~~~~~~
Back inside the ``degrees_api.py`` file, let's add a second route, ``/degrees/{id}`` that returns the 
data associated with a single dictionary. There are often design questions one should consider when writing 
new code. In this case, we have:

  * What method(s) should it accept? 
  * What type will the incoming ``id`` field be from the user? 
  * How will you find the corresponding dictionary? 
  * What should happen if the user enters an ``id`` that doesn't exist?


Discussion
^^^^^^^^^^
By default, FastAPI uses String for the types of path variables. If we use a route declaration like this,

.. code-block:: python3
   
   @app.get('/degrees/{id}', methods=['GET'])
   def degrees_for_id(id):
       # implementation...


Then GET any request with a URL path that starts with ``/degrees/`` and ends with any string will match. That is,

  * ``/degress/0`` --> ``id`` holds the value ``"0"`` as a Python String.
  * ``/degrees/A`` --> ``id`` holds the value ``"A"`` as a Python String.
  * ``/degrees/one`` --> ``id`` holds the value ``"one"`` as a Python String.

will all match the ``degrees_for_id`` route and the variable, ``id`` will hold a ``str`` value. In this case,
we'll have to deal with the ``str`` type in our function, converting it to ``int``, etc.  


Typed URL Parameters
---------------------

We can specify the types of the URL parameters we are expecting using the syntax ``<variable_name:type>``. 
For example, we could change our ``degrees_for_id`` route declaration as follows, to indicate we required the ``id``
variable to be an integer:

.. code-block:: python3
   
   @app.get('/degrees/{id}')
   def degrees_for_id(id: int):
       # implementation...

With the above definition, a request like ``GET /degrees/A`` will no longer match our ``degrees_for_id`` route
while a request like ``GET /degrees/2`` will ``call degrees_for_id`` with an integer type for the ``id``
variable. 



Additional Resources
--------------------
