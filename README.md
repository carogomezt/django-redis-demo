# Django Redis Demo
## Installation Steps
1. [Install Python](https://www.python.org/downloads/)
2. [Install Docker](https://docs.docker.com/get-docker/)
3. Clone the repository:
    ```
    git clone git@github.com:carogomezt/django-redis-demo.git
    ```
4. Go to the project folder and create a new virtual environment:
    ```
    mkdir django-redis-demo
    python3 -m venv venv
    source venv/bin/activate
    ```
5. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```
6. Run the migrations:
   ```
   python manage.py migrate
   ```
7. Create a super user:
```
python manage.py createsuperuser
```
7. To test if everything was installed right, run the app and see that it shows some content:
   ```
   python manage.py run server
   ```
_Note: If you have Redis installed locally you could skip the next step._

8. Stop the running app and run the docker image, we are using here a docker image of Redis to avoid additional installations:
   ```
   docker-compose up
   ```