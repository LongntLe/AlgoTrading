"""Store trading strategies
    List: Moving Average, Random Test Strategy"""

from event import SignalEvent

class movingaverage(object):
    def __init__(self, instrument, events):
        self.instrument = instrument
        self.events = events
        self.ticks = 0
        self.invested = False

class TestStrategy(object):
    def __init__(self, instrument, events):
        self.instrument = instrument
        self.events = events
        self.ticks = 0
        self.invested = False

    def calculatesignals(self, event):
        if event.type = "TICK":
            self.ticks += 1
            if self.ticks % 3 == 0:
                if self.invested == False:
                    signal = SignalEvent(self.instrument, "market", "buy")
                    self.events.put(signal)
                    self.Invested = True
                else:
                    signal = SignalEvent(self.instrument, "market", "sell")
                    self.events.put(signal)
                    self.Invested = False
                
