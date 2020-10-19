from flask import Flask

from tester.view import index, test


def create_app(test_config=None):
    # create and configure the app
    app = Flask('tester', instance_relative_config=True)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.add_url_rule("/", "index", index, methods=["GET"])
    app.add_url_rule("/test", "test", test, methods=["GET"])
    
    return app


def run():
    app=create_app()
    app.run(debug=True)