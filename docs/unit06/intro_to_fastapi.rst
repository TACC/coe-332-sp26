Introduction to FastAPI
=======================

In this section, we will get a brief introduction into FastAPI, the Python web framework,
including how to set up a REST API with multiple routes (URLs). After going through this
module, students should be able to:

* Install the Python FastAPI library and import it into a Python program.
* Define and implement various "routes" or API endpoints in a FastAPI Python program.
* Run a local FastAPI development server.
* Use curl to test routes defined in their FastAPI program when the local development
  server is running.
* **Design Principles**: Additionally, we will see how using FastAPI contributes to 
  the *modularity*, *abstraction*, and *generalization* of software. 


FastAPI is a Python library and framework for building web servers. Some of the
defining characteristics of Flask make it a good fit for this course:

* FastAPI is small and lightweight - relatively easy to use and get setup initially
* FastAPI is robust - a great fit for REST APIs and **microservices**
* FastAPI is performant - when used correctly, it can handle the traffic of sites
  with 100Ks of users
* FastAPI understands Python type hints and Pydantic data models, and can leverage these 
  to help you build more robust, reliable services. 


What is a Microservice?
-----------------------

Microservices - also known as the microservice architecture - is an
architectural style that structures an application as a collection of services
that are:

* Highly maintainable and testable
* Loosely coupled
* Independently deployable
* Organized around business capabilities

The microservice architecture enables the continuous delivery/deployment of
large, complex applications. It also enables an organization to evolve its
technology stack. Many heavily-used, well-known sites use microservices
including Netflix, Amazon, and eBay.

There is a great article on DevTeam.Space
`about microservices <https://www.devteam.space/blog/microservice-architecture-examples-and-diagram/>`_.


Setup and Installation
----------------------

The FastAPI library is not part of the Python standard library but can be
installed with ``uv``. In addition to making FastAPI available to
import into a Python program, it will also expose some new command line tools. On
your Jetstream VM, perform the following:

.. code-block:: console

   [coe332-vm]$ uv add fastapi[standard]
   Resolved 61 packages in 235ms
   Prepared 26 packages in 322ms
   Installed 26 packages in 17ms
   . . .

   [coe332-vm]$ fastapi --help
    Usage: fastapi [OPTIONS] COMMAND [ARGS]...                                                                                           
                                                                                                                                          
    FastAPI CLI - The fastapi command line app. 😎                   
    . . . 


A Hello World FastAPI App
-------------------------

In a new directory on the class server, create a file called ``app.py`` and open
it for editing. Enter the following lines of code:

.. code-block:: python3

  from fastapi import FastAPI

  app = FastAPI()

On the first line, we are importing the ``FastAPI`` class.

On the third line, we create an instance of the ``FastAPI`` class (called ``app``).
This so-called "FastAPI application" object holds the primary configuration and
behaviors of the web server.


Run the FastAPI App
-------------------

There are a few options when starting the FastAPI app. For now, we recommend you
start your Flask application using the ``fastapi dev`` command, specifying the name 
of the Python file (in our case ``main.py``).

.. code-block:: console

   [coe332-vm]$ fastapi dev main.py
   FastAPI   Starting development server 🚀
 
             Searching for package file structure from directories with __init__.py files
             Importing from /home/ubuntu/prep
 
    module   🐍 main.py
 
      code   Importing the FastAPI app object from the module with the following code:
 
             from main import app
 
       app   Using import string: main:app
 
    server   Server started at http://127.0.0.1:8000
    server   Documentation at http://127.0.0.1:8000/docs
 
       tip   Running in development mode, for production use: fastapi run
 
             Logs:
 
      INFO   Will watch for changes in these directories: ['/home/ubuntu/prep']
      INFO   Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
      INFO   Started reloader process [125169] using WatchFiles
      INFO   Started server process [125172]
      INFO   Waiting for application startup.
      INFO   Application startup complete.

That's it! We now have a server up and running. Some notes on what is happening:

* Note that the program took over our shell; we could put it in the background,
  but for now we want to leave it in the foreground. (Multiple PIDs are started
  for the FastAPI app when started in daemon mode; to get them, find all processes
  listening on the port 8000 socket with ``lsof -i:8000``).
* If we make changes to our FastAPI app while the server is running in development
  mode, the server will detect those changes automatically and "reload"; you will
  see a log to the effect of ``Detected change in <file>``.
* We can stop the program with ``Ctrl+C`` just like any other (Python) program.
* If we stop our FastAPI programs, the server will no longer be listening and our
  requests will fail.


Next we can try to talk to the server using ``curl``. Note this line:

.. code-block:: console

     *    server   Server started at http://127.0.0.1:8000

That tells us our server is listening on the ``localhost`` - ``127.0.0.1``, and
on the default Flask port, port ``8000``.

Ports Basics
~~~~~~~~~~~~

Ports are a concept from networking that allows multiple services or programs to
be running at the same time, listening for messages over the internet, on the
same computer.

* For us, ports will always be associated with a specific IP address. In
  general, we specify a port by combining it with an IP separated by a colon (``:``)
  character. For example, ``129.114.97.16:8000``.
* One and only one program can be listening on a given port at a time.
* Some ports are designated for specific activities; Port 80 is reserved for
  HTTP, port 443 for HTTPS (encrypted HTTP), but other ports can be used for
  HTTP/HTTPS traffic.

.. note::

   Only one application can be associated with a given port. If you try to 
   run a second FastAPI application on the same default port (8000) on the 
   same machine, you will hit errors. You can specify the port you want
   FastAPI to listen on using the ``--port`` option to the 
   ``fastapi dev`` command; e.g., 
   ``fastapi dev --port 8001 main.py``
   

curl Basics
~~~~~~~~~~~

You can think of ``curl`` as a command-line version of a web browser: it is just
an HTTP client.

* The basic syntax is ``curl <some_base_url>:<some_port>/<some_url_path>``.
  This will make a ``GET``
  request to the URL and port print the message response.
* Curl will default to using port 80 for HTTP and port 443 for HTTPS.
* You can specify the HTTP verb to use with the ``-X`` flag; e.g.,
  ``curl -X GET <some_url>`` (though ``-X GET`` is redundant because that is the
  default verb).
* You can set "verbose mode" with the ``-v`` flag, which will then show
  additional information such as the headers passed back and forth (more on this
  later).

Try the following, for example: 

.. code-block:: console

   [coe332-vm]$ curl https://api.github.com

Make a Request
--------------

Because the terminal window running your Flask app is currently locked to that
process, the simplest thing to do is open up a new terminal and SSH into the
class server again.

To make a request to your Flask app, type the following in the new terminal:

.. code-block:: console

   [coe332-vm]$ curl 127.0.0.1:8000
   - or -
   [coe332-vm]$ curl localhost:8000


You should see something like the following response:

.. code-block:: json 

  {"detail":"Not Found"}

Our server is sending us JSON! It's sending a 404 that it could not find the
resource we requested. Although it appears to be an error (and technically it
is), this is evidence that the FastAPI server is running successfully. It's time
to add some routes.


Routes in FastAPI
-----------------

In a FastAPI app, you define the URLs in your application using the ``@app``
decorators. Specifications of the ``@app`` decorators include:

* Must specify an HTTP verb as an attribute to ``@app`` using dot notation, and this is the 
  HTTP method that the function will handle. For example, ``@app.get`` for GET requests, 
  ``app.post`` for POST requests, etc. 
* Must be placed on the line before the declaration of a Python function.
* Requires a string argument which is the path of the URL (not including the base
  URL)

When the URL + HTTP method combination is requested, FastAPI will call the
decorated function.


Tangent: What is a Python Decorator?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A decorator is a function that takes another function as an input and extends
its behavior in some way. The decorator function itself must return a function
which includes a call to the original function plus the extended behavior. The
typical structure of a decorator is as follows:

.. code-block:: python3
   :linenos:

   def my_decorator(some_func):

       def func_to_return():

           # extend the behavior of some_func by doing some processing
           # before it is called (optional)
           do_something_before()

           # call the original function
           some_func(*args, **kwargs)

           # extend the behavior of some_func by doing some processing
           # after it is called (optional)
           do_something_after()

       return func_to_return

As an example, consider this test program:

.. code-block:: python3
   :linenos:

   def print_decorator(f):
       def func_to_return(*args, **kwargs):
           print(f'args: {args}; kwargs: {kwargs}')
           val = f(*args, **kwargs)
           print(f'return: {val}')
           return val
       return func_to_return

   @print_decorator
   def foo(a):
       return a+1

   result = foo(2)
   print(f'Got the result: {result}')

Our ``@print_decorator`` decorator gets executed automatically when we call ``foo(2)``.
Without the decorator, the final output would be:

.. code-block:: text

   Got the result: 3

By using the decorator, however, the final output is instead:

.. code-block:: text

   args: (2,); kwargs: {}
   return: 3
   Got the result: 3

Define the Hello World Route
----------------------------

The original FastAPI app we wrote above (in ``main.py``) did not define any routes.
Let's define a "hello world" route for the base URL. Meaning if someone were to
curl against the base URL (``/``) of our server, we would want to return the
message "Hello, world!". To do so, add the following lines to your ``app.py``
script:

.. code-block:: python3
    :linenos:
    :emphasize-lines: 5-7

    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    def root():
        return {"message": "Hello World"}

The ``@app.get`` decorator on line 5 is expecting ``GET`` requests at the base
URL ``/``. When it receives such a request, it will execute the ``root()``
function below it.

In your active SSH terminal, execute the curl command again (you may need to
restart the FastAPI app); you should see:

.. code-block:: console

   [coe332-vm]$ curl localhost:8000/
   {"message":"Hello World"}(

Routes with URL Parameters
--------------------------

FastAPI makes it easy to create routes (or URLs) with variables in the URL. The
variable name simply must appear in curly brackets (``{..}``) within the
``@app.get()`` decorator statement. Then, specify the variable as a parameter 
to the actual function. Additionally, you may specify the type which provides additional 
benefits, as we will see. 

For example, the following would grant the
function below it access to a variable called ``year`` and declare it to be an ``int`` type.

.. code-block:: python3

   @app.get('/{year}')
   def f(year: int):
       # function implementation...


In the next example, we extend our ``main.py`` FastAPI app by adding a route
with a variable (``{name}``) declared ast type ``str``:

.. code-block:: python3
   :linenos:
   :emphasize-lines: 9-11

    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    def root():
        return {"message": "Hello World"}

   @app.get('/{name}')
   def hello_name(name: str):
       return { "message": f"Hello, {name}"}


Now, the FasAPI app supports multiple routes with different functionalities:

.. code-block:: console

   [coe332-vm]$ curl localhost:8000/
   {"message":"Hello World"}

   [coe332-vm]$ curl localhost:8000/joe
   {"message":"Hello, joe"}
   
   [coe332-vm]$ curl localhost:8000/jane
   {"message":"Hello, jane"}


EXERCISE
~~~~~~~~

Let's use the sample Meteorite Landing data (`see here <https://raw.githubusercontent.com/TACC/coe-332-sp26/refs/heads/main/docs/unit02/sample-data/Meteorite_Landings_Simple.json>`_)
to define some more interesting routes. We will create a route that allows a user
to download the entire dataset over HTTP. Consider the following:

* What should the name of our function be?
* What URL path should it respond to?
* What HTTP verb(s) should it handle?

Once those questions are answered, we'll need to actually implement the new route function.
What will we need to do to implement the function? The implementation will require two
steps:

1) Read the data into Python from the JSON file. (What Python library will you use for this step?)
2) Return the result of step 1)

Once implemented, test the function using ``curl``.

Next, write one more route to access the information of a specific meteorite.
In REST API parlance, assume the whole data set is a "collection", and the data
from one meteorite is an "item" of that collection.


Additional Resources
--------------------

* `FastAPI Docs <https://fastapi.tiangolo.com/>`_
