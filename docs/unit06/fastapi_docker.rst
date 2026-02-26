Containerizing FastAPI
======================

As we have discussed previously, Docker containers are critical to packaging an
application along with all of its dependencies, isolating it from
other applications and services, and deploying it in a consistent and reproducible
way across different platforms.

Here, we will walk through the process of containerizing a FastAPI application with Docker, and then
using ``curl`` to interact with it as a containerized microservice. After going through this
module, students should be able to:

* Assemble the different components needed for a containerized microservice into on directory.
* Leverage ``uv`` for dependency management (i.e., for Python packages) for the project.
* Build and run in the background a containerized FastAPI microservice.
* Map ports on the Jetstream VM to ports inside a container, and use ``curl`` with the
  the correct ports to make requests to and generate responses from the microservice.
* Deploy the microservice with docker compose
* **Design Principles:** By combining FastAPI and Docker, we will see how both contribute to
  the *modularity*, *portability*, *abstraction*, and *generalization* of software (all
  four major design principles).

Build a Docker Image
--------------------

As we saw in a previous section, we write up the recipe for our application
installation process in a Dockerfile. Fortunately, we'll be able to Leverage ``uv``
to make the installation straight-forward.

Create a file called ``Dockerfile`` for our
FastAPI microservice and add the following lines:

.. code-block:: dockerfile
    :linenos:

    FROM python:3.14

    # COPY the uv binary
    COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

    # Copy the project files
    RUN mkdir /app
    COPY pyproject.toml /app
    COPY .python-version /app
    COPY uv.lock /app

    # Sync the project into a new environment, asserting the lockfile is up to date
    WORKDIR /app
    RUN uv sync --locked

    # Add the actual app -- do this after syncing to preserve the cache
    COPY fastapi/main.py /app

    CMD ["uv", "run", "--", "fastapi", "dev",  "--host", "0.0.0.0", "main.py"]

In the above Dockerfile, on line 1 use a Python official image -- version 3.14 -- that matches 
our project's Python. We then copy the ``uv`` binary using the ``uv``-project's official 
docker image (line 3). On lines 7-10 we create a directory ``/app`` in the container image 
and copy our project's ``uv`` files there. Note that we do **NOT** copy our application file (the ``main.py``) 
yet, so that the Docker image cache is not busted every time we change our ``main.py`` file.
The ``uv sync --locked`` command on line 14
syncs the project into a new environment, asserting the lockfile is up to date. 
Finally, we add out ``main.py`` file to the image on line 17 and then specify the default command 
at line 19. 

Save the file and build the image with the following command:

.. code-block:: console

   [coe332-vm]$ docker build -t <username>/coe332sp26-fastapi:1.0 .

.. warning:

   Don't forget to replace ``<username>`` with your Docker Hub username.

Run a Docker Container
----------------------

To create an instance of your image (a "container"), use the following command:

.. code-block:: console

   [coe332-vm]$ docker run --name "api" -d -p 8000:8000 <username>/coe332sp26-fastapi:1.0

The ``-d`` flag detaches your terminal from the running container - i.e. it
runs the container in the background. The ``-p`` flag maps a port on the Jetstream
VM (8000, in the above case) to a port inside the container (again 8000, in the
above case). In the above example, the FastAPI app was set up to use the
default port inside the container (8000), and we can access that through our
specified port on Jetstream (8000). This explicit mapping is convenient if you 
have multiple services running on the same VM and you want to avoid port
collisions. 

Check to see that things are up and running with:

.. code-block:: console

   [coe332-vm]$ docker ps -a

The list should have a container with the name you gave it, an ``UP`` status,
and the port mapping that you specified.

If the above is not found in the list of running containers, try to debug with
the following:

.. code-block:: console

   [coe332-vm]$ docker logs "your-container-name"
   -or-
   [coe332-vm]$ docker logs "your-container-ID"


Access Your Microservice
------------------------

Now for the payoff - you can use ``curl`` to interact with your FastAPI microservice by specifying
the correct port. Following the example above, which was using
port 8000:

.. code-block:: console

   [coe332-vm]$ curl localhost:8000/
   Hello, world!
   [coe332-vm]$ curl localhost:8000/Joe
   Hello, Joe!


Clean Up
--------

Finally, don't forget to stop your running container and remove it.

.. code-block:: console

   CONTAINER ID   IMAGE                                 COMMAND           CREATED         STATUS         PORTS                                       NAMES
   a785237628d6   jstubbs/coe332sp26-fastapi   "uv run -- fastapi d…"    4 minutes ago   Up 4 minutes   0.0.0.0:5000->5000/tcp, :::8000->8000/tcp     api
   [coe332-vm]$ docker stop a785237628d6
   a785237628d6
   [coe332-vm]$ docker rm a785237628d6
   a785237628d6

EXERCISE
~~~~~~~~

Containerize your FastAPI degrees app from last week:

1. Create a Dockerfile for your app
2. Build the image from the Dockerfile
3. Run the server locally and test the endpoints using curl


Docker Compose, Revisited
-------------------------

Using the ``docker run`` command to start containers is OK for simple commands, but as 
we started to see in the previous material, the commands can get long pretty quickly. It can be
hard to remember all of the flags and options that we want to use when starting our
containers. 

Moreover, so far we have been looking at single-container applications. 
But what if we want to do something more complex involving multiple containers? In this course, 
our goal is to ultimately develop and orchestrate a multi-container
application consisting of, e.g., a Flask app, a database, a message queue, an
authentication service, and more.


Write a Compose File
--------------------

Docker compose works by interpreting rules declared in a YAML file (typically
called ``docker-compose.yml``). The rules we will write will replace the
``docker run`` commands we have been using, and which have been growing quite
complex. Recall from the past exercise that the command we were using to start our FastAPI 
application container looked like the following:

.. code-block:: console

   [coe332-vm]$ docker run --name "api" -d -p 8000:8000 jstubbs/coe332sp26-fastapi

The above ``docker run`` command can be translated into a YAML file.
Navigate to the folder that contains your Python scripts and Dockerfiles, then
create a new empty file called ``docker-compose.yml`` and paste in the following text:

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 8

   ---

   services:
       api:
           build:
               context: ./
               dockerfile: ./Dockerfile
           image: <username>/coe332sp26-fastapi
           container_name: api
           ports:
               - "8000:8000"


.. note::

   Be sure to update the highlighted line above with your username.


The ``services`` section defines the configuration of individual container
instances that we want to orchestrate. In our case, we define just one service
called ``api``. We can use any allowable name for the services we defined, but each
name should be unique within the docker-compose.yml file. 

The ``api`` service is configured with its own Docker image, including a
reference to a Dockerfile to be used to ``build`` the image, a recognizable name
for the running container, and a port mapping for the FastAPI service. Recall from
the `previous unit <../unit05/docker_compose.html>`_ that other speicifcations
can be defined in this file including a list of mounted volumes, user IDs for
running the service, default commands, and many others. The choice of which 
options to use entirely depends on the app and the context.

.. note::

   The top-level ``services`` keyword shown above is just one important part of
   Docker compose. Later in this course we will look at named volumes and
   networks which can be configured and created with Docker compose.


Running Docker Compose
----------------------

To run our FastAPI application container, we simply use the ``docker compose up`` 
verb, which will start up all containers defined in the file. Alternatively,
we could use ``docker compose run`` and pass the name of a service to run, in this
case, ``api``:

.. code-block:: console

   [coe332-vm]$ docker compose up 
    WARN[0000] No services to build                         
    [+] up 2/2
    ✔ Network prep_default Created                                                                                                            0.1s 
    ✔ Container api        Created                                                                                                            0.1s 
    Attaching to api
    api  | 
    api  |    FastAPI   Starting development server 🚀
    api  |     
    . . .


Note that ``docker compose`` starts the container in the foreground and takes over our terminal. If we use 
``Ctrl+C`` we will stop the container. We can see confirm that the container is stopped using the
``docker ps -a`` command:

.. code-block:: console

   [coe332-vm] docker ps -a 
    CONTAINER ID   IMAGE                        COMMAND                  CREATED              STATUS                     PORTS     NAMES
    ec3a591746d5   jstubbs/coe332sp26-fastapi   "uv run -- fastapi d…"   About a minute ago   Exited (0) 3 seconds ago             api

To start the service in the background, use the ``-d`` flag:

.. code-block:: console

   [coe332-vm]$ docker compose up -d

Once the service is running, perform some curl commands to test the running Flask
app before stopping the service with:


.. code-block:: console

   [coe332-vm]$ docker compose down



Essential Docker Compose Command Summary
----------------------------------------

+------------------------+------------------------------------------------+
| Command                | Usage                                          |
+========================+================================================+
| docker compose version | Print version information                      |
+------------------------+------------------------------------------------+
| docker compose config  | Validate docker-compose.yml syntax             |
+------------------------+------------------------------------------------+
| docker compose up      | Spin up all services                           |
+------------------------+------------------------------------------------+
| docker compose down    | Tear down all services                         |
+------------------------+------------------------------------------------+
| docker compose build   | Build the images listed in the YAML file       |
+------------------------+------------------------------------------------+
| docker compose run     | Run a container as defined in the YAML file    |
+------------------------+------------------------------------------------+



Additional References
----------------------

* `Using uv with Docker <https://docs.astral.sh/uv/guides/integration/docker/>`_