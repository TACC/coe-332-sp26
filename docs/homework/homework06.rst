Homework 06
===========

**Due Date: Thursday, Apr 2, by 11:00am central time**

The Hammer of Genes
-------------------

Scenario: We are going to turn our attention to a brand new dataset. The Human Genome
Organization (`HUGO <https://en.wikipedia.org/wiki/Human_Genome_Organisation>`_) is a 
non-profit which oversees the HUGO Gene Nomenclature Committee
(`HGNC <https://en.wikipedia.org/wiki/HUGO_Gene_Nomenclature_Committee>`_). The HGNC 
*"approves a unique and meaningful name for every gene"*. For this homework, we will
download the complete set of HGNC data and inject it into a Redis database through
a Flask interface.

This homework will essentially be a re-hash of the exercises from the last
`Redis section <../unit07/redis_and_flask.html>`_.


.. note::

   If you want to do this homework with a different data set, e.g. the data set you
   want to work on for your final project, just get it approved with the instructors
   first.


PART 1
~~~~~~

You can find the HGNC data on this page: https://www.genenames.org/download/archive/

Scroll to the bottom and look for the link that says "Current tab separated hgnc_complete_set
file" or "Current JSON format hgnc_complete_set file". Please spend some time reading this
page to help you understand the data. I recommend opening up the tsv file in a spreadsheet
tool (like Excel) to get a better feel for what it contains. Notice there are a lot more 
fields than we are used to (54), but it is the same *list-of-dictionaries* format that
we see over and over again in this class. Another thing to notice is that this dataset
is *sparse*, meaning not every cell has data in it.


PART 2
~~~~~~

Start a new directory for this homework (called ``homework06``). Write a Pydantic data model and a FastAPI app that
has a ``/data`` route and a ``/gene`` route to make the first 14 fields from the hgnc dataset available. 

Specifically, write a Pydantic data model to model the following fields from the hgnc data set:

* hgnc_id, symbol, name, locus_group, locus_type, status, location, location_sortable, alias_symbol, alias_name, 
  prev_symbol, prev_name, gene_group, gene_group_id

Here are the details on what the routes should do:

* A POST request to ``/data`` should load the HGNC data to a Redis database. Use the Python
  ``requests`` library to get the data directly from the web and create instances of your Pydantic model 
  with each element from the dataset. Store the Pydantic model objects in Redis. 
* A GET request to ``/data`` should read all data out of Redis and return it as a JSON list.
* A DELETE request to ``/data`` should delete all data from Redis.
* The ``/genes`` route should return a json-formatted list with the ``hgnc_id`` for each object.
  (This is the first field in the data set, and a unique identifier for each gene).
* The ``/genes/<hgnc_id>`` route should return all data associated with a given ``<hgnc_id>``.
  (Again, this is the first field in the data set, and a unique identifier for each gene).
  Be careful to handle the case where something other than a valid gene ID is provided by the user,
  and be careful to handle the sparesely populated data it returns. An example query to this route
  might look like:

.. code-block:: console

   [coe332-vm]$ curl localhost:5000/genes/HGNC:5
   {
    "hgnc_id": "HGNC:5",
    "symbol": "A1BG",
    "name": "alpha-1-B glycoprotein",
    "locus_group": "protein-coding gene",
    "locus_type": "gene with protein product",
    "status": "Approved",
    "location": "19q13.43",
    "location_sortable": "19q13.43",
    "alias_symbol": "",
    "alias_name": "",
    "prev_symbol": "",
    "prev_name": "",
    "gene_group": "Immunoglobulin like domain containing",
    "gene_group_id": 594,
   }


After completing the above, your app should have the following routes:

+-------------------------+------------+--------------------------------------------+
| **Route**               | **Method** | **What it should do**                      |
+-------------------------+------------+--------------------------------------------+
| ``/data``               | POST       | Put data into Redis                        |
+-------------------------+------------+--------------------------------------------+
| ``/data``               | GET        | Return all data from Redis                 |
+-------------------------+------------+--------------------------------------------+
| ``/data``               | DELETE     | Delete data in Redis                       |
+-------------------------+------------+--------------------------------------------+
| ``/genes``              | GET        | Return json-formatted list of all hgnc_ids |
+-------------------------+------------+--------------------------------------------+
| ``/genes/<hgnc_id>``    | GET        | Return all data associated with <hgnc_id>  |
+-------------------------+------------+--------------------------------------------+


Please use defensive programming strategies for your routes with exception handling, and
use doc strings / type annotations as appropriate.



PART 3
~~~~~~

The application should be containerized and orchestrated along side a Redis container.
Write a Dockerfile for containerizing your FastAPI app, and write a Docker-compose yaml
file for orchestrating the services together. Read very closely the 
`Docker Compose <../unit07/redis_and_fastapi.html#docker-compose>`_
section of Unit 07 for detailed instructions on how to do this part. 



PART 4
~~~~~~

Write a README with the standard sections from previous homeworks: there should
be a descriptive title, there should be a high level description of the project,
there should be concise descriptions of the main files within, and you should
be using Markdown styles and formatting to your advantage. We will specifically
be looking for:

* Instructions to launch the containerized app and Redis using docker compose
* Give example API query commands and expected outputs in code blocks

Finally, your README should also have a section to describe the data itself. Please
give enough information for others to understand what data they are seeing and
what it means (not every field must be described, just a general overview).
Please cite the data appropriately as well.



What to Turn In
---------------

A sample Git repository may contain the following new files after completing
homework 06:

.. code-block:: text
   :emphasize-lines: 7-12

   my-coe332-hws/
   ├── homework01
   │   └── ...
   ├── ...
   ├── homework05
   │   └── ...
   ├── homework06
   │   ├── Dockerfile
   │   ├── docker-compose.yaml
   │   ├── gene_api.py
   │   ├── README.md
   │   └── requirements.txt
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

* `HGNC Data Set <https://www.genenames.org/download/archive/>`_
* `Unit on Docker Compose <../unit07/redis_and_flask.html#docker-compose>`_
* Please find us in the class Slack channel if you have any questions!

