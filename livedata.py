import databento as db
import os 

data = []

def setup_livedata():
    key = os.environ.get("DATABENTO_API_KEY")
    if key is None:
        raise Exception ("Unknown DATABENTO_API_KEY")
    
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
        print(f"callback run for {record}")
        data.append(record)


    # Create a callback to handle exceptions from `user_callback`
    def error_handler(exception: Exception) -> None:
        print(f"an error occurred {exception}")

    client.add_callback(
        record_callback=user_callback,
        exception_callback=error_handler,  # optional error handler
    )

    client.start()

