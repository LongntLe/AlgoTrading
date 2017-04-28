from event import TickEvent
import v20
import pandas as pd

class StreamingForexPrices(object):
    def __init__(
            self, domain, access_token,
            account_id, instruments, events_queue
            ):
        #self.ticks = 0
        #self.data = pd.DataFrame()
        self.domain = domain
        self.access_token = access_token
        self.account_id = account_id
        self.instruments = instruments
        self.events_queue = events_queue
        self.cur_bid = None
        self.cur_ask = None
        self.ctx_stream = v20.Context(
                self.domain,
                443,
                True,
                application="sample_code",
                token=self.access_token,
                datetime_format="RFC3339"
                )

    def stream_to_queue(self):
        response = self.ctx_stream.pricing.stream(
                self.account_id,
                snapshot = True,
                instruments = self.instruments
                )
        for msg_type, msg in response.parts():
            if msg_type == "pricing.Price":
                #msg = self.on_success(msg.time, msg.asks[0].price)
                print(msg.instrument, msg.time, msg.asks[0].price, msg.bids[0].price)
                instrument = msg.instrument
                time = msg.time
                bid = msg.bids[0].price
                ask = msg.asks[0].price
                tev = TickEvent(instrument, time, bid, ask)
                self.events_queue.put(tev)
                self.cur_bid = bid
                self.cur_ask = ask
                #self.ticks += 1
                #print(self.ticks, end=' ')
                #self.data = self.data.append(
                #        pd.DataFrame({"time": [time], "ask": [ask]}))
                #self.data.index = pd.DatetimeIndex(self.data["time"])
                #resam = self.data.resample("1min").last()
                #print(resam[["ask", "returns", "positions"]].tail())
            elif msg_type == "pricing.Heartbeat" and args.show_heartbeats:
                print(msg)
