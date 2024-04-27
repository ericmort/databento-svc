from flask import Flask
import livedata 

app = Flask(__name__)
livedata.setup_livedata()

@app.route('/es')
def get_es():
    return livedata.data

if __name__ == '__main__':
    app.run(debug=True)

