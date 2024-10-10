from flask import Flask

import controllers.accidents_controller as accidents

app = Flask(__name__)

if __name__ == '__main__':
    app.register_blueprint(accidents.accidents_blueprint, url_prefix="/api/accidents")
    app.run(debug=True)