from flask import Flask
from flask import request
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "shadowfax"}
app.config["SECRET_KEY"] = "secretKey"

db = MongoEngine(app)

if __name__ == '__main__':
  app.run()

__import__('shadowfax.views')
