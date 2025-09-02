from flask import Flask

from service.create_report import create_report

app = Flask(__name__)


@app.route("/")
def home():
    return create_report()


if __name__ == "__main__":
    app.run(debug=True)
