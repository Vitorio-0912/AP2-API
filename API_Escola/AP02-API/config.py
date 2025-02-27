import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT']=8000
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
""" mysql://<username>:<password>@<host>/<db_name>
 """
""" mssql+pyodbc://@<host>/<db_name>?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes """


db = SQLAlchemy(app)