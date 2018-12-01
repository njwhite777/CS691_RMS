# Readme:

## Project Description:
This repository contains code for an assignment for Software Requirements and Design, CS691, a software engineering course at Ball State University. The web application implemented herein operates as a restaurant management system, allowing restaurants to be defined, menus to be managed and associated with restaurants, menu items and prices to be defined, and orders to be tracked. Three roles are used to manage various aspects of the public interface for the restaurant.

## Technology Choices:
For this project the backend is implemented in Python 3 using the Flask framework. All HTML  served as part of this project is rendered from Jinja templates. Frontend scripting is done with JavaScript. For purposes of development, the database is an sqlite3 file in the project directory. All database operations are abstracted using SQLAlchemy, so adaptation to any other SQL backend is virtually transparent apart from some basic configuration details and potentially networking. These particular technologies were chosen for two main reasons: First, as the only developer, I wanted a technology stack with which I was familiar. Second, Flask is not super opinionated about the interfaces/modules that a developer must use, allowing one to develop an application at a level of abstraction that is more natural based on the needs and requirements for a particular project.

## Additional Documentation:
#### Class Diagrams:
<a href="class_diagram.png">Iteration I Diagram</a>
<a href="class_diagramII.png">Iteration II Diagram</a>

#### Requirements:
<a href="requirements.md">Iteration I</a>
<a href="requirementsII.md">Iteration II</a>
<a href="requirementsIII.md">Iteration II</a>


## Replicating the development environment:
To replicate the environment, install python virtual environments and virtualenvwrapper. Set up a new virtual environment for this project:
```
mkvirtualenv CS691
```

Then, clone the repository:
```
git clone https://github.com/njwhite777/SoftwareRequrementsAndDesign_FP.git && cd SoftwareRequrementsAndDesign_FP
```

Make sure the virtual environment for this project is activated.
```
workon CS691
```

Install the dependencies:
```
pip install -r requirements.txt
```

Now you should be able to run the development server:
```
./manage.py runserver
```
#### Helpful development hints:
If you want to populate your database with some basic data:
```
./manage.py init_db
```

If you want to drop to a shell in the application context:
```
./manage.py shell
```
