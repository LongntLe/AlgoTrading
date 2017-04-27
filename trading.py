import queue
import threading
import time

from execution import Execution
from settings import STREAM_DOMAIN, API_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID
from strategy.randomstrategy import TestRandomStrategy
from strategy.momentum import momentumstrat
from streaming import StreamingForexPrices

def trade(events, strategy, execution):
    while True:
        try:
            event = events.get(False)
        except queue.Empty:
            pass
        else:
            if event is not None:
                if event.type == "TICK":
                    strategy.calculate_signals(event)
                elif event.type == "ORDER":
                    print("Executing order!")
                    execution.execute_order(event)
        time.sleep(heartbeat)

if __name__ == "__main__":
    heartbeat = 0.5
    events = queue.Queue()

    instrument = "EUR_USD"
    units = 10000

    prices = StreamingForexPrices(
            STREAM_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID,
            instrument, events
            )

    execution = Execution(API_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID)

    strategy = momentumstrat(instrument, units, events)

    trade_thread = threading.Thread(target=trade, args=(events, strategy, execution))
    price_thread = threading.Thread(target=prices.stream_to_queue, args=[])

    trade_thread.start()
    price_thread.start()

