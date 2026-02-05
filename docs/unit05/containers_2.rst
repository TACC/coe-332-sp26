Advanced Containers
===================

In the first part, we pulled and ran existing container images from Docker Hub.
In this section, we will build an image from scratch for running some of our own
Python3 code. Then, we will push that image back up to Docker Hub so others may
find and use it. After going through this module, students should be able to:

* Install and test code in a container interactively
* Write a Dockerfile from scratch
* Build a Docker image from a Dockerfile
* Push a Docker image to Docker Hub
* Volume mount external data inside a Docker container
* **Design Principles:** Containers contribute to the portability of software projects


Getting Set Up
--------------

*Scenario:* You are a developer who has written some code for reading and
parsing meteorite landing data in JSON format. You now want to distribute that
code for others to use in what you know to be a stable production environment
(including OS and dependency versions). End users may want to use this application
on their local workstations, in the cloud, or on an HPC cluster.


The first step in a typical container development workflow entails installing
and testing an application interactively within a running Docker container.

.. note::

   We recommend doing this on your VMs. But, one of the most
   important features of Docker is that it is platform agnostic. These steps
   could be done anywhere Docker is installed.


To begin, make a new folder for this work and prepare to gather some important
files.


.. code-block:: console

   [coe332-vm]$ mkdir -p coe-332/docker-exercise/
   [coe332-vm]$ cd coe-332/docker-exercise/
   [coe332-vm]$ pwd
   /home/ubuntu/coe-332/docker-exercise

Specifically, you need your ``ml_data_analysis.py`` script and the input data
file called ``Meteorite_Landings.json``. You can make copies of your own, our
download sample copies from the links below. You also need a ``Dockerfile``, and
we can just make an empty one with no contents for now.

.. code-block:: console

   [coe332-vm]$ pwd
   /home/ubuntu/coe-332/docker-exercise
   [coe332-vm]$ touch Dockerfile
   [coe332-vm]$ wget https://raw.githubusercontent.com/tacc/coe-332-sp26/main/docs/unit05/scripts/Meteorite_Landings.json
   [coe332-vm]$ wget https://raw.githubusercontent.com/tacc/coe-332-sp26/main/docs/unit05/scripts/ml_data_analysis.py
   [coe332-vm]$ wget https://raw.githubusercontent.com/tacc/coe-332-sp26/main/docs/unit05/scripts/models.py
   [coe332-vm]$ ls
   Dockerfile  Meteorite_Landings.json  ml_data_analysis.py

.. warning::

   It is important to carefully consider what files and folders are in the same
   ``PATH`` as a Dockerfile (known as the 'build context'). The ``docker build``
   process will index and send all files and folders in the same directory as
   the Dockerfile to the Docker daemon, so take care not to ``docker build`` at
   a root level.


Containerize Code Interactively
-------------------------------

There are several questions you must ask yourself when preparing to containerize
code for the first time:

1. What is an appropriate base image?
2. What dependencies are required for my program?
3. What is the installation process for my program?
4. What environment variables may be important?

We can work through these questions by performing an **interactive installation**
of our Python script. Our development environment (e.g. the Jetstream VM)
is a Linux server running Ubuntu 24.04 and Python 3.14. We know our code works there,
so that is how we will containerize it. Use ``docker run`` to interactively attach to a fresh
`Python 3.14 container <https://hub.docker.com/_/python/tags?name=3.14>`_.

.. code-block:: console

   [coe332-vm]$ docker run --rm -it -v $PWD:/code python:3.14 /bin/bash
   root@7ad568453e0b:/#

Here is an explanation of the options:

.. code-block:: text

   docker run       # run a container
   --rm             # remove the container on exit
   -it              # interactively attach terminal to inside of container
   -v $PWD:/code    # mount the current directory to /code
   ubuntu:20.04     # image and tag from Docker Hub
   /bin/bash        # shell to start inside container


The command prompt will change, signaling you are now 'inside' the container.
And, new to this example, we are using the ``-v`` flag which mounts the contents
of our current directory (``$PWD``) inside the container in a folder in the root
directory called (``/code``).


Check for and Install Necessary Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first thing we will typically do is check if our dependenices are available
in the container. If they are not available, we will use a package manager to 
install them. To run our Meterorite Landing code, we just need Python3 and
a few simple Python libraries, which can be managed through ``uv``.

.. code-block:: console

   root@edd3bf9e45ab:/# which python3
   /usr/local/bin/python3
   root@edd3bf9e45ab:/# python3 --version
   Python 3.14

Python3 is available in this container (as expected). But what about ``uv``? Run ``uv``
in your terminal and you will see output like the following:

.. code-block:: console

   root@91b9c9caa283:/# uv
   bash: uv: command not found

We can see that ``uv`` is not installed in this (or any) python base imgae by default. Let's
install in our container just as we did at the beginning of the course

Run the following inside of your container to install ``uv``

.. code-block:: console  

   root@91b9c9caa283:/# curl -LsSf https://astral.sh/uv/install.sh | sh

and make sure that we add it to our **$PATH**

.. code-block:: console  

   root@91b9c9caa283:/# source $HOME/.local/bin/env

Run ``uv help`` to ensure you have correctly installed it

.. code-block:: console  

   root@91b9c9caa283:/# uv help
   An extremely fast Python package manager.

   Usage: uv [OPTIONS] <COMMAND>

   Commands:
   auth                       Manage authentication
   run                        Run a command or script
   init                       Create a new project
   ...

    
Now that ``uv`` is install, let's initialize a uv environment in our ``/code`` directory
and install the libraries our ``ml_data_analysis.py`` script depends on.

.. code-block:: console  

   root@91b9c9caa283:/# uv init ./code

``cd`` into the ``./code`` directory.

.. code-block:: console  

   root@91b9c9caa283:/# cd ./code

Add the packages

.. code-block:: console  

   root@91b9c9caa283:/code# uv add pydantic pytest

Now that we have set up the container with the same packages as our VM, Let's run
our ml_data_analysis script and see if it works:

.. code-block:: console  

   root@91b9c9caa283:/code# uv run python ml_data_analysis.py 
   83857.3
   Northern & Eastern
   Northern & Eastern
   Northern & Western
   Northern & Western
   ...

It works!

.. warning::

   An important question to ask is: Does the versions of Python and other
   dependencies match the versions you are developing with in your local
   environment? If not, make sure to install the correct version of Python.



Install and Test Your Code
~~~~~~~~~~~~~~~~~~~~~~~~~~

At this time, we should make a small edit to the code that will make it a little
more flexible and more amenable to running in a container. Instead of hard coding
the filename ``Meteorite_Landings.json`` in the script, let's make a slight
modification so we can pass the filename on the command line. In the script, add
this line near the top of ``ml_data_analysis.py``:


.. code-block:: python3

   import sys

And change the ``with open...`` statements to these, as appropriate:

.. code-block:: python3

   with open(sys.argv[1], 'r') as f:
       ml_data = json.load(f)




.. note::

   You may need to install your favorite text editor with something like:

   .. code-block:: console

      root@edd3bf9e45ab:/# apt-get update
      root@edd3bf9e45ab:/# apt-get install vim

We now have functional versions of our script 'installed' in this container.
Now would be a good time to execute the `history` command to see a record of the
build process. When you are ready, type `exit` to exit the container and we can
start writing these build steps into a Dockerfile.


Assemble a Dockerfile
---------------------

After going through the build process interactively, we can translate our build
steps into a Dockerfile using the directives described below. Open up your copy
of ``Dockerfile`` with a text editor and enter the following:


The FROM Instruction
~~~~~~~~~~~~~~~~~~~~

We can use the FROM instruction to start our new image from a known base image.
This should be the first line of our Dockerfile. In our scenario, we want to
match our development environment with Python3.14. We know our code works in
that environment, so that is how we will containerize it for others to use:

.. code-block:: dockerfile

   FROM python:3.14 

Base images typically take the form `os:version`. Avoid using the '`latest`'
version; it is hard to track where it came from and the identity of '`latest`'
can change.

.. tip::

   Browse `Docker Hub <https://hub.docker.com/>`_ to discover other potentially
   useful base images. Keep an eye out for the 'Official Image' badge.


The RUN Instruction
~~~~~~~~~~~~~~~~~~~

We can install updates, install new software, or download code to our image by
running commands with the RUN instruction. In our case, our dependencies
were Python3 (built into our base image), ``uv``, ``pydantic``, and ``pytest`` (not using this yet). So, we will use a RUN instruction to
install anything that is missing. The containerized version of ``uv`` is a little different that our local installation. Document can be found
`here <https://docs.astral.sh/uv/guides/integration/docker/#installing-uv>`_ 

.. code-block:: dockerfile

   # Download the latest installer
   ADD https://astral.sh/uv/install.sh /uv-installer.sh

   # Run the installer then remove it
   RUN sh /uv-installer.sh && rm /uv-installer.sh

   # Ensure the installed binary is on the `PATH`
   ENV PATH="/root/.local/bin/:$PATH"

   # Initialize a uv project
   RUN uv init /code

   # NOTE: The WORKDIR instruction sets the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions that follow it in the Dockerfile
   WORKDIR /code

   RUN uv add pydantic pytest


Each RUN instruction creates an intermediate image (called a 'layer'). Too many
layers makes the Docker image less performant, and makes building less
efficient. We can minimize the number of layers by combining RUN instructions.
Dependencies that are more likely to change over time (e.g. Python3 libraries)
still might be better off in in their own RUN instruction in order to save time
building later on.



The COPY Instruction
~~~~~~~~~~~~~~~~~~~~

There are a couple different ways to get your source code inside the image. One
way is to use a RUN instruction with ``wget`` to pull your code from the web.
When you are developing, however, it is usually more practical to copy code in
from the Docker build context using the COPY instruction. For example, we can
copy our script to the root-level ``/code`` directory with the following
instructions:

.. code-block:: dockerfile

   COPY ml_data_analysis.py /code/ml_data_analysis.py

   COPY models.py /code/models.py

The ENV Instruction
~~~~~~~~~~~~~~~~~~~

Another useful instruction is the ENV instruction. This allows the image
developer to set environment variables inside the container runtime. In our
interactive build, we added the ``/code`` folder to the ``PATH``. We can do this
with ENV instructions as follows:

.. code-block:: dockerfile

   ENV PATH="/code:$PATH"



Putting It All Together
~~~~~~~~~~~~~~~~~~~~~~~

The contents of the final Dockerfile should look like:

.. code-block:: dockerfile
   :linenos:

   FROM python:3.14

   # Download the latest installer
   ADD https://astral.sh/uv/install.sh /uv-installer.sh

   # Run the installer then remove it
   RUN sh /uv-installer.sh && rm /uv-installer.sh

   # Ensure the installed binary is on the `PATH`
   ENV PATH="/root/.local/bin/:$PATH"

   # Initialize a uv project
   RUN uv init /code

   # NOTE: The WORKDIR instruction sets the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions that follow it in the Dockerfile
   WORKDIR /code

   RUN uv add pydantic pytest

   COPY ml_data_analysis.py /code/ml_data_analysis.py

   COPY models.py /code/models.py


Build the Image
---------------

Once the Dockerfile is written and we are satisfied that we have minimized the
number of layers, the next step is to build an image. Building a Docker image
generally takes the form:

.. code-block:: console

   [coe332-vm]$ docker build -t <dockerhubusername>/<code>:<version> ./

The ``-t`` flag is used to name or 'tag' the image with a descriptive name and
version. Optionally, you can preface the tag with your **Docker Hub username**.
Adding that namespace allows you to push your image to a public registry and
share it with others. The trailing dot '``.``' in the line above simply
indicates the location of the Dockerfile (a single '``.``' means 'the current
directory').

To build the image, use:

.. code-block:: console

   [coe332-vm]$ docker build -t username/ml_data_analysis:1.0 ./

.. note::

   Don't forget to replace 'username' with your Docker Hub username.


Use ``docker images`` to ensure you see a copy of your image has been built. You can
also use `docker inspect` to find out more information about the image.

.. code-block:: console

   [coe332-vm]$ docker images
   REPOSITORY                 TAG        IMAGE ID       CREATED              SIZE
   username/ml_data_analysis  1.0        2883079fad18   About a minute ago   446MB
   ...

.. code-block:: console

   [coe332-vm]$ docker inspect username/ml_data_analysis:1.0


If you need to rename your image, you can either re-tag it with ``docker tag``, or
you can remove it with ``docker rmi`` and build it again. Issue each of the
commands on an empty command line to find out usage information.



Test the Image
--------------

We can test a newly-built image two ways: interactively and non-interactively.
In interactive testing, we will use ``docker run`` to start a shell inside the
image, just like we did when we were building it interactively. The difference
this time is that we are NOT mounting the code inside with the ``-v`` flag,
because the code is already in the container:

.. code-block:: console

   [coe332-vm]$ docker run --rm -it username/ml_data_analysis:1.0 /bin/bash

   root@c5cf05edddcd:/code# uv run ml_data_analysis.py Meteorite_Landings.json
   Traceback (most recent call last):
     File "/code/ml_data_analysis.py", line 96, in <module>
       main()
     File "/code/ml_data_analysis.py", line 82, in main
       with open(sys.argv[1], 'r') as f:
   FileNotFoundError: [Errno 2] No such file or directory: 'Meteorite_Landings.json'

Here is an explanation of the options:

.. code-block:: text

   docker run      # run a container
   --rm            # remove the container when we exit
   -it             # interactively attach terminal to inside of container
   username/...    # image and tag on local machine
   /bin/bash       # shell to start inside container


Uh oh! We forgot about ``Meteorite_Landings.json``! We get a FileNotFoundError
in Python3. This is because we did not (1) copy the JSON file into the container
at build time, nor did we (2) copy the JSON file into the container at run
time.

We should pause at this moment to think about how we want to distribute this
application. Should the data be encapsulated within? Or should we expect potential
users to be bring their own data for analysis?

Let's try again, but this time mount the data inside the container so we can
access it. If we mount the current folder as, e.g., ``/data``, then everything
in the current folder will be available. In addition, if we write any new files
inside the container to ``/data``, those will be preserved and persist outside
the container once it stops.

.. code-block:: console

   [coe332-vm]$ docker run --rm -it -v $PWD/Meteorite_Landings.json:/data/Meteorite_Landings.json username/ml_data_analysis:1.0 /bin/bash
   ...
   ### Same command as above, but easier to read:
   [coe332-vm]$ docker run --rm \
                         -it \
                         -v $PWD/Meteorite_Landings.json:/data/Meteorite_Landings.json \
                         username/ml_data_analysis:1.0 \
                         /bin/bash
   
   root@dc0d6bf1875c:/# pwd
   /
   root@dc0d6bf1875c:/# ls /data
   Meteorite_Landings.json
   root@dc0d6bf1875c:/# ls /code
   ml_data_analysis.py
   root@dc0d6bf1875c:/# ml_data_analysis.py /data/Meteorite_Landings.json
   83857.3
   Northern & Eastern
   ... etc



Everything looks like it works now! Next, exit the container and test the code
non-interactively. Notice we are calling the container again with ``docker run``,
but instead of specifying an interactive (``-it``) run, we just issue the command
as we want to call it on the command line. Also, notice the return of the ``-v``
flag, because we need to create a volume mount so that our data
(``Meteorite_Landings.json``) is available inside the container.

.. code-block:: console

   [coe332-vm]$ docker run --rm \
                         -v $PWD/Meteorite_Landings.json:/data/Meteorite_Landings.json \
                         username/ml_data_analysis:1.0 \
                         ml_data_analysis.py /data/Meteorite_Landings.json
   Northern & Eastern
   ... etc

Much simpler and cleaner! Our only local dependencies are the Docker runtime and
some input data that we provide. Then we pull and run the image, mounting our
data inside the container and executing the embedded Python3 script. Anyone with
their own data could follow our same steps to replicate our work in their own
environments.



Share Your Docker Image
-----------------------

Now that you have containerized, tested, and tagged your code in a Docker image,
the next step is to disseminate it so others can use it.

Docker Hub is the *de facto* place to share an image you built. Remember, the
image must be name-spaced with either your Docker Hub username or a Docker Hub
organization where you have write privileges in order to push it:

.. code-block:: console

   [coe332-vm]$ docker login
   ...
   [coe332-vm]$ docker push username/ml_data_analysis:1.0


You and others will now be able to pull a copy of your container with:

.. code-block:: console

   [coe332-vm]$ docker pull username/ml_data_analysis:1.0


As a matter of best practice, it is highly recommended that you store your
Dockerfiles somewhere safe. A great place to do this is alongside the code
in, e.g., GitHub. GitHub also has integrations to automatically update your
image in the public container registry every time you commit new code. (More on
this later in the semester).

For example, see: `Publishing Docker Images <https://docs.github.com/en/actions/publishing-packages/publishing-docker-images/>`_




Additional Resources
--------------------

* `Docker for Beginners <https://training.play-with-docker.com/beginner-linux/>`_
* `Play with Docker <https://labs.play-with-docker.com/>`_
