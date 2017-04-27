from event import OrderEvent
import pandas as pd
import numpy as np

"""
Lack position management class,
which would be added later
along with some modifications in this strat
"""
class momentumstrat(object):
    def __init__(self, instrument, units, events):
        self.instrument = instrument
        self.units = units
        self.events = events
        self.ticks = 0
        self.data = pd.DataFrame()

    def calculate_signals(self, event):
        self.position = 0
        if event.type == "TICK":
            self.ticks += 1
            self.data = self.data.append(
                    pd.DataFrame({"ticks": [self.ticks], "time": [event.time], "ask": [event.ask]}))
            self.data.index = pd.DatetimeIndex(self.data["time"])
            resam = self.data.resample("5S").last()
            resam["returns"] = np.log(resam["ask"]/resam["ask"].shift(1))
            resam["position"] = np.sign(
                    resam["returns"].rolling(12).mean()).dropna() #TODO: add self.momentum = timeframe
            print(resam[["time", "ask", "returns", "position"]].tail())

            if resam["position"].ix[-1] == 1: # last position is higher than previous means
                if self.position == 0: # position of portfolio equals to 0 => buy because no transaction happens before that
                    order = OrderEvent(
                            self.instrument, self.units, "market", "buy"
                            )
                elif self.position == -1:
                    order = OrderEvent(
                            self.instrument, 2*self.units, "market", "buy"  #order buy happens when 
                            )
                else:
                    order = OrderEvent(
                             self.instrument, 0, "market", "buy"
                             )
                self.position = 1
                self.events.put(order)
            elif resam["position"].ix[-1] == -1:
                if self.position == 0:
                    order = OrderEvent(
                            self.instrument, -self.units, "market", "sell"
                            )
                elif self.position == 1:
                    order = OrderEvent(
                            self.instrument, -2*self.units, "market", "sell"
                            )
                else:
                    order = OrderEvent(
                             self.instrument, 0, "market", "buy"
                             )
                self.position = -1
                self.events.put(order)
