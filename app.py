from flask import Flask
import livedata 
import logging 

app = Flask(__name__)
livedata.setup_livedata(app)

@app.route('/')
def get_index():
    return "Hello world"

@app.route('/es')
def get_es():
    app.logger.info("received request")
        
    for x in livedata.data:
        app.logger.debug({
            "instrument_id" : x["instrument_id"]
        })
    app.logger.info(livedata.data)
    return livedata.data

if __name__ == '__main__':
    app.run(debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(logging.DEBUG)
    app.logger.info("Initialized loggers")
