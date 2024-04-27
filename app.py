from flask import Flask
import livedata 
import logging 
import databento as db
import os

app = Flask(__name__)

data = []

def user_callback(record: db.DBNRecord) -> None:
    app.logger.info(f"callback: ${record}")
    data.append({"instrument_id" : record.instrument_id})
        

# Create a callback to handle exceptions from `user_callback`
def error_handler(exception: Exception) -> None:
    app.logger.info(f"an error occurred {exception}")

def setup_livedata():
    key = os.environ.get("DATABENTO_API_KEY")
    if key is None:
        raise Exception ("Unknown DATABENTO_API_KEY")
    
    masked = len(key[:-4])*"#"+key[-4:]
    #app2.logger.info(f'DATABENTO_API_KEY: ${masked}')
    app.logger.info(masked)

    # Create a live client
    client = db.Live(key=key)

    # Subscribe with a specified start time for intraday replay
    client.subscribe(
        dataset="GLBX.MDP3",
        schema="ohlcv-1h",
        symbols="ESM4",
        #stype_in="parent",
        start="2024-04-26T14:00:00"
    )

    
    client.add_callback(
        record_callback=user_callback,
        exception_callback=error_handler,  # optional error handler
    )

    client.start()
    app.logger.info("Subscription started.")




@app.route('/')
def get_index():
    app.logger.info("received request")
        
    for x in data:
        app.logger.info({
            "instrument_id" : x["instrument_id"]
        })
    
    app.logger.info(data)
    return data



if __name__ == '__main__':
    app.run(debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(logging.DEBUG)
    app.logger.info("Initialized loggers")
    

setup_livedata()