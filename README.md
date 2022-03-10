# Monitoring project API

## Installation

### Setup a virtualenv

1. Set up VENV variable

```bash
VENV=/path/to/your/venv
```

2. Create and activate a virtual environment

```bash
virtualenv -p /usr/bin/python3 $VENV
source $VENV/bin/activate
```

3. Update ```pip``` and install libraries

```bash
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

### Configuration

1. Create a ```.env``` file at the root of the project and add the following
   variables

```dotenv
FLASK_SETTINGS_FILE=/absolute/path/to/your/config/file
FLASK_ENV=development# or production
FLASK_DEBUG=1

################
# See: https://flask.palletsprojects.com/en/1.0.x/quickstart/#sessions
# Use -> python -c "import os; print(os.urandom(16))" to generate one
################
FLASK_SECRET="Your Secret Key"
```

2. In your ```flask settings file``` add the following variables

```dotenv
SQLALCHEMY_DATABASE_URI="sqlite:///absolute/path/to/your/db.sqlit"
```

### Run the service

1. Set up the application database (Be sure that your ```venv``` is already
   activated before)

```bash
flask setup-db
```

2. Launch the service

```bash
flask run -p 3000
```

> **Important**
> 
> The development server is not intended to be used on production systems. It 
> was designed especially for development purposes and performs poorly under 
> high load. For deployment setups have a look at the 
> [Application Deployment](https://werkzeug.palletsprojects.com/en/1.0.x/deployment/)
> pages.
> 