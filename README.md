# Django Redis Demo
## Installation Steps
1. [Install Python](https://www.python.org/downloads/)
2. [Install Docker](https://docs.docker.com/get-docker/)
3. [Install Node.js](https://nodejs.org/en/download/)
4. Clone the repository:
    ```
    git clone git@github.com:carogomezt/django-redis-demo.git
    ```
5. Go to the project folder and create a new virtual environment:
    ```
    mkdir django-redis-demo
    python3 -m venv venv
    source venv/bin/activate
    ```
6. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```
7. Run the migrations:
   ```
   python manage.py migrate
   ```
8. Create a super user:
   ```
   python manage.py createsuperuser
   ```
9. To test if everything was installed right, run the app and see that it shows some content:
   ```
   python manage.py run server
   ```
_Note: If you have Redis installed locally you could skip the next step._

10. Stop the running app and run the docker image, we are using here a docker image of Redis to avoid additional installations:
   ```
   docker-compose up
   ```

## Caching Configuration
You could see that the cache is defined under `django_cache/settings.py`. Here you could define your caching service, in our case is Redis:
```
CACHES = {
     "default": {
         "BACKEND": "django_redis.cache.RedisCache",
         "LOCATION": "redis://redis:6379/",
         "OPTIONS": {
             "CLIENT_CLASS": "django_redis.client.DefaultClient"
         },
     }
 }
```
The reason why we installed `django-redis` is because it will act as a client that will abstract the communication we have with Redis.
### Cached View
Under `store/views.py` you could see that we have two views, the first one is the products view which calls the database every time that we want to return all products. 
The second view is the one who uses caching, here we check if the caching key is saved, if that is not the case it retrieves the data from the database and save it in the caching system, 
it uses the default time out of 300 seconds which is 5 minutes.
- Normal view: http://localhost:8000/products
- Cached View: http://localhost:8000/cached_products
### Testing
To test these APIs we have to conduct a load test. I will be using a npm package called loadtest.

You can install loadtest globally using this command:
```
sudo npm install -g loadtest
```
Once that is done, let's test our non-cached API. Run the command:
```
loadtest -n 100 -k http://localhost:8000/products
```
After running that command we could see the following result:
```
INFO Completed requests:  100
INFO Total errors:        0
INFO Total time:          2.547047284 s
INFO Requests per second: 39
INFO Mean latency:        25.1 ms
```
This means that our API can handle only 39 requests per second.

Let's test the cached API.
```
loadtest -n 100 -k http://localhost:8000/cached_products
```
After running that command we could see the following result:
```
INFO Completed requests:  100
INFO Total errors:        0
INFO Total time:          1.413555047 s
INFO Requests per second: 71
INFO Mean latency:        13.9 ms
```
The result is much better, almost double the amount of requests.
Why is this possible?, Because the first time you hit the cache endpoint the application will query the information 
from the database but subsequent calls to the same URL will bypass the database and query from the cache because the data is
already available.

If you want to see the keys in Redis you could open the Redis CLI and check it:
```
redis-cli
127.0.0.1:6379> KEYS *
```

### Additional resources 
- [Effortless API Request Caching with Python & Redis](https://rednafi.github.io/digressions/python/database/2020/05/25/python-redis-cache.html)
- [Django caching using Redis](https://tamerlan.dev/django-caching-using-redis/)
- [How to Cache Using Redis in Django Applications](https://code.tutsplus.com/tutorials/how-to-cache-using-redis-in-django-applications--cms-30178)
- [Hands-on with Redis and Django](https://enlear.academy/hands-on-with-redis-and-django-ed7df9104343)
- [Redis](https://redis.io/)
- [Caching Overview](https://aws.amazon.com/caching/)

