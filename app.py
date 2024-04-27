from flask import Flask
import livedata 

app = Flask(__name__)
livedata.setup_livedata(app)

@app.route('/es')
def get_es():
    for x in livedata.data:
        app.logger.debug({
            "instrument_id" : x["instrument_id"]
        })
        return livedata.data

if __name__ == '__main__':
    app.run(debug=True)

