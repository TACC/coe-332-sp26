Writing Tests for FastAPI
-------------------------

There are several different approaches for writing *tests* for FastAPI servers,
some of which are included in the FastAPI documentation. The approach I like the
best, and which is most congruent with the topics we already covered in this class,
is to instead write *integration tests*. 

For these tests, the key thing is that you have to have an actual copy of your
FastAPI server running. Then, the tests will perform ``requests.get()``, 
``requests.post()``, etc., to the various
routes in your server, and the tests can evaluate the responses and assert the desired 
behavior and properties. Be careful to make sure that your tests
are independent of the data, which may change over time. The job of these
tests is not to check / validate that the right data is being returned; rather,
the goal is to make sure the routes work and return the right kind of response.

If your code also has standalone functions separate from the functions decorated
as FastAPI routes, (e.g., in the case of the ISS data you may have written
standalone functions for finding the time closest to now or computing average
speed that are called from other functions), then you would still want to import
those and test them as normal in your test file.

Consider the following pytest snippet that tests the /epochs and /epochs/<epoch>
routes for the ISS tracker:


.. code-block:: python3
   :linenos:

   import pytest
   import requests

   response1 = requests.get('http://127.0.0.1:8000/epochs')
   a_representative_epoch = response1.json()[0]
   response2 = requests.get('http://127.0.0.1:8000/epochs/'+a_representative_epoch)

   def test_epochs_route():
       assert response1.status_code == 200
       assert isinstance(response1.json(), list) == True

   def test_specific_epoch_route():
       assert response2.status_code == 200
       assert isinstance(response2.json(), dict) == True



These lines may need to be modified depending on the format of data returned by
your API. And, as mentioned above, it assumes these tests are performed when your
API is already running.