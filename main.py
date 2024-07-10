from flask import Flask, render_template
import process
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/tool/')
def tool():
    if os.path.exists("recording.wav"):
        return render_template('demo.html', scores=process.main())
    return render_template('demo.html', scores=[])


if __name__ == '__main__':
    app.run(port=3000)
