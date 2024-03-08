from flask import Flask, request

app = Flask(__name__)


# app and database configuration later

# logic similar to:

# User object


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    return


@app.route('/create_acc', methods=['POST'])
def create_acc():
    username = request.form['username']
    password = request.form['password']
    return


if __name__ == '__main__':
    app.run(debug=True)
