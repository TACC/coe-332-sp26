Working with JSON
=================

In this hands-on module, we will learn how to work with the JSON data format.
JSON (JavaScript Object Notation) is a powerful, flexible, and lightweight data
format that we see a lot throughout this course, especially when working with
web apps and REST APIs.

After going through this module, students should be able to:

* Identify and write valid JSON
* Read JSON into an object in a Python3 script
* Loop over and work with elements in a JSON object
* Write JSON to file from a Python3 script


JSON Basics
-----------

JSON (JavaScript Object Notation) is a lightweight, human-readable text format for 
storing and working with data, especially in web applications and 
API servers like what we will be building this semester. The name comes from the 
fact that the syntax was derived from JavaScript, but the JSON format 
is an open standard that is used in virtually all modern programming languages. 

The JSON format is defined recursively from a set of basic types, as follows:

* Primitive types: including numeric types (integers and floats), strings, and
  booleans,
* Objects: (also called "dictionaries") structured as ``name: value`` pairs using ``{ }``, and 
* Arrays: (also called "lists") structured as a sequence of items using ``[ ]``. 

The following are basic example of JSON objects: 

.. code-block:: python3

  # a JSON string 
  "abc"

  # a JSON integer
  -1

  # A JSON float 
  3.14

  # a JSON boolean -- note the lowercase
  true 

  # a JSON list -- note the mix of primitive types and duplicated values 
  [ "abc", -1, 12, false, "abc"]

  # a JSON dictionary -- keys must be strings and must be unique 
  {
    "foo": "abc", 
    "bar": -1, 
    "key": false 
  }

The recursive nature of JSON objects means combinations of valid JSON 
documents are also valid. For example, dictionary values can be lists, 
and list values can in turn be dictionaries, or other lists, etc. 
Here is a more complex JSON object: 

.. code-block:: json 

    [
        {
          "id": 1, 
          "username": "jstubbs", 
          "is_student": false, 
        }, 
        {
          "id": 2, 
          "username": "cyz", 
          "is_student": true 
        }
    ]


The universality of this data structure makes it ideal for exchanging
information between programs written in different languages and web apps. 
Note that JSON offers a lot of flexibility on the placement of white space 
and newline characters. Here is another example where types have been 
combined to form complex data structures:

.. code-block:: JSON

   {
     "department": "COE",
     "number": 332,
     "name": "Software Engineering and Design",
     "inperson": true,
     "finalgroups": null,
     "instructors": ["Joe", "Charlie", "Nathan"],
     "prerequisites": [
       {"course": "COE 322", "instructor": "Victor"},
       {"course": "SDS 322", "instructor": "Victor"}
     ]
   }

We'll be working through some examples by writing some code on your student VM. We'll use VSCode for these 
interactions. Open a VSCode RemoteSSH session (Cmd+Shift+P -> RemoteSSH) and create a new 
terminal (Cmd+Shift+P -> Terminal: Create New Terminal). 


Within the terminal inside VSCode on your class VM, navigate to your ``uv`` project directory that you created 
last time (``class-work``) and create a new directory within there called ``working-with-json``:

.. code-block:: console 

    [coe332-vm]$ cd class-work
    [coe332-vm]$ mkdir working-with-json

(You can also right-click from within the file explorer view and select New Folder...)

Download this sample JSON files into that folder using the ``wget`` command, or
click `this link <https://raw.githubusercontent.com/TACC/coe-332-sp26/main/docs/unit02/sample-data/Meteorite_Landings_Simple.json>`_
and cut and paste the contents into a file called ``Meteorite_Landings.json``:

.. code-block:: console

   [coe332-vm]$ wget https://raw.githubusercontent.com/TACC/coe-332-sp26/main/docs/unit02/sample-data/Meteorite_Landings_Simple.json



.. note::

   The Meteorite Landing data is adapted from a data set provided by The
   Meteoritical Society here: https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh


EXERCISE
~~~~~~~~

Plug this file (or some of the above samples) into an online JSON validator
(e.g. `JSONLint <https://jsonlint.com/>`_). Try making manual changes to some of
the entries to see what breaks the JSON format.


Read JSON into a Python3 Script
-------------------------------

The ``json`` Python3 library is part of the Python3 Standard Library, meaning it
can be imported without having to be installed by ``uv````. Start editing a new
Python3 script called ``json_ex.py`` within the ``working-with-json`` directory 
using VSCode by right-click'ing the ``working-with-json`` folder, selecting 
``New File...`` and entering 
the name (``json_ex.py``) into the little box that opens up. 
The main file editing panel will also open up the file for editing. 


.. warning::

   Do not name your Python3 script "json.py". If you ``import json`` when there
   is a script called "json.py" in the same folder, it will import that instead
   of the actual ``json`` library.

The code you need to read in the JSON file of state names and abbreviations into
a Python3 object is:

.. code-block:: python3
   :linenos:

   import json

   with open('Meteorite_Landings_Simple.json', 'r') as f:
       ml_data = json.load(f)

Only three simple lines! We ``import json`` from the standard library so that we
can work with the ``json`` module. We use the safe ``with open...`` statement to
open the file we downloaded read-only into a filehandle called ``f``. Finally,
we use the ``load()`` method of the ``json`` class to load the contents of the
JSON file into our new ``ml_data`` object.

EXERCISE
~~~~~~~~
Add code to your script to print out the ``ml_data`` object to the screen. 
Execute the script in the VSCode terminal. 

*Solution.* What do we need to add to the script to print the ``ml_data`` object and 
where should we add it? 

All that is required is that we add a ``print(ml_data)`` to the end of the script. 
We can execute the script in the terminal using the following command: 

.. code-block:: console 

  [coe332-vm]$ python json_ex.py 


EXERCISE
~~~~~~~~

Explore the types of the various objects within ``ml_data`` by making calls to the ``type()`` 
function. In addition, use the ``keys()`` function to see what keys are available within the 
dictionaries. Finally, ``print()`` each of these as necessary to be sure
you know what each is. Be able to explain the output of each call to ``type()``
and ``print()``.

.. code-block:: python3
   :linenos:

   import json

   with open('Meteorite_Landings_Simple.json', 'r') as f:
       ml_data = json.load(f)

   print(type(ml_data))
   print(type(ml_data['meteorite_landings']))
   print(type(ml_data['meteorite_landings'][0]))
   print(type(ml_data['meteorite_landings'][0]['name']))

   print(ml_data)
   print(ml_data['meteorite_landings'])
   print(ml_data['meteorite_landings'][0]
   print(ml_data['meteorite_landings'][0].keys())
   print(ml_data['meteorite_landings'][0]['name'])
   print(type(ml_data['meteorite_landings'][0]['mass']))

.. tip::

   Consider doing this in the Python3 interpreter's interactive mode instead of
   in a script. I especially enjoy using ``ipython`` for such tasks, which can 
   be installed with ``uv add ipython``. 


Modeling Data with Pydantic: A First Look 
------------------------------------------

If we look at an example meteorite landing from the data, we see a common structure: 

.. code-block:: json 

    {
      "name": "Ruiz",
      "id": 10001,
      "class_name": "L5",
      "mass": 21,
      "lat": 50.775,
      "long": 6.08333
    }

Each landing is a dictionary with the following set of six keys and the associated 
types of the values: 

 * ``name`` -- string 
 * ``id`` -- integer 
 * ``class_name`` -- string 
 * ``mass`` -- integer
 * ``lat`` -- float 
 * ``long`` -- float 

The Pydantic Python library provides a powerful facility for modeling data 
using Python types. Using Pydantic models allows us to automatically 
validate and work with data in a robust way. 

To start modeling data with Pydantic, we use define a model using 
the ``BaseModel`` that resembled the data in our application. For example, 
we could create a model to represent a meteorite landing with the following 
code: 

.. code-block:: python 

    from pydantic import BaseModel

    class MeteoriteLanding(BaseModel):
        name: str
        id: int
        class_name: str
        mass: int
        lat: float
        long: float 

What is the code above doing? In the first line, we import ``BaseModel``
from the ``pydantic`` package. We then define a new Python class called 
``MeteoriteLanding`` to model a meteorite landing. Technically, we are 
using Object Oriented Programming (OOP) here, defining a new class that inherits 
from the ``BaseModel`` class. But if you haven't seen OOP, don't worry about 
it --- we'll explain it more in a future lecture. For now, just think of 
it as the syntax needed to define a new Pydantic model. 

Within the ``class`` key word we list the fields (or members) of our model. 
We indent each field to indicate that it belongs to the ``MeteoriteLanding``
class. Each field has a name followed by a type, separated by a ``:``. For 
example, the first line says that each ``MeteoriteLanding`` object has a 
``name`` that is of type ``str``, the Python abbreviation for the string type. 
Similarly, the next line indicates that every ``MeteoriteLanding`` has a 
field called ``id`` of type ``int``, for integer. 

Notice that our ``MeteoriteLanding`` model is a generic description of the 
specific ``Ruiz`` meteorite landing we looked at initially. This is the 
entire idea with data *modeling*. We have provided a template or a blue print 
for how any and all meteorite landing objects will be structured (at least 
in this example).

Using Our PyDantic Model
------------------------

Now that we have a ``MeteoriteLanding`` model, what can we do with it? 
The first thing we can do is use it to create meteorite landing objects. 
We do this by simply passing values for each of the fields, just like if 
we were calling a funtion: 

.. code-block:: python 

    ml1 = MeteoriteLanding(name="Ruiz", 
                           id=10001, 
                           class_name="L5", 
                           mass=21, 
                           lat=50.775, 
                           long=6.08333)

The code above works and creates a new ``MeteoriteLanding`` object called 
``ml1``. Moreover, each of the fields is accessible using "dot notation"; 
for example, ``ml1.name`` has type ``str`` and value ``Ruiz``. 

EXERCISE
~~~~~~~~
Use dot notation and the ``type`` function to verify the values and types of 
the other fields on ``ml1``. 


We can create additional ``MeteoriteLanding`` objects by simply passing 
additional set of values. For example, 

.. code-block:: python 

    ml2 = MeteoriteLanding(name="Beeler", 
                           id=10002, 
                           class_name="H6", 
                           mass=720, 
                           lat=56.18333, 
                           long=10.23333)

    ml3 = MeteoriteLanding(name="Brock", 
                           id=10003, 
                           class_name="EH4", 
                           mass=107000, 
                           lat=54.21667, 
                           long=-113.0)
    . . . 


What would you expect would happen though if we tried to do the following? 

.. code-block:: python 
    :emphasize-lines: 5

    ml4 = MeteoriteLanding(name="Ruiz", 
                           id=1001, 
                           class_name="L5", 
                           mass=21, 
                           lat="abc", 
                           long=6.08333)

There is something wrong with the data: we've stated in the data model that 
``lat`` should be a field of type ``float``, however we are passing in the 
value ``"abc"``, which is clearly not a floating point number. Fundamentally, 
this kind of data is breaking from what our model has described, and this 
could potential cause problems for our program down the line. 
For example, what if we were to try and perform some computation witht he latitude, 
assuming it was a floating point number. This "invalid" data could cause errors 
or even make our program crash. We'd like to detect that in a controlled way.

Indeed, if we execute the code above in an ``ipython`` shell we see the following
error: 

.. code-block:: python 

    ValidationError: 1 validation error for MeteoriteLanding
    lat
    Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='abc', input_type=str]
        For further information visit https://errors.pydantic.dev/2.12/v/float_parsing

Let's try one more example. What do you think will happen with the following 
code? Is this a valid or invalid according to the model?

.. code-block:: python 
    :emphasize-lines: 5

    ml4 = MeteoriteLanding(name="Ruiz", 
                           id=10001, 
                           class_name="L5", 
                           mass=21, 
                           lat="50.775", 
                           long=6.08333)

Technically, we are trying to pass a string (``"50.775"``) for the ``lat`` 
field that was declare to be a ``float`` type. However, Pydantic accepts 
this code as "valid" and it creates the ``ml4`` object. What does it do 
to the ``lat`` field? 

.. code-block:: python3 

    ml4.lat
    --> 50.775

    type(ml1.lat)
    --> float

Pydantic converted it automatically to a float because the contents of the 
string represented a valid floating point. In many cases, this kind of 
behavior -- automatically converting types when possible -- will be useful 
in your application, but in other cases, you may want the type checking to 
be strict. This, like many things in software engineering, depends on the 
requirements of your application, but rest assured that Pydantic provides 
a mechanism for enforcing strict types when you need it. 



Validating JSON Data 
--------------------

Similarly, we can also use Pydantic models to validate the JSON data that is 
supposed to represent meteorite landings. Recall the following JSON object: 

.. code-block:: json 

    {
      "name": "Ruiz",
      "id": 10001,
      "class_name": "L5",
      "mass": 21,
      "lat": 50.775,
      "long": 6.08333
    }

If we read this object into Python (from a file, say) using ``json.load`` 
we would have a Python dictionary: 

.. code-block:: python3 

    d = {'name': 'Ruiz',
         'id': 10001,
         'class_name': 'L5',
         'mass': 21,
         'lat': 50.775,
         'long': 6.08333}

Recall that if I have a Python function, ``f``, and a dictionary, ``d``, 
then the syntax ``f(**d)`` means: "Call the function f passing named 
arguments for each key in ``d`` and its associated value."

For example, if I have a function: 

.. code-block:: python 

    def f (first: int, second: int) -> int: 
       return first + second 

and a python dictionary with keys ``first`` and ``second``, like so:

.. code-block:: python 

   d = { "first": 5, "second": 3}

then:

.. code-block:: python 

    f(**d)
    --> 8


In the same kind of way, we can create a ``MeteoriteLanding`` object from the 
first dictionary above using this ``**d`` notation: 

.. code-block:: python 

    d = {'name': 'Ruiz',
         'id': 10001,
         'class_name': 'L5',
         'mass': 21,
         'lat': 50.775,
         'long': 6.08333}
    
    ml5 = MeteoriteLanding(**d)

And just like before, Pydantic handles data validation for us. 
What do you think would happen with the following code?

.. code-block:: python 

    d = {'name': 'Ruiz',
         'id': "a123",
         'class_name': 'L5',
         'mass': 21,
         'lat': 50.775,
         'long': 6.08333}
    
    ml5 = MeteoriteLanding(**d)

EXERCISE
~~~~~~~~
Previously, we read the Meteorite_Landings_Simple.json file into Python. 
Modify your script to read the data into a list of ``MeteoriteLanding`` 
objects. 

*Solution.* 

.. code-block:: python 

    import json
    from pydantic import BaseModel 

    class MeteoriteLanding(BaseModel):
        name: str
        id: int
        class_name: str
        mass: int
        lat: float
        long: float

    mls = []
    with open('Meteorite_Landings_Simple.json', 'r') as f:
        ml_data = json.load(f)
    for ml in ml_data["meteorite_landings"]:
        mls.append(MeteoriteLanding(**ml))


Work with JSON Data
-------------------

As we have seen, the meteorite landing data contains fields including
names, ids, classes, masses, latitudes, and longitudes. Let's write a
few functions to help us analyze the data.

A powerful aspect of Pydantic models is that we can use them to describe 
the types just like ``int``, ``float``, etc. For example, we can use 
them in the signatures of functions. We'll see this in the examples 
below. 

First, we'll write a function to calculate the average mass of a set of 
meteorites from the data set. What kind of argument(s) should our function 
take? 

Our function will take a list of ``MeteoritLanding`` objects, and it will 
iterate over that list, collecting the ``mass`` of each object as it goes.
Remember, we can use dot notation to access the ``mass`` of each 
meteorite landing. 

After implementing it, call the function with the entire list of meteorite landings
(the ``mls`` object computed in the previous exercise), 
and have it print the average mass to screen.


*Solution.* 

.. code-block:: python3
   :linenos:

   def compute_average_mass(landings: list[MeteoriteLandings]) -> float: 
       total_mass = 0.
       for ml in landings:
           total_mass += ml.mass
       return (total_mass / len(landings))
   
   print(compute_average_mass(mls))

Notice how easy to read our function becomes. Just from the signature, 
you can immediately tell what kind of data the function requires, and 
the ``for`` loop clearly sums up the mass of the 

Next, write a function to check where on the globe the meteorite landing site is
located. We need to check whether it is Northern or Southern hemisphere, and
whether it is Western or Eastern hemisphere.

In this case, our function will accept just a single ``MeteoriteLanding`` 
object, and it will use dot notation to access its ``lat`` and ``long`` 
fields. 

Once you implement the function, call it with the first meteorite landing 
from the ``mls`` list.

.. code-block:: python3
   :linenos:

   def check_hemisphere(ml: MeteoriteLanding) -> str: 
       location = ''
       if (ml.lat > 0):
           location = 'Northern'
       else:
           location = 'Southern'
       if (ml.long > 0):
           location = f'{location} & Eastern'
       else:
           location = f'{location} & Western'
       return(location)

    check_hemisphere(mls)


EXERCISE
~~~~~~~~

Write a third function to count how many of each 'class' of meteorite there is
in the list. What types should the function signature have? 
The output should look something like:

.. code-block:: console

   type, number
   H, 1
   H4, 2
   L6, 6
   ...etc

*Solution.* A first solution may look something like this:

.. code-block:: python3 

    def meteorite_types(landings: list[MeteoriteLanding]) -> dict:
         result = {}
         for ml in landings:
             if ml.class_name not in result.keys():
                 result[ml.class_name] = 1
             else:
                 result[ml.class_name] += 1
         return result


Serializing Pydantic Models
---------------------------

Another powerful aspect of Pydantic models is that they provide built-in 
methods for *serializing*, or converting, to standard formats such as JSON. 
Given a Pydantic model, for example our ``ml1`` we created above, we can 
use the ``model_dump_json()`` function to generate JSON. 

.. code-block:: python3

    ml1
    --> MeteoriteLanding(name='Ruiz', id=10001, class_name='L5', mass=21, lat=50.775, long=6.08333)

    ml1.model_dump_json()
    --> '{"name":"Ruiz","id":10001,"class_name":"L5","mass":21,"lat":50.775,"long":6.08333}'

Notice that the return type of ``model_dump_json`` is ``str``, exactly what we 
would expect for a serializing method, and the format is structured like JSON. 

Write JSON to File
------------------

Finally, in a new script, we will create an object that we can write to a new
JSON file. Our object will represent a UT course. Each course will have a 
``course_id`` (string), a ``title`` (string), and a list of ``topics``, each 
should be a string. 

We'll first define a Pydantic model to represent our data. Then, we'll create 
an example UTCourse object. Finally, we'll pass the output of ``model_dump_json``
to ``json.dump`` to save it to a file. 

*Solution.*

.. code-block:: python3
   :linenos:

   from pydantic import BaseModel 
   
   class UTCourse(BaseModel):
       course_id: str
       title: str
       topics: list[str]

   course = UTCourse(course_id='COE332', 
                     title='Software Engineering and Design',
                     topics=['linux', 'python3', 'git'])

   with open('course.json', 'w') as out:
       json.dump(course.model_dump_json(), out, indent=2)

Notice that most of the code in the script above was simply assembling a normal
Python3 dictionary. The ``json.dump()`` method only requires two arguments - the
object that should be written to file, and the filehandle. The ``indent=2``
argument is optional, but it makes the output file looks a little nicer and
easier to read.

Inspect the output file and paste the contents into an online JSON validator.



Additional Resources
--------------------

* `Reference for the JSON library <https://docs.python.org/3.9/library/json.html>`_
* `Validate JSON with JSONLint <https://jsonlint.com/>`_
* `Meteorite Landings Data <https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh>`_
