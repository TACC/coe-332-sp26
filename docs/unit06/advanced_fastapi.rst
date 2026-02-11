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
   
   @app.get('/degrees/{id}')
   def degrees_for_id(id):
       # implementation...


Then any GET request with a URL path that starts with ``/degrees/`` and ends with any string will 
match. That is,

  * ``/degress/0`` --> ``id`` holds the value ``"0"`` as a Python String.
  * ``/degrees/A`` --> ``id`` holds the value ``"A"`` as a Python String.
  * ``/degrees/one`` --> ``id`` holds the value ``"one"`` as a Python String.

will all match the ``degrees_for_id`` route and the variable, ``id`` will hold a ``str`` value. 
In this case, we'll have to deal with the ``str`` type in our function, converting it to ``int``, 
etc.  


Typed URL Parameters
---------------------

We can specify the types of the URL parameters we are expecting using the syntax ``<variable_name:type>``. 
For example, we could change our ``degrees_for_id`` route declaration as follows, to 
indicate we required the ``id`` variable to be an integer:

.. code-block:: python3
   
   @app.get('/degrees/{id}')
   def degrees_for_id(id: int):
       # implementation...

With the above definition, a request like ``GET /degrees/A`` will no longer match our 
``degrees_for_id`` route while a request like ``GET /degrees/2`` will ``call degrees_for_id`` 
with an integer type for the ``id`` variable. 

EXERCISE 3
~~~~~~~~~~
Modify your ``degrees_for_id`` route to specify an integer path parameter. 


Responses in FastAPI
--------------------

Suppose we wanted to add a third route that just returns a single value, the number of degrees 
associated with a particular dictionary. We might proceed as follows:

  * For the URL path, use ``/degrees/{id}/degrees``
  * Iterate through the list looking for the dictionary with the same ``id`` as the input. 
  * If we find a dictionary, ``d``, with the same id, return ``d['degrees']``.

Let's try that and see what happens.

EXERCISE 4
~~~~~~~~~~
Implement a new route for the ``/degrees/{id}/degrees`` endpoint.

EXERCISE 5
~~~~~~~~~~
With your API server running in one window, open a Python interactive
session in another window and:

* Make a ``GET`` request to your ``/degrees`` URL and capture the response in a
  variable, say ``r``
* Verify that ``r.status_code`` is what you expect (what do you expect it to be?)
* Verify that ``r.content`` is what you expect.
* Use ``r.json()`` to decode the response and compare the type to that of ``r.content``.

Then, repeat the above with the ``/degrees/<id>/degrees`` endpoint. 

.. note:: 

   What Python package will you need to import to make the HTTP request? 

HTTP Content Type Headers
-------------------------

Requests and responses have ``headers`` which describe additional metadata about
them. Headers are ``key:value`` pairs (much like dictionary entries). The ``key``
is called the header name and the ``value`` is the header value.

There are many pre-defined headers for common metadata such as specifying the
size of the message (``Content-Length``), the domain the server is listening on
(``Host``), and the type of content included in the message (``Content-Type``).


We can use ``curl`` or the Python ``requests`` library to see all of the headers
returned on a response from our Flask server. Let's try it.

EXERCISE 6
~~~~~~~~~~

1) Use ``curl`` to make a GET request to your ``/degrees`` endpoint
   and pass the ``-v`` (for "verbose") option. This will show you additional information,
   including the headers. Note that with ``-v``, curl shows headers on both the request and
   the response. Request headers are lines that start with a ``>`` while response headers are
   lines that start with a ``<``.
2) Use ``curl`` again to make the same request, but this time pass the ``--head``
   option instead of the ``-v``; this will show you **only** the headers being
   returned in the response.
3) Inside a Python shell, use ``requests`` to make the same GET request to your ``/degrees``
   endpoint, and capture the result in a variable, ``r``. Inspect the ``r.headers`` attribute.
   What is the type of ``r.headers``?

.. code-block:: console

   [coe332-vm]$ url -v 127.0.0.1:8000/degrees
   *   Trying 127.0.0.1:8000...
   * Connected to 127.0.0.1 (127.0.0.1) port 8000
   > GET /degrees HTTP/1.1
   > Host: 127.0.0.1:8000
   > User-Agent: curl/8.5.0
   > Accept: */*
   > 
   < HTTP/1.1 200 OK
   < date: Wed, 11 Feb 2026 22:30:49 GMT
   < server: uvicorn
   < content-length: 181
   < content-type: application/json
   < 
   * Connection #0 to host 127.0.0.1 left intact
   [{"id":0,"year":1990,"degrees":5818},
   {"id":1,"year":1991,"degrees":5725},
   {"id":2,"year":1992,"degrees":6005},
   {"id":3,"year":1993,"degrees":6123},
   {"id":4,"year":1994,"degrees":6096}]   

.. code-block:: python3

   >>> import requests
   >>>
   >>> response = requests.get('http://127.0.0.1:5000/degrees')
   >>>
   >>> response.headers
   {'date': 'Wed, 11 Feb 2026 22:32:55 GMT', 
   'server': 'uvicorn', 
   'content-length': '25', 
   'content-type': 'application/json'}

We see that we are sending a ``Content-Type`` of ``'application/json'``, which is what we want. 
That is how the Python requests library is able to provide the ``r.json()`` function to 
automatically convert to a Python list or dictionary. 

Media Type (or Mime Type)
~~~~~~~~~~~~~~~~~~~~~~~~~

The allowed values for the ``Content-Type`` header are the defined
**media types** (formerly, **mime types**). The main thing you want to know
about media types are that they:

* Consist of a type and subtype
* The most common types are application, text, audio, image, and multipart
* The most common values (type and subtype) are application/json,
  application/xml, text/html, audio/mpeg, image/png, and multipart/form-data

Query Parameters
----------------

The HTTP specification allows for parameters to be added to the URL in form of
``key=value`` pairs. Query parameters come after a ``?`` character and are
separated by ``&`` characters; for example, the following request to a hypothetical API:

.. code-block:: console

      GET https://api.example.com/degrees?limit=3&offset=2

passes two query parameters: ``limit=3`` and ``offset=2``. Note that the URL path in
the example above is still ``/degrees``; that is, the ``?`` character terminates the URL
path, and any characters that follow create the query parameter set for the request.

In REST architectures, query parameters are often used to allow clients to
provide additional, optional arguments to the request.

Common uses of query parameters in RESTful APIs include:

* Pagination: specifying a specific page of results from a collection
* Search terms: filtering the objects within a collection by additional search
  attributes
* Other parameters that might apply to most if not all collections such as an
  ordering attribute (``ascending`` vs ``descending``)


Specifying Query Parameters in FastAPI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FastAPI allows you to specify query parameters directly in a function signature that 
has been decorated with a ``@app`` decorator. When you declare other function parameters that are 
not part of the path parameters, they are automatically interpreted as "query" parameters.

For example, consider the following line of Python code: 

.. code-block:: python3
  
  @app.get('/degrees')
  def get_degrees(limit: int):
     #...function implementation...

We are declaring a variable, ``limit``, in the function signature, but it does not appear in the 
path ``/degrees`` being passed to the ``@app`` decorator. Thus, FastAPI will consider it to be 
a query parameter. 

Note that, just like any other argument to a Python function, if a default value is not specified 
in the signature, then the parameter is assumed to be required. We can modify the signature to 
include a default value -- the syntax is exactly the same as with normal functions, e.g., 

.. code-block:: python3
  
  @app.get('/degrees')
  def get_degrees(limit: int = 10):
     #...function implementation...

With the above signature, the ``limit`` query parameter will not be required, and if not passed, 
will have a default value of 10. 

EXERCISE 7
~~~~~~~~~~
Implement a ``start`` query parameter on your ``GET /degrees`` endpoint so that the API only 
returns degrees on or after the year passed in ``start``. The ``start`` parameter should be 
optional, and, it not passed, the API should return the degrees from the very beginning. 

Check the behavior by issuing some ``curl`` requests in another window, e.g.,  

.. code-block:: console

   [coe332-vm]$ curl http://api.example.com/degrees?start=1993


Let's use this idea to update our ``degrees_api`` to only return the years starting from the
``start`` query parameter year, if that parameter is provided.


Solution
~~~~~~~~~

To implement a ``start`` query parameter on the ``GET /degrees`` endpoint that only returns data
for years on or after the ``start`` year, we first might write someting like:

.. code-block:: python3
   :linenos:

   @app.get('/degrees')
   def degrees(start: int = 1990):
       data = get_data()
       result = [] 
       # iterate through data and check if years are >= start...

Here, we are specifying a default value of ``1990`` which happens to be the first year in the 
datset. Is that a safe approach? Is there a better default value we could use? 

In the following solution, we modify the default value to be 0. That way, even if the dataset 
grows to include more years in the past, the default behavior will still be to return all of the 
data. 

.. code-block:: python3
   :linenos:

   @app.get('/degrees')
   def degrees(start: int = 0):
       data = get_data()
       result = []
       for d in data:
           if d['year'] >= start:
               result.append(d)
       return result



Error Handling
--------------
What happens if the user enters a non-numeric value for the ``start`` parameter? 
Try it and see what happens:

.. code-block:: console

   [coe332-vm]$ curl http://127.0.0.1:8000/degrees?start=abc


Nice! We get a well-formatted JSON object with a fairly descriptive message about what was wrong: 

.. code-block:: console 
   {
   "detail": [
      {
         "type": "int_parsing",
         "loc": [
         "query",
         "start"
         ],
         "msg": "Input should be a valid integer, unable to parse string as an integer",
         "input": "abc"
      }
   ]
   }

This message is saying the input, ``abc`` of the ``start`` query parameter should have been an 
integer. In other words, FastAPI is automatically taking care of error handling for us! This is 
one of the biggest benefits to using strong typing in our Python signatures. Much of the error 
handling, type conversion, etc., can be handled automatically by the underlying library. 



Additional Resources
--------------------
