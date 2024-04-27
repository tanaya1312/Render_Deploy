from flask import Flask
app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, World!...I am Tanaya.'


if __name__ == '__main__':
    # Run the app
    app.run(debug=True)
