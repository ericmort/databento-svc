from flask import Flask
import livedata 
import logging 
import databento as db
import os
import datetime 

app = Flask(__name__)
historical_data = []
current_price = {}

live_or_historical = "historical"

def user_callback(record: db.DBNRecord) -> None:
    app.logger.info(f"callback: ${record}")
    if live_or_historical == "live":
        current_price = {"open" : record.open, "close" : record.close, "high": record.high, "low" : record.low, "volume" : record.volume}
    else:
        current_price = record
        
        #dt = datetime.datetime.fromtimestamp(record.ts_recv // 1000000000)
        #current_price["dt"] = dt.strftime('%Y-%m-%d %H:%M:%S') + '.' + str(int(record.ts_recv % 1000000000)).zfill(9)
    
    historical_data.append(current_price)

        

# Create a callback to handle exceptions from `user_callback`
def error_handler(exception: Exception) -> None:
    app.logger.error(f"an error occurred {exception}")

def setup_databento():
    key = os.environ.get("DATABENTO_API_KEY")
    if key is None:
        raise Exception ("Unknown DATABENTO_API_KEY")
    
    masked = len(key[:-4])*"#"+key[-4:]
    app.logger.info(f'DATABENTO_API_KEY: ${masked}')
    
    start_historical(key)
    
    

def start_historical(key):
    client = db.Historical(key=key)
    data = client.timeseries.get_range(
        dataset="GLBX.MDP3",
        symbols="ESM4",
        schema="trades",
        start="2024-04-24T14:00:00",
        end="2024-04-24T14:00:10",
        limit=10,
    )
    data.replay(user_callback)

def start_live(key) -> None:
    start_time = datetime.now()
    
    client = db.Live(key=key)
    client.subscribe(
        dataset="GLBX.MDP3",
        schema="ohlcv-1h",
        symbols="ESM4",
        start=start_time
    )

    
    client.add_callback(
        record_callback=user_callback,
        exception_callback=error_handler,  
    )

    client.start()
    app.logger.info("Subscription started.")


@app.route('/')
def get_index():
    return 'Hello, world'

@app.route('/historical')
def get_historical():
    app.logger.debug("received request")
    global historical_data
    app.logger.debug(historical_data)
    return str(len(historical_data))
    
@app.route('/live')
def get_live():
    app.logger.debug("received request")
    return current_price


if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    app.logger.info("Initialized loggers")
    setup_databento()    
    app.run(debug=True, host='0.0.0.0', port=10000)
else:
    app.logger.setLevel(logging.DEBUG)
    app.logger.info("Initialized loggers")
    setup_databento()
    