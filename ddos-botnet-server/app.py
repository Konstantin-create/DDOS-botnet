from flask import Flask, request
from config import PathConfigs

# Server init
app = Flask(__name__)


from modules import routes

app.run(host="0.0.0.0", port="80")