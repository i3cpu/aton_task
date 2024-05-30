## User Guide

1. Make sure you have Python and pip (Python package installer) installed.
2. Activate or create a virtual environment (venv) to isolate the project.
  Install the required dependencies listed in the requirements.txt file using the command:

<pre>
```   pip3 install -r requirements.txt
```
</pre>

3.  Perform Django database migrations. Migrations are needed to create database tables related to your project's models. Execute the following commands:
<pre>
```   python3 manage.py makemigrations
      python3 manage.py migrate
```
</pre>

4.  Run the Django development server:
<pre>
```   python3 manage.py runserver
```
</pre>
