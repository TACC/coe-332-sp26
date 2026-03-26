Messaging Systems
=================

The Queue is a powerful data structure which forms the foundation of many concurrent design patterns. Often these
design patterns center around passing messages between agents within the concurrent system. We will explore one of the
simplest and most useful of these message-based patterns - the so-called "Task Queue". By the end of this module,
students should be able to:

  * Describe the components of a task queue system, and explain how it will be utilized within our 
    FastAPI-based API system architecture.
  * Create task queues in Redis using the ``hotqueue`` library, and work with the ``put()`` and 
    ``consume()`` methods to queue and receive messages across two Python programs. 
  * Use the ``@q.worker`` decorator in ``hotqueue`` to create a simple Python consumer program.
  * Explain the general approach to organizing Python code into different modules and describe how to
    do this for the FastAPI-based API system we are building. 
  * Implement good code organization practices including denoting objects as public or private. 
  * **Design Principles.** The implementation of a task queue incorporates the principle of abstraction, while 
    organizing code into public and private objects demonstrates the use of modularity and encapsulation. 


Task Queues
-----------

In a task queue system,

  * Agents called "producers" write messages to a queue that describe work to be done.
  * A separate set of agents called "consumers" receive the messages and do the work. While work is being done,
    no new messages are received by the consumer.
  * Each message is delivered exactly once to a single consumer to ensure no work is "duplicated".
  * Multiple consumers can be processing "work" messages at once, and similarly, 0 consumers can be processing messages
    at a given time (in which case, messages will simply queue up).

The Task Queue pattern is a good fit for our jobs service.

  * Our FastAPI API will play the role of producer.
  * One or more "worker" programs will play the role of consumer.
  * Workers will receive messages about new jobs to execute and performing the analysis steps.



Task Queues in Redis
--------------------

The ``HotQueue`` class provides two methods for creating a task queue consumer; the first is the ``.consume()`` method
and the second is the ``@q.worker`` decorator.


The Consume Method
~~~~~~~~~~~~~~~~~~

With a ``q`` object defined like ``q = HotQueue('queue', host='<Redis_IP>', port=6379, db=1)``,
the consume method works as follows:

  * The ``q.consume()`` method returns an iterator which can be looped over using a ``for`` loop (much like a list).
  * Each object returned by the iterator is a message received from the task queue.
  * The ``q.consume()`` method blocks (i.e., waits indefinitely) when there are no additional messages in the queue
    arbitrarily named ``queue``.
  

The basic syntax of the consume method is this:

.. code-block:: python3

   for item in q.consume():
       # do something with item

In this case, the ``item`` object is the message that was retrieved from the task queue. 


EXERCISE 1
~~~~~~~~~~

Complete the following on your JetStream VM.

  1. Start a Redis container in the background and expose port 6379.
  2. Open two separate terminals, each logged in to the user VM and running an interactive Python shell.
  3. In each terminal, create a ``HotQueue`` object pointing to the same Redis queue.
  4. In the first terminal, add three or four Python strings to the queue; check the length of the queue.
  5. In the second terminal, use a ``for`` loop and the ``.consume()`` method to print objects in the queue to the screen.
  6. Observe that the strings are printed out in the second terminal.
  7. Back in the first terminal, check the length of the queue; add some more objects to the queue.
  8. Confirm the newly added objects are "instantaneously" printed to the screen back in the second terminal.

A Word on Container Networking 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We'd like to use containers to orchestrate the components of our task queue system. We'll have 
two Python containers representing the producer and consumer components, and we'll have an additional 
Redis container for persisting the queue data. To get this to work, we'll need to address the Redis 
server, running in the last container, from our other two Python containers. To do that, we'll need 
to understand a bit about container networking. 

Docker isolates individual containers at the network level, meaning that each container is uniquely 
addressable with an IP address and a full complement of ports (0-65535). We can see the IP address 
of an individual container using the ``docker inspect <container>`` command:

.. code-block:: console

  [coe332-vm]$ docker inspect 089c14804c9b

  [
      {
          "Id": "089c14804c9bb5a26ec01b6df2a23916a7be83e89326bc5818688097b22b50b5",
          "Created": "2025-03-25T01:24:31.150990988Z",
          "Path": "sleep",
          "Args": [
              "999999"
          ],
          "State": {
    . . .   

The output is a JSON-formatted documented with many details about the container. At the bottom 
is a stanza called ``NetworkSettings`` which contains a stanza ``Networks`` with an entry for 
each network that the container has been connected to. For example: 


.. code-block:: console
  :emphasize-lines: 10

            "Networks": {
                "bridge": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": null,
                    "MacAddress": "02:42:ac:11:00:02",
                    "NetworkID": "6200fb8b8e549f9421dc04bce67cdeca2dead6b78651c8ee92061fc22fb77c56",
                    "EndpointID": "0752c7d43fd567bcf5f402048f95c73a96874904188640e44c7bcadb462eb2c7",
                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "DriverOpts": null,
                    "DNSNames": null
                }

The output shows that the container is connected to a single network called ``bridge`` and the 
container has an IP address of ``172.17.0.2`` on this network.

So what is the ``bridge`` network anyway?
To keep containerized services secure, by default, Docker utilizes a virtualized network, called a 
*bridge network*, also referred to as the *docker0* bridge. Our container's IP address resides on 
this bridge network, and, by default, this network is not exposed outside of our host VM. In other
words, the ``172.17.0.2`` IP address is only accessible from our VM. 

We can see this interface using the Linux command ``ip addr``. This command outputs every 
network interface available on the host and its associated IP address. 

.. code-block:: console

  [coe332-vm]$ ip addr 

  1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
      link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
      inet 127.0.0.1/8 scope host lo
        valid_lft forever preferred_lft forever
      inet6 ::1/128 scope host noprefixroute 
        valid_lft forever preferred_lft forever
  . . .

  3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:67:98:46:a0 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:67ff:fe98:46a0/64 scope link 
       valid_lft forever preferred_lft forever
  . . .

This output shows that the docker0 bridge is configured with the IP address ``172.17.0.1``. 

When we publish a port on a container, for example, using the ``-p`` flag to the ``docker run`` 
command, we are asking Docker to connect the port on our container's IP address on the bridge network 
to the port on the docker0 bridge itself, as well as to other host network interfaces 
(e.g., the eth0, enp3s0, etc.).
This means that, when publishing a container port, one can use either the container IP address 
or the docker0 address (or another host network IP) to connect to the port. The benefit of using 
the docker0 address is that it is stable, while the container IP address changes each time 
we start the container. 

**Services in Docker Compose.** Finally, in the case where we have defined services using docker-compose, 
Docker takes one more step and configures the service name to map to the IP address of the container within
other containerized services defined within the compose file. Note that this is only for those services defined 
within the compose file, and so attempting to use the service name on the host or within other containers 
will fail to resolve. 


Finally, we underscore that all of this Docker networking is typically restricted to the individual server (e.g., VM)
running Docker. When we discuss Kubernetes, we will further expand upon these ideas to allow ports on containerized 
services to be connected to and from other containers running across a cluster of machines. 


EXERCISE 2
~~~~~~~~~~

Repeat the steps in Exercise 1, but this time orchestrate three containers together 
using ``docker-compose``: a Redis container and two other Python containers which may simulate, 
for example, a FastAPI app and a worker. 

.. note:: 

  Before starting the containers defined in the ``docker-compose.yml`` file, make sure to create a directory 
  called ``data`` in the current directory. 


.. code-block:: yaml

   services:
       redis-db:
           image: redis:7
           volumes:
               - ./data:/data
           ports:
               - 6379:6379
           user: "1000:1000"
           command: ["--save", "1", "1"]
       python1:
           image: python:3.14
           command: ["sleep", "9999999"]
       python2:
           image: python:3.14
           command: ["sleep", "9999999"]


Use the above ``docker-compose.yml`` file (make sure you understand what each part is doing), and execute 
the command:

.. code-block:: console

   [coe332-vm]$ docker compose up -d
   Creating network "messaging_default" with the default driver
   Creating messaging_redis-db_1 ... done
   Creating messaging_python2_1  ... done
   Creating messaging_python1_1  ... done


Once the containers are running, use ``docker ps -a`` to find the names of the container, and ``docker exec``
to create two new shells inside the running containers:

.. code-block:: console

   # From terminal 1
   [coe332-vm]$ docker exec -it messaging_python1_1 /bin/bash
   root@ba734c20dfe3:/#

.. code-block:: console

   # From terminal 2
   [coe332-vm]$ docker exec -it messaging_python2_1 /bin/bash
   root@22ca40c5cf18:/# 


.. note::

   Once inside the running containers, what IP / alias do you use to refer to the Redis container?
   What libraries might you have to install?

   Since these are just throw-away containers, you can use ``pip`` to install these packages. 

When finished with the exercise, clean up your running containers by doing:

.. code-block:: console

   [coe332-vm]$ docker-compose down
   Stopping messaging_python2_1  ... done
   Stopping messaging_python1_1  ... done
   Stopping messaging_redis-db_1 ... done
   Removing messaging_python2_1  ... done
   Removing messaging_python1_1  ... done
   Removing messaging_redis-db_1 ... done
   Removing network messaging_default


The @q.worker Decorator
~~~~~~~~~~~~~~~~~~~~~~~

Given a HotQueue queue object, ``q``, the ``@q.worker`` decorator is a convenience utility to turn a function into a consumer
without having to write a for loop. The basic syntax is:

.. code-block:: python3

   >>> @q.worker
   >>> def do_work(item):
   >>>     # do something with item

In the example above, ``item`` will be populated with the item dequeued.

Then, to start consuming messages, simply call the function:

.. code-block:: python

    >>> do_work()
    # ... blocks until new messages arrive

.. note::

  The ``@q.worker`` decorator replaces the ``for`` loop. Once you call a function decorated with ``@q.worker``, the
  code never returns unless there is an unhandled exception.


EXERCISE 3
~~~~~~~~~~

Write a function, ``echo(item)``, to print an item to the screen, and use the ``@q.worker`` decorator to
turn it into a consumer. Call your echo function in one terminal and in a separate terminal, send messages to the
Redis queue. Verify that the message items are printed to the screen in the first terminal.

In practice, we will use the ``@q.worker`` in a Python source file like so --

.. code-block:: python

   # A simple example of Python source file, worker.py
   q = HotQueue('queue', host='<Redis_IP>', port=6379, db=1)

   @q.worker
   def do_work(item):
       # do something with item...

   do_work()


Assuming the file above was saved as ``worker.py``, calling ``python worker.py`` from the shell would result in a
non-terminating program that "processed" the items in the ``"queue"`` queue using the ``do_work(item)`` function.
The only thing that would cause our worker to stop is an unhandled exception.


Additional Resources
--------------------

* `HotQueue <https://pypi.org/project/hotqueue/>`_
