Homework 05
===========

**Due Date: Thursday, Mar 5, by 11:00am central time**

The Fountains of FastAPI
------------------------

This homework is an extension of your previous homework --- homework 04. The goal
this week is to transform your simple Python3 script into a full FastAPI web
application. Please first copy all of the ``homework04`` files into a new folder
called ``homework05``.


PART 1
~~~~~~

Your FastAPI application will be containerized and have the same (or similar)
functionality as in homework 04, but in this homework each functionality should
be accessible by a FastAPI route. The following routes are required:

+----------------------------------+------------+--------------------------------------------+
| **Route**                        | **Method** | **What it should do**                      |
+----------------------------------+------------+--------------------------------------------+
| ``/epochs``                      | GET        | Return entire data set                     |
+----------------------------------+------------+--------------------------------------------+
| ``/epochs?limit=int&offset=int`` | GET        | Return modified list of Epochs given query |
|                                  |            | parameters                                 |
+----------------------------------+------------+--------------------------------------------+
| ``/epochs/<epoch>``              | GET        | Return state vectors for a specific Epoch  |
|                                  |            | from the data set                          |
+----------------------------------+------------+--------------------------------------------+
| ``/epochs/<epoch>/speed``        | GET        | Return instantaneous speed for a specific  |
|                                  |            | Epoch in the data set (math required!)     |
+----------------------------------+------------+--------------------------------------------+
| ``/now``                         | GET        | Return state vectors and instantaneous     |
|                                  |            | speed for the Epoch that is nearest in     |
|                                  |            | time                                       |
+----------------------------------+------------+--------------------------------------------+


All of the normal Python3 script best practices apply:

* Write appropriately formatted doc strings for your functions
* Use type annotations where appropriate
* Organize your code in the same way as the other scripts we have written
* Write unit tests for all functions except the ``main()`` function - special
  consideration may be required to write unit tests for FastAPI routes
* Implement selective logging and error handling where appropriate


.. tip::

   For the speed function, you will need an equation to calculate speed from
   Cartesian velocity vectors: **speed = sqrt(x_dot^2 + y_dot^2 + z_dot^2)**


PART 2
~~~~~~

Include a software diagram in your repository. This time, focus your diagram
on the FastAPI API and how a user interacts with it. You may want to illustrate
the container, the data source, the queries, and the responses, for example.
Again, there is really no wrong answer here -- we just want you to think about
illustrating something about your software system in a way that is useful for
describing it to others. 

.. note::

   After collecting Homework 05, we will share some model diagrams from the class
   (with permission). This will give you a chance to reflect on your own diagram
   and update it if necessary for inclusion in the Midterm.


PART 3
~~~~~~

The homework must also include a README file. The README should be descriptive,
use proper grammar, and contain enough instructions so anyone else could clone
the repository and figure out how to run your app and interact with it. 
Guidelines to follow for the README are:

* Descriptive title
* High-level description of the folder contents / project objective. I.e. why
  does this exist and why is it important? (2-3 sentences)
* Instructions on how to access and description of the data set from the original source
  (do not include the data itself in this repository!)
* Instructions on how to build a container for your code
* Instructions to deploy your containerized code as a FastAPI app (be careful to
  specify anythin the user needs to know about exposing the correct port)
* Instructions including specific ``curl`` commands for accessing the routes in
  your app
* Descriptions of what the output from each route shows / means
* Try to use markdown styles to your advantage, give the sections headers, use
  code blocks where appropriate, etc.

Remember, the README is your chance to document for yourself and explain to others
why the project is important, what the code is, and how to use it / interpret
the outputs / etc. This is a *software engineering and design* class, so we are
not just checking to see if your code works. We are also evaluating the design of
the overall submission, including how well the project is described in the README.


What to Turn In
---------------

A sample Git repository may contain the following new files after completing
homework05:

.. code-block:: text
   :emphasize-lines: 10-15

   my-coe332-hws/
   ├── homework01
   │   └── ...
   ├── homework02
   │   └── ...
   ├── homework03
   │   └── ...
   ├── homework04
   │   ├── ...
   ├── homework05
   │   ├── Dockerfile
   │   ├── README.md
   │   ├── diagram.png
   │   ├── iss_tracker.py
   │   └── test_iss_tracker.py
   └── README.md


Note on Using AI
----------------

The use of AI to complete this assignment is not recommended, but it is
permitted with the following restrictions:

The use of LLMs (like ChatGPT, Copilot, etc) or any other AI must be rigorously
cited. Any code blocks or text that are generated by an AI model should be clearly
marked as such with in-code comments describing what was generated, how it was
generated, and why you chose to use AI in that instance. The homework README must
also contain a section that summarizes where AI was used in the assignemnt.







Additional Resources
--------------------

* `NASA Data Set <https://www.nasa.gov/spot-the-station/#TRAJECTORY>`_
* `Info on State Vectors <https://en.wikipedia.org/wiki/Orbital_state_vectors>`_
* `Info on Reference Frame <https://en.wikipedia.org/wiki/Earth-centered_inertial>`_
* `Unit on XML <../unit02/xml.html>`_
* Please find us in the class Slack channel if you have any questions!

