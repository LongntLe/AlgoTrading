import random

from event import OrderEvent

class TestRandomStrategy(object):
    def __init__(self, instrument, units, events):
        self.instrument = instrument
        self.units = units
        self.events = events
        self.ticks = 0
        self.invested = False

    def calculate_signals(self, event):
        if event.type == "TICK":
            self.ticks += 1
            if self.ticks % 5 == 0:
                if self.invested == False:
                    signal = SignalEvent(self.instrument, "market", "buy")
                    self.events.put(signal)
                    self.invested = True
                else:
                    signal = SignalEvent(self.instrument, "market", "sell")
                    self.events.put(signal)
                    self.invested = False
                """
                side = random.choice(["buy", "sell"])
                if side == "buy":
                    order = OrderEvent(
                            self.instrument, self.units, "market", side
                            )
                elif side == "sell":
                    order = OrderEvent(
                            self.instrument, -self.units, "market", side
                            )
                self.events.put(order)
                """
                #TODO: trim down side, not needed any more. 
                #On second thought, wait for implementation of portfolio as we may need to report side

