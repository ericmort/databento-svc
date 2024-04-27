import databento as db
import os 
import logging 

data = []

def setup_livedata(app):
    key = os.environ.get("DATABENTO_API_KEY")
    if key is None:
        raise Exception ("Unknown DATABENTO_API_KEY")
    
    masked = len(key[:-4])*"#"+key[-4:]
    app.logger.info(f'DATABENTO_API_KEY: ${masked}')

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

    def user_callback(record: db.DBNRecord) -> None:
        app.logger.info(f"callback: ${record}")
        data.append({"instrument_id" : record.instrument_id})


    # Create a callback to handle exceptions from `user_callback`
    def error_handler(exception: Exception) -> None:
        app.logger.info(f"an error occurred {exception}")

    client.add_callback(
        record_callback=user_callback,
        exception_callback=error_handler,  # optional error handler
    )

    client.start()
    app.logger.info("Subscription started.")
