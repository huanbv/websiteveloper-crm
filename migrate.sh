export APP_CONFIG_FILE=config/development.py
export FLASK_ENV=development
export FLASK_APP=wsgi.py

# adding paths
ROOT_DIR=.
MAIN_DIR=./src/main/
export PYTHONPATH=$MAIN_DIR:$ROOT_DIR

#export # showing all environment variables

flask db init --directory db/migrations
flask db migrate --directory db/migrations -m "new migrate íntance"
flask db upgrade --directory db/migrations
