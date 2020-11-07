## Server-side application for sticka-sto.

### Setup
Create a virtual environment for all this stuff and put your terminal into that environment

```
# I usually just go "env" for env_name but you might want to make it more meaningful
virtualenv -p python3 <env_name>
source <env_name>/bin/activate
```

Install all the Python requirements

```
pip install -r requirements.txt
```

*When necessary* Updating the requirements
```
pip freeze > requirements.txt
```

### psycopg2
You may need a couple of system requirements. I had to download:

```
sudo apt-get install python3-dev
sudo apt-get install libpq-dev
```
