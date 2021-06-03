from flask import Flask
from flask_cors import CORS

from api.users.views import user_app
from extensions import db, jwt, migrate

app = Flask("myapi")
app.config.from_object("config")

# Configure flask extensions
CORS(app)
db.init_app(app)
jwt.init_app(app)
migrate.init_app(app, db)

# Register all blueprints for application
app.register_blueprint(user_app, url_prefix="/api/v1/users")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
