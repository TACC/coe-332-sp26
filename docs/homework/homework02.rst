Homework 02
===========

**Due Date: Tuesday, Feb 10, by 11:00am central time**

A Fall of Meteordust
--------------------

Our in-class examples so far have used a modified and abridged Meteorite Landings
data set. For this homework, we will work with the real Meteorite Landings data
set from NASA while exercising our Python3 best practices.


PART 1
~~~~~~

Write two Python3 scripts for reading and summarizing the Meteorite Landings data
from NASA. The requirements are as follows:

* Scripts are organized following guidelines in Unit 03
* Primary script reads in CSV-formatted 
  `Meteorite Landings data <https://data.nasa.gov/docs/legacy/meteorite_landings/Meteorite_Landings.csv>`_
* Define Pydantic models to describe the data and use those to read the data in from the CSV. Note that
  you should define **two Pydantic models**, one for the ``GeoLocation`` column and one for the ``MeteoriteLanding`` object 
  itself. As we did in class, the ``MeteoriteLanding`` object should include the ``GeoLocation`` object as a field. 
* Primary script contains functions for parsing the data and
  printing or plotting some summary statistics to screen or file. These can
  be the same functions shown in the class (i.e., ``compute_average_mass``,
  ``check_hemisphere``, or ``count_classes``), however, you should update them to use the new model definitions. 
* At least one function must make use of the great-circle distance algorithm to
  calculate the distance between landing sites (see reference at the end of the assignment).
* The great-circle distance algorithm must be provided as a standalone script / 
  function that is imported into your primary script
* All functions must contain appropriate doc strings and type hints
* All functions must contain corresponding unit tests in an appropriately-named 
  files. Unit tests must be compatible with ``pytest``
* Scripts must support logging, and include a mix of log statements (focus on 
  ``DEBUG``, ``WARNING``, and ``ERROR`` where appropriate)
* Scripts must use appropriate error handling if, e.g., a null value is present
  in the input data


PART 2
~~~~~~

Your homework 02 files must be within a new subdirectory called ``homework02`` in
your COE 332 homeworks repository on GitHub. The directory should contain your primary
Python3 script, the secondary script containing the great-circle distance function,
two unit test scripts, and a ``README.md`` file. The README should
be descriptive, use proper grammar, and contain enough instructions so anyone else
could clone the repository and figure out what the scripts do and how to run them.
General guidelines to follow for the README for homework 02 are:

* Descriptive title
* High-level description of the folder contents / project objective. I.e. why
  does this exist and why is it important? (2-3 sentences)
* Specific description of the individual Python3 scripts (1-2 sentences each)
* Instructions to obtain any necessary data and where to copy it to
* Instructions to run the code from start to finish, plus how to interpret the
  results (2-3 sentences)
* Use markdown styles to your advantage, give the sections headers, use code
  blocks where appropriate, etc.

Remember, the README is your chance to document for yourself and explain to others
why the project is important, what the code is, and how to use it / interpret
the outputs / etc. This is a *software engineering and design* class, so we are
not just checking to see if your code works. We are also evaluating the design of
the overall submission, including how well the project is described in the README.


What to Turn In
---------------

A sample Git repository may contain the following new files after completing
homework 02:

.. note:: 

  We did not explicitly require you to turn in you ``pyproject.toml`` and ``uv.lock`` files, 
  but please be sure to include those this time. Going forward, having these files will be 
  important as we add more dependencies. We also highly recommended you include a ``.gitignore``
  so that you can ignore Python cache files (.pyc files) and other files that will clutter your 
  version control history. 

.. code-block:: text
   :emphasize-lines: 2-4, 9-14

   my-coe332-hws/
   |── .gitignore
   |── pyproject.toml
   |── uv.lock
   ├── homework01
   │   ├── README.md
   │   ├── ml_json_converter.py
   │   └── ml_json_reader.py
   ├── homework02
   │   ├── README.md           
   │   ├── gcd_algorithm.py        # your file names may vary
   │   ├── ml_data_analysis.py
   │   ├── test_gcd_algorithm.py
   │   └── test_ml_data_analysis.py
   └── README.md

There is no need to email the link to your homework repo again, as we should have
it on file from the first homework. We will re-clone the same repo as before at the
due date / time for evaluation.


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

* `Meteorite Landings Data <https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh/about_data>`_
* `JSON guide <https://coe-332-sp25.readthedocs.io/en/latest/unit02/json.html>`_
* `Latitude and Longitude as decimals <https://en.wikipedia.org/wiki/Decimal_degrees>`_
* `Great-circle distance formula <https://en.wikipedia.org/wiki/Great-circle_distance>`_
* `Markdown syntax <https://www.markdownguide.org/basic-syntax/>`_
* `Tips on writing a good README <https://www.makeareadme.com/>`_
* Please find us in the class Slack channel if you have any questions!
