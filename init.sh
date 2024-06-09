mkdir .venv

touch Pipfile
touch Pipfile.lock

pipenv install flask
pipenv install requests
pipenv install flask_sqlalchemy
pipenv install mysql_connector_python

pipenv shell
