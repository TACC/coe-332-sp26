Code Organization
=================

Following standard Python3 code organization practices will make our code easier
to read by other developers, and by our future selves who are looking back to see
what we did. After going through this module, students should be able to:

* Organize code into ``main()`` functions
* Import functions into other scripts without executing the ``main()`` block
* Write functions in a generalizable way so they are reusable
* Use a shebang in their Python3 scripts to make them executable



Main Function
-------------

In many Python programs, you will find the developer has organized their code
into a ``main()`` function. Then, they will only call the ``main()`` function
if the variable ``__name__`` is equal to the string ``'__main__'``. For example:

.. code-block:: python3

    def main():
        # application code goes here

    if __name__ == '__main__':
        main()


If this script is executed on the command line directly, then the internal
variable ``__name__`` will be set to the string ``'__main__'``. The conditional
evaluates as ``True`` and the ``main()`` function is called.

If this script is instead **imported into another script**, say, to reuse some of
the functions defined within, then the internal variable ``__name__`` will instead
be set to the name of the script. Thus, the ``main()`` function is not called,
but other functions defined in this script would be available.

Consider the code below for analyzing the Meteorite Landings:

.. code-block:: python3
    :linenos:

    import json
    from pydantic import BaseModel

    class MeteoriteLanding(BaseModel):
        name: str
        id: int
        class_name: str
        mass: int
        lat: float
        long: float

    def compute_average_mass(landings: list[MeteoriteLandings]) -> float:
        total_mass = 0.
        for ml in landings:
            total_mass += ml.mass
        return (total_mass / len(landings))

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

    with open('Meteorite_Landings_Simple.json', 'r') as f:
        ml_data = json.load(f)

    landings = [MeteoriteLanding(**item) for items in ml_data["meteorite_landings"]]

    print(compute_average_mass(landings))

    for ml in landing:
        print(check_hemisphere(ml))


To reorganize this code, we would put the file read operation and the two function
calls into a main function:

.. code-block:: python3
    :linenos:
    :emphasize-lines: 30-42

    import json
    from pydantic import BaseModel

    class MeteoriteLanding(BaseModel):
        name: str
        id: int
        class_name: str
        mass: int
        lat: float
        long: float

    def compute_average_mass(landings: list[MeteoriteLandings]) -> float:
        total_mass = 0.
        for ml in landings:
            total_mass += ml.mass
        return (total_mass / len(landings))

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

    def main():
        with open('Meteorite_Landings_Simple.json', 'r') as f:
            ml_data = json.load(f)

        landings = [MeteoriteLanding(**ml) for ml in ml_data["meteorite_landings"]]

        print(compute_average_mass(landings))

        for ml in landings:
            print(check_hemisphere(ml))
            
    if __name__ == '__main__':
        main()


Let's put this code in a module called ``ml_data_analysis.py``.

If this code is imported into another Python3 script, that other script will have
access to the ``compute_average_mass()`` and ``check_hemisphere()`` functions,
but it will not execute the code in the ``main()`` function.

EXERCISE
~~~~~~~~

Write a new script to import the above code, assuming that above code is saved
in a file called ``ml_data_analysis.py``:

.. code-block:: python3
    :linenos:
    import ml_data_analysis     # assumes it is in this directory, or installed in known location
    
    ml1 = ml_data_analysis.MeteoriteLanding(name="Ruiz", 
                           id=10001, 
                           class_name="L5", 
                           mass=21, 
                           lat=50.775, 
                           long=6.08333)
                           
    print(ml_data_analysis.check_hemisphere(ml1))

Try executing this new script with and without protecting the imported code in a
``main()`` function. How do the outputs differ?

.. tip::

   The main function does not have to be called literally ``main()``. But, if
   someone else is reading your code, calling it ``main()`` will certainly help
   orient the reader.

Refactoring
-----------

Refactoring is when you reorganize your code while preseving its original behavior.
Refactoring code is analagous to factoring in mathematics. For example:

``f(x) = x^2 + x`` can be written as ``f(x) = x(x + 1)``

or in the opposite direction:

``f(x) = x(x + 1)`` -> ``f(x) = x^2 + x``

The expression changes, but the result does not.

In software engineering, we refactor our code so that it is better organized, more readable, and easier to reason about. 

EXERCISE
~~~~~~~~

Before we start refactoring, take another look at the code above and ask yourself the following:

1. Can I succinctly describe what this code is doing?
2. Can we reorganize this code in some way that improves its readability and our ability to reason about what it does?

.. note::

   Let the following software development principle guide your thinking:

   **Single Responsiblity Principle (SRP)**: A function, class, or module should have a single, well-defined job or responsiblity.

First, let's put our pydantic model in its own module called ``models.py``:

.. code-block:: python3
    :linenos:
    :emphasize-lines: 30-42
    :caption: models.py

    from pydantic import BaseModel

    class MeteoriteLanding(BaseModel):
        name: str
        id: int
        class_name: str
        mass: int
        lat: float
        long: float

Next, let's consider the ``compute_average_mass`` and ``check_hemisphere`` functions. We can see from the types in the function
signatures that both of these functions are tightly coupled to the ``MeteoriteLanding`` class. This is an indication that we should probably
package it with or near the ``MeteoriteLanding`` class.

To keep it simple, lets just put it in the ``models.py`` module.

.. code-block:: python3
    :linenos:
    :caption: models.py

    from pydantic import BaseModel

    class MeteoriteLanding(BaseModel):
        name: str
        id: int
        class_name: str
        mass: int
        lat: float
        long: float

    def compute_average_mass(landings: list[MeteoriteLandings]) -> float:
        total_mass = 0.
        for ml in landings:
            total_mass += ml.mass
        return (total_mass / len(landings))

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

Now we must fix the imports in our ``ml_data_analysis.py`` module.

.. code-block:: python3
    :linenos:

    import json

    from models import MeteoriteLanding, compute_average_mass, check_hemisphere

    def main():
        with open('Meteorite_Landings_Simple.json', 'r') as f:
            ml_data = json.load(f)

        landings = [MeteoriteLanding(**ml) for ml in ml_data["meteorite_landings"]]

        print(compute_average_mass(landings))

        for ml in landings:
            print(check_hemisphere(ml))
            
    if __name__ == '__main__':
        main()

This results in a cleaner, easier to read application that simple to reason about. 

**Q**: What does this program do?

**A**: It loads a meteorite landings dataset, computes the average mass of the meteorites, calculates the which hemispheres they landed in, and prints the results to stdout.

Now run the ``ml_data_analysis`` file with ``uv run python ml_data_analysis.py`` and see that it runs the same as before.

Intermediate Pydantic & Complex Datasets
----------------------------------------

In the ealier examples, we downloaded and used the ``Meteorite_Landings_Simple.json`` dataset. This dataset was
modified to simplify our introduction to the ``pydantic`` library. The original dataset contains json objects with keys
that are not compatible with python's syntax for class attributes.

Now that we have an inital grasp of pydantic, let's work with the original dataset.

On your VM, run the following code in the directory that contains you ``ml_data_analysis.py``.

.. code-block:: console

   [coe332-vm]$ wget https://raw.githubusercontent.com/TACC/coe-332-sp26/main/docs/unit02/sample-data/Meteorite_Landings.json


You should now have a file called ``Meteorite_Landings.py`` with the unmodified JSON inside.

.. code-block:: json 

    {
        "meteorite_landings": [
            {
                "name": "Ruiz",
                "id": "10001",
                "recclass": "L5",
                "mass (g)": "21",
                "reclat": "50.775",
                "reclong": "6.08333",
                "GeoLocation": "(50.775, 6.08333)"
            },
            {
                "name": "Beeler",
                "id": "10002",
                "recclass": "H6",
                "mass (g)": "720",
                "reclat": "56.18333",
                "reclong": "10.23333",
                "GeoLocation": "(56.18333, 10.23333)"
            },
            ...
        ]
    }

There are a few things about this new dataset that should catch you attention.

First, notice the data types of the values for each property. They are all strings!
We know from our previous work that pydantic is smart enough to coerce these
values into the correct python type (provided such coercion is possible).

Second, we have different keys in this dataset:

- ``mass (g)`` instead of ``mass``
- ``reclat`` instead of ``lat``
- ``reclong`` instead of ``long``
- ``recclass`` instead of ``class_name``
- and finally an additional ``GeoLocation`` field with what looks like a tuple of the lat and long wrapped in a string.

Let's now modify our pydantic model to handle this new dataset. 

.. code-block:: python3
    :linenos:
    :caption: models.py

    from pydantic import BaseModel, Field, model_validator


    class MeteoriteLanding(BaseModel):
        name: str
        id: int
        mass: int = Field(alias="mass (g)")
        class_name: str = Field(alias="recclass")
        location: GeoLocation

        @model_validator(mode="before")
        @classmethod
        def preprocess_inputs(cls, values):
            values["location"] = {
                "lat": values["reclat"],
                "long": values["reclong"],
            }
        return values

    class GeoLocation(BaseModel):
        lat: float
        long: float

    ...

Let's break down our modifications to the ``models.py`` module.

First, we created aliases for certain properties of our data using pydantic's Field class.
The Field class is used to annotate an pydantic model attribute with some metadata.
This metadata helps pydantic understands which model attribute corresponds to the input data.

- The value at key ``mass (g)`` will be used with the attribute ``mass``
- The value at key ``reclat`` will be used with the attribute ``lat``
- The value at key ``reclong`` will be used with the attribute ``long``
- The value at key ``recclass`` will be used with the attribute ``class_name``

Second, we added a GeoLocation class that contains a ``lat`` and ``long``.

And finally, we made use of pydantic's ``model_validator`` and python's ``classmethod`` decorators
to instruct pydantic on how to construct the input data. We will learn more about decorators in detail
in a later unit. The ``model_validator`` decorator is a function that will be run before the model class
is instantiated. It allows us to manipulate the incoming data, run validation logic, and much more.

If you're observent, you may have noticed that we completely ignored the ``"Geolocation"`` property in
the data. This is duplicate data on each object that we do not need. Pydantic will safely ignore any additional
properties unless you tell it otherwise.

.. note::

    You can make your model more strict by adding a model config attribute on your model class:
    
    .. code-block:: python

        class MyModel(pydantic.BaseModel):
            model_config = pydantic.ConfigDict(extra="forbid")

Since we nested our ``lat`` and ``long`` properties inside the ``GeoLocation`` model, 
we need to modify the ``check_hemisphere`` function in the ``models.py`` module to access that properly.

.. code-block:: python3
    :linenos:
    :caption: models.py

    ...

    def check_hemisphere(ml: MeteoriteLanding) -> str:
        location = ''
        if (ml.location.lat > 0):
            location = 'Northern'
        else:
            location = 'Southern'
        if (ml.location.long > 0):
            location = f'{location} & Eastern'
        else:
            location = f'{location} & Western'
        return(location)

    ...

Now run the ``ml_data_analysis.py`` file and you will see that we have the same output
as before.

Shebang
-------

A "shebang" is a line at the top of your script that defines what interpreter should
be used to run the script when treated as a standalone executable. You will often
see these used in Python, Perl, Bash, C shell, and a number of other scripting
languages. In our case, we want to use the following shebang, which should appear
on the first line of our Python3 scripts:

.. code-block:: python3

   #!/usr/bin/env python3

The ``env`` command simply figures out which version of ``python3`` appears first
in your path, and uses that to execute the script. We usually use that form instead
of, e.g., ``#!/usr/bin/python3.8`` because the location of the Python3 executable
may differ from machine to machine, whereas the location of ``env`` will not.

Next, you also need to make the script executable using the Linux command
``chmod``:

.. code-block:: console

   [coe332-vm]$ chmod u+x ml_data_analysis.py

That enables you to call the Python3 code within as a standalone executable without
invoking the interpreter on the command line:

.. code-block:: console

   [coe332-vm]$ ./ml_data_analysis.py

This is helpful to lock in a Python version (e.g. Python3) for a script that may
be executed on multiple different machines or in various environments.


Other Tips
----------

As our Python3 scripts become longer and more complex, we should put more thought
into how the different contents of the script are ordered. As a rule of thumb, try
to organize the different sections of your Python3 code into this order:

.. code-block:: python3

   # Shebang

   # Imports

   # Global variables / constants

   # Class definitions

   # Function definitions

   # Main function definition

   # Call to main function

Other general tips for writing code that is easy to read can be found in the
`PEP 8 Style Guide <https://www.python.org/dev/peps/pep-0008/>`_, including:

* Use four spaces per indentation level (no tabs)
* Limit lines to 80 characters, wrap and indent where needed
* Avoid extraneous whitespace unless it improves readability
* Be consistent with naming variables and functions

  * Classes are usually ``CapitalWords``
  * Constants are usually ``ALL_CAPS``
  * Functions and variables are usually ``lowercase_with_underscores``
  * Consistency is the key

* Use functions to improve organization and reduce redundancy
* Document and comment your code

.. note::

   Beyond individual Python3 scripts, there is a lot more to learn about organizing
   *projects* which may consist of many files. We will get into this later in the
   semester.



Additional Resources
--------------------

* `PEP 8 Style Guide <https://www.python.org/dev/peps/pep-0008/>`_
