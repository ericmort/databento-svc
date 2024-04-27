from flask import Flask
import livedata 

app = Flask(__name__)

@app.route('/es')
def get_es():
    return livedata.data

if __name__ == '__main__':
    livedata.setup_livedata()
    app.run(debug=True)

