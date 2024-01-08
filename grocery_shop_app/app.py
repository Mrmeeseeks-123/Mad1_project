from flask import Flask
from application.models import *

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///groceryshop_db.sqlite3"
db.init_app(app)
app.app_context().push()

from application.controllers1 import *

from application.controllers2 import *

from application.controllers3 import *


if __name__=="__main__":
	app.run(debug=True)


