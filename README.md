[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)

# StudX

**StudX** is a web-based school management system written in Python 3 and using Django framework.
The application records personal data of student, teacher and Staff people. It allows to manage all the information that a school needs on a daily basis. 

:loudspeaker:
**Notic:** This project has been initiated while learning Python 3 and the Django framework. It is still under development and all features are not completed yet! If you notice any coding error or security issue or if you have recommendations on design, coding or recommendations in general do not hesitate to contact me.

### In development features

* Student records keeping
* Discipline management
* Attendance management
* Internal communication
* Student, Teacher, Staff Schedule


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See installing instructions for notes on how to deploy the project on a live system.

### Prerequisites
You will find hereafter what I use to develop and to run the project
* Ubuntu Server 16.04 LTS 
* Apache Web Server
* Python 3
* Django 2
* MySQL database
* Virtualenv (not mandatory but recommended)

### Installing
I use Virtualenv for developping this project so in order to get a local copy of the project directory clone "StudX_dir/Studx".
Then follow these steps:
1. create the database by typing in mysql command line `create database Studx_database`
2. Provide the required information to the `DATABASES` dictionnary by editing `/StudX/settings.py`
3. Create the tables with the django command line `python manage.py makemigrations` then `python manage.py migrate`
4. Finally, run the django server `python manage.py runserver <your-ip:port>`

## Built With

* [Python 3](https://www.python.org/downloads/) - Programming language
* [Django](https://www.djangoproject.com/) - Web framework 
* [MySQL](https://www.mysql.com/) - Database


## Contributing
Contributions will be warmly welcomed 


## Versioning
I use exclusively Github

## Authors

* **Debruycker Vincent**

## License

This is an open source project not under any particular license.
However framework, packages and librairies used are on their own licenses. Be aware of this if you intend to use part of this project for your own project.

### List of licensed resources 
* [CodyHouse - Schedule template](https://github.com/CodyHouse/schedule-template.git)
* [TinyMCE - HTML editor package](https://www.tiny.cloud/)
* [django-widget-tweaks](https://pypi.org/project/django-widget-tweaks/)





