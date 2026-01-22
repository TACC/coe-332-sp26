Unit Testing
============

As our code continues to grow, how can we be sure it is working as expected? If
we make minor changes to the code, what tests can we run to make sure we didn't
break anything? Are our functions written well enough to capture and correctly
handle all of the edge cases we throw at them? In this module, we will use the
Python ``pytest`` library to write unit tests: small tests that are designed to
test specific individual components of code. After working through this module,
students should be able to:

* Find the documentation for the Python ``pytest`` library
* Identify parts of code that should be tested
* Identify appropriate assertions and exceptions to test for
* Write and run reasonable unit tests


Getting Started
---------------

Unit tests are designed to test small components (e.g. individual functions) of
your code. They should demonstrate that things that are expected to work
actually do work, and things that are expected to break raise appropriate errors.
The Python ``pytest`` unit testing framework supports test automation, set up
and shut down code for tests, and aggregation of tests into collections. It is
not part of the Python Standard Library, so we must install it.

In your project directory, run the following:

.. code-block:: console

   [coe332-vm]$ uv add --dev pytest

Find the `documentation here <https://docs.pytest.org/en/7.0.x/>`_.

Pull a copy of the
`meteorite landings data analysis script <https://raw.githubusercontent.com/TACC/coe-332-sp24/main/docs/unit03/scripts/ml_data_analysis.py>`_
we have been working on, and a copy of the
`meteorite landings json file <https://raw.githubusercontent.com/TACC/coe-332-sp24/main/docs/unit02/sample-data/Meteorite_Landings.json>`_,
if you don't have copies already.


Devise a Reasonable Test
------------------------

The functions in this Python3 script are relatively simple, but how can we be
sure they are working as intended? Let's begin with the ``compute_average_mass()``
function. We might choose to test it manually using the Python3 interactive
interpreter:

.. code-block:: python3
   >>> from models import MeteoriteLanding, compute_average_mass
   >>>
   >>> ml1 = MeteoriteLanding(**{"name": 'Meteor1', "id": 1, "recclass": 'L5', "mass (g)": 3, "reclat": 50.775, "reclong": 6.08333})
   >>> ml2 = MeteoriteLanding(**{"name": 'Meteor2', "id": 2, "recclass": 'L5', "mass (g)": 7, "reclat": -50.775, "reclong": 6.08333})
   >>>
   >>> data = [ml1, ml2]
   >>>
   >>> print(compute_average_mass(data))
   5.0

So simple! We import our code, hand-craft a simple data structure, and send the
data plus the key we are interested in to our function. We know off the top of
our heads that the average of 3 and 7 is 5.0, and that is in fact the number we
get back.

Instead of writing that out each time we want to test, let's instead put this
into another Python3 script. When writing test scripts, it is a common convention
to name them the same name as the script you are testing, but with the ``test_``
prefix added at the beginning.


.. code-block:: console

   [coe332-vm]$ touch test_ml_data_analysis.py


Open up the script with VIM (or editor of your choice) and put in our testing code:

.. code-block:: python3
   :linenos:

   from models import MeteoriteLanding, compute_average_mass
   
   ml1 = MeteoriteLanding(**{"name": 'Meteor1', "id": 1, "recclass": 'L5', "mass (g)": 3, "reclat": 50.775, "reclong": 6.08333})
   ml2 = MeteoriteLanding(**{"name": 'Meteor2', "id": 2, "recclass": 'L5', "mass (g)": 7, "reclat": -50.775, "reclong": 6.08333})
   
   data = [ml1, ml2]
   
   print(compute_average_mass(data))


Next try to execute the test script on the command line:

.. code-block:: console

   [coe332-vm]$ python3 test_ml_data_analysis.py
   5.0

Great! We assume the test is working. But we still have to look at the output
(5.0) and remember back to our hand-crafted data and make sure that is the correct
result. It would be more efficient if we had a way to check that the correct
answer is returned in our test script itself. To do this, we can use the ``assert``
statement.

.. code-block:: python3
   :linenos:
   :emphasize-lines: 8

   from models import MeteoriteLanding, compute_average_mass
   
   ml1 = MeteoriteLanding(**{"name": 'Meteor1', "id": 1, "recclass": 'L5', "mass (g)": 3, "reclat": 50.775, "reclong": 6.08333})
   ml2 = MeteoriteLanding(**{"name": 'Meteor2', "id": 2, "recclass": 'L5', "mass (g)": 7, "reclat": -50.775, "reclong": 6.08333})
   
   data = [ml1, ml2]
   
   assert (compute_average_mass(data) == 5.0)

Now instead of printing the result, we use ``assert`` to make sure it is equal
to our expected outcome. If the conditional is true, nothing will be printed. If
the conditional is false, we will see an ``AssertionError``.

EXERCISE
~~~~~~~~

* Write a few more tests to convince yourself that the function is in fact returning
  the average of the input values.
* Modify one of the tests so that it should fail, and execute the tests to confirm
  that it does fail.
* If you have multiple tests that pass and multiple tests that fail, how would you
  know?


Automate Testing with Pytest
----------------------------
We will be using the automated testing framework ``pytest`` to test our code.
Pytest is an excellent framework for small unit tests and for large functional
tests (as we will see later in the semester).

Next, we just need to make a minor organizational change to our test code. We
group all of our tests for a given function (e.g. all the tests for 
``compute_average_mass``) into their own function. By convention, we typically
name that function as "``test_``" plus the name of the function we are testing.
Pytest will automatically look in our working tree for files that start with the
``test_`` prefix, and execute the test functions within.

.. code-block:: python3
   :linenos:
   :emphasize-lines: 7

   from models import MeteoriteLanding, compute_average_mass
   
   ml1 = MeteoriteLanding(**{"name": 'Meteor1', "id": 1, "recclass": 'L5', "mass (g)": 3, "reclat": 50.775, "reclong": 6.08333})
   ml2 = MeteoriteLanding(**{"name": 'Meteor2', "id": 2, "recclass": 'L5', "mass (g)": 7, "reclat": -50.775, "reclong": 6.08333})
   ml3 = MeteoriteLanding(**{"name": 'Meteor3', "id": 3, "recclass": 'L5', "mass (g)": 11, "reclat": -50.775, "reclong": 6.08333})
   
   def test_compute_average_mass():
      assert (compute_average_mass([m1, m2]) == 5.0)
      assert (compute_average_mass([m1, m3]) == 7.0)
      assert (compute_average_mass([m1, m2, m3]) == 7.0)


Call the ``pytest`` executable in your top directory with ``uv run pytest``, it will find your test
function in your test script, run that function, and finally print some
informative output:

.. code-block:: console

   =================================== test session starts =====================================
   platform linux -- Python 3.8.10, pytest-8.0.0, pluggy-1.4.0
   rootdir: /home/wallen/coe-332/code-organization
   collected 1 item
   
   test_ml_data_analysis.py .                                                            [100%]
   
   ==================================== 1 passed in 0.01s ======================================


What Else Should We Test?
-------------------------

The simple tests we wrote above seems almost trivial, but they are actually great
sanity tests to tell us that our code is working. What other behaviors of our
``compute_average_mass()`` function should we test? In no particular order, we
could test the following non-exhaustive list:

* If the list only contains one MeteoriteLanding object, the function still behaves as
  expected
* The return value should be type ``float``
* If we send it an empty list, that should raise some sort of exception
* If we give it bad arguments (e.g. a value is a string instead of a MeteoriteLanding object), we should get an ``Exception``

.. tip::

   A list of all of the built-in Python3 exceptions can be found in the
   `Python docs <https://docs.python.org/3.6/library/exceptions.html>`_.


To test some of these behaviors, let's create some additional assertions and
organize them into their own functions.


.. code-block:: python3
   :linenos:
   :emphasize-lines: 10-11,13-17

   from models import MeteoriteLanding, compute_average_mass
   import pytest
   
   ml1 = MeteoriteLanding(**{"name": 'Meteor1', "id": 1, "recclass": 'L5', "mass (g)": 3, "reclat": 50.775, "reclong": 6.08333})
   ml2 = MeteoriteLanding(**{"name": 'Meteor2', "id": 2, "recclass": 'L5', "mass (g)": 7, "reclat": -50.775, "reclong": 6.08333})
   ml3 = MeteoriteLanding(**{"name": 'Meteor3', "id": 3, "recclass": 'L5', "mass (g)": 11, "reclat": -50.775, "reclong": 6.08333})
   
   def test_compute_average_mass():
      assert (compute_average_mass([ml1, ml2]) == 5.0)
      assert (compute_average_mass([ml1, ml3]) == 7.0)
      assert (compute_average_mass([ml1, m2l, ml3]) == 7.0)

   def test_compute_average_mass_exceptions():
      with pytest.raises(ZeroDivisionError):
         compute_average_mass([])
      with pytest.raises(AttributeError):
         compute_average_mass(["foo"])                    


After adding the above tests, run ``uv run pytest`` again:

.. code-block:: console

   =================================== test session starts =====================================
   platform linux -- Python 3.8.10, pytest-8.0.0, pluggy-1.4.0
   rootdir: /home/wallen/coe-332/code-organization
   collected 2 items
   
   test_ml_data_analysis.py ..                                                           [100%]
   
   ==================================== 2 passed in 0.01s ======================================

Success! The tests for our first function are passing. Our test suite essentially
documents our intent for the behavior of the ``compute_average_mass()`` function.
And, if ever we change the code in that function, we can see if the behavior we
intend still passes the test.


EXERCISE
~~~~~~~~

In the same test script, but under new test function definitions:

* Write tests for the ``check_hemisphere()`` function
* Write tests for the ``count_classes()`` function


Capturing Standard Out
----------------------

If you have a function that prints to standard out (stdout), we can write a 
unit test for that using the ``capsys`` utility. Imagine a function that takes
an argument and prints something to screen:

.. code-block:: python3
   :linenos:

   def print_func(num):      
      print(f'hello {num}') 
                          
   def main():               
      print_func(5)         
                          
   if __name__ == '__main__':
      main()    

Executing this code prints ``hello 5`` to screen. To write a unit test for this,
we import the function into our test script, call the function normally, then
capture the response using the ``capsys.readouterr()`` method. Then we assert that
the response matches our expectations. Assume the above Python code is in a script
called ``print_hello.py``.

.. code-block:: python3
   :linenos:

   from print_hello import print_func   
                                      
   def test_print_func(capsys):          
      print_func(1)                     
      captured = capsys.readouterr()    
      assert captured.out == 'hello 1\n'

Notice that we put a newline character (``\n``) at the end of the expected output.
This character is automatically added by the ``print`` function. See the additional
resources below for more information on using ``capsys``.

Organizing Your Tests & Test Data
---------------------------------

In the previous example, we put our tests in a `test_*.py` file. This is fine if you only have a few tests.
But how should we handle the case in which we are testing many funcions, classes, modules, etc?

There are a many valid ways to organize your tests and test data.

One common approach is to put all of your tests in a ``tests`` directory at the root of you
project. Quite often, the internal directory structure of ``tests`` will closely mirror the directory 
structure of the project you're building tests for.

For example, if we have a function ``check_hemisphere`` in ``src/models.py`` then we might put the test for that function
in ``tests/test_models`` or ``tests/models/test_check_hemisphere``. Following this pattern will make it easy
to find tests associated with some part of your codebase.

Another possibility is to put your tests adjacent to the code against which those tests are written.

For example, if we have a function ``check_hemisphere`` in ``src/models.py`` then we might put the test for that function
in ``src/test_models.py

Your test's will generally follow the same pattern. In the previous tests that we wrote, the
``MeteoriteLanding`` test data was initialized in the test itself. But what if we want to reuse those
test objects? We don't want to rewrite the same test data over and over in different tests.

Regardless of whether we are following the first or second organizational pattern, it often makes the most sense to put
your test objects in some centralized location above or adjacent to the tests that will be using that data.

Additional Resources
--------------------

* `Pytest Documentation <https://docs.pytest.org/>`_
* `Exceptions in Python <https://docs.python.org/3.8/library/exceptions.html>`_
* `Capsys Examples <https://docs.pytest.org/en/7.1.x/how-to/capture-stdout-stderr.html>`_