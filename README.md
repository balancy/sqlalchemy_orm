# SQLAlchemy ORM

App tests work with SQLAlchemy ORM.

### How to install locally

Python3 and Git should be already installed. 

1. Clone the repository by command:
```console
git clone https://github.com/balancy/sqlalchemy_orm
```

2. Go inside cloned repository and create virtual environment by command:
```console
python -m venv env
```

3. Activate virtual environment. For linux-based OS:
```console
source env/bin/activate
```
&nbsp;&nbsp;&nbsp;
For Windows:
```console
env\scripts\activate
```

4. Install requirements by command:
```console
pip install -r requirements.txt
```

5. Rename `example.config.py` to `config.py` and write inside your propre DB name

## How to use

1. Create DB by command:
```console
python create_db.py
```

2. Fill DB by command:
```console
python fill_db_with_data.py
```

3. Request data from DB by command:
```console
python request_data_from_db.py
```
