## SNAPYTICKET MAIN REPOSITORY

### Technologies used
>###### Django: The web framework for perfectionists with deadlines (Django builds better web apps with less code).

### Installation
>###### If you wish to run your own build, first ensure you have python globally installed in your computer. 

###### If not, you can get python here.

    $ https://www.python.org/
    
###### Install python package manager pipenv by doing 

    $ pip install pipenv
    
###### Then, Git clone this repo to your PC:

    $ git clone https://github.com/snapyticket/snapyticket-final/
### Dependencies
###### Cd into your the cloned repo as such:

    $ cd snapyticket-final
    
###### Create and fire up your virtual environment:

    $ pipenv install
    $ pipenv shell
    
###### Install the dependencies needed to run the app:

    $ pipenv install
    
###### Make those migrations work

    $ cd snapyticket
    $ python manage.py makemigrations
    $ python manage.py migrate
    
### Run It
###### Fire up the server using this one simple command:

    $ python manage.py runserver
###### You can now access the file app service on your browser by using:

    $ run http://localhost:8000/
