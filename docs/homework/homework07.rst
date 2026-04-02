Homework 07
===========

**Due Date: Thursday, Apr 9, by 11:00am central time**

The Light of Other Jobs
-----------------------

Scenario: Continuing from the previous homework, we are going to add some new
functionality into our web API. Please start from the files developed in Homework
06, and continue to use the `HGNC data <https://www.genenames.org/download/archive/>`_.
At this point we assume you can orchestrate your FastAPI and Redis services together 
using docker-compose. For this homework, we are going to add a third service: the
Worker. 

.. note::

   If you want to do this homework with a different data set, e.g. the data set you
   want to work on for your final project, just get it approved with the instructors
   first.



PART 1
~~~~~~

Create two new routes in your FastAPI app, ``/jobs`` and ``/jobs/<jobid>``. These should
be in addition to the existing routes. The routes should satisfy the following requirements:

  * A POST request to ``/jobs`` should create a new job with a unique identifier (uuid)

    * The POST request must include a data packet in JSON format which is stored along
      with the job information (see below)

  * A GET request to ``/jobs`` should list all existing job IDs
  * A GET request to ``/jobs/<jobid>`` should return job information for a given job ID

Following the example in `Unit 08 - Jobs API <../unit08/jobs_api.html>`_,
job IDs should be put into a queue, and job information (e.g. ID, status, user-provided parameters)
should be stored in a separate partition in the Redis database. I highly recommend using the Jobs 
API code from Unit 08 for this.

The POST request to ``/jobs`` should look similar to:

.. code-block:: console

   $ curl localhost:5000/jobs -X POST -d '{"start":1, "end":2}' -H "Content-Type: application/json"

However, ``start`` and ``end`` don't really make sense in the context of the HGNC data, and 
probably don't make sense in the context of your final project data set. Look through the data
you are using for this project and decide what parameters you would ask the user to specify
if they were trying to perform an analysis on a subset of the data. Perhaps a range of gene loci? 
Perhaps a range of HGNC Gene IDs? Perhaps a range of dates? There are many possible choices 
for this. **Provide instructions in your README on what parameters
we should pass to your jobs route. If the user does not provide the right parameters, the route
should not submit a job; instead it should return a message to the user describing what the 
problem is.**



PART 2
~~~~~~

Following the example in `Unit 08 - Messaging Systems <../unit08/messaging.html#exercise-3>`_,
write a Worker Python script that satisfies the following requirements:

  * The Worker should pull methods and clients from the Jobs API
  * It should use the HotQueue ``@q.worker`` decorator to watch the queue and pull off Job IDs as they arrive
  * When it pulls a Job ID off the queue, it should find the corresponding job information in the jobs database,
    update the status to ``"in progress"``, wait for a few seconds, then update the status to ``"complete"``

The Worker needs to be running in a separate container runtime from the FastAPI app. It can use
the same container image as the FastAPI app (except with a different entrypoint command) if desired.
For this homework, the worker does not actually need to do any *real* work - we are just setting
up the infrastructure for now.




PART 3
~~~~~~

In addition to the Python scripts described above, you will need several other files to
support this software system:

**pyproject.toml and uv.lock**: Describe all non-standard Python library dependencies. If you are keeping 
a separate set of uv files for each homework directory, then you should add new versions of these files to 
your homework07 directory. Otherwise, you should update the existing ones at the root of your repository with 
any changes needed. If you are keeping just one copy of the files at the root of your repo, then you can 
temporarily copy the uv files into your homework07 directory to build your docker image(s).

**Dockerfile:** Should install Python dependencies using the uv files and should
copy in Python scripts. I recommend using one Dockerfile to build one Docker image with
all Python scripts inside, then using two different entrypoint commands to either deploy
a FastAPI app or Worker container runtime.

**docker-compose.yml:** Should orchestrate three services together: Redis database, FastAPI
app, Worker. The Redis container needs to be able to write snapshots to a local folder
(you may have to provide some extra instructions here to solve folder permission issues).

Finally, following `Exercise 5 <../unit08/jobs_api.html#exercise-5>`_
from Unit 08, you must use an **environment variable** to dynamically set the Redis host IP.
Environment variables are variables that get set in the shell and are available for programs. In 
Python, the ``os.environ.get()`` method will be helpful. In your docker-compose.yml file, the 
``environment:`` attribute will be required.




PART 4
~~~~~~

Write a README with the standard sections from previous homeworks: there should
be a descriptive title, there should be a high level description of the project,
there should be concise descriptions of the main files within, and you should
be using Markdown styles and formatting to your advantage. We will specifically
be looking for:

* Instructions to use the ``/jobs`` and ``/jobs/<jobid>`` routes
* Instructions to launch the containerized web app
* Give example API query commands and expected outputs in code blocks

Finally, your README should also have a section to describe the data itself. Please
give enough information for others to understand what data they are seeing and
what it means (not every field must be described, just a general overview).
Please cite the data appropriately as well.




What to Turn In
---------------

A sample Git repository may contain the following new files after completing
homework 07 (notice the evolving organization):

.. code-block:: text
   :emphasize-lines: 7-17

   my-coe332-hws/
   ├── homework01/
   │   └── ...
   ├── ...
   ├── homework06/
   │   └── ...
   ├── homework07
   │   ├── Dockerfile
   │   ├── README.md
   │   ├── data
   │   │   └── .gitcanary
   │   ├── docker-compose.yml
   │   └── src
   │       ├── api.py
   │       ├── jobs.py
   │       └── worker.py
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

* `Environment Variables in Docker-compose <https://docs.docker.com/compose/environment-variables/set-environment-variables/>`_ 
* Please find us in the class Slack channel if you have any questions!
