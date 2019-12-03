from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Testing ml model API"


if __name__ == "__main__":
    app.run(debug=True)
