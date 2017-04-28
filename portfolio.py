from copy import deepcopy

from event import OrderEvent
from position import Position

class Portfolio(object):
    def __init__(
            self, ticker, events, base="GBP", leverage=20,
            equity=100000.0, risk_per_trade=0.02
            ):
    #TODO: dynamic equity and risk_per_trade
    #TODO: modify base for multiple currency types
    #TODO: dynamic leverage (is it possible for oanda?)
        self.ticker = ticker
        self.events = events
        self.base = base
        self.leverage = leverage
        self.equity = equity
        self.balance = deepcopy(self.equity)
        self.risk_per_trade = risk_per_trade
        self.trade_units = self.calc_risk_position_size()
        self.positions = {}

    def calc_risk_position_size(self):
        return self.equity * self.risk_per_trade

    def add_new_position(
            self, side, market, units, exposure,
            add_price, remove_price
            ):
        ps = Position(
                side, market, units, exposure, 
                add_price, remove_price
                )
        self.positions[market] = ps

    def add_position_units(
            self, market, units, exposure,
            add_price, remove_price
            ):
        if market not in self.positions:
            return False
        else:
            ps = self.positions[market]
            new_total_units = ps.units + units
            new_total_cost = ps.avg_price*ps.units + add_price*units
            ps.exposure += exposure
            ps.avg_price = new_total_cost/new_total_units
            ps.units = new_total_units
            ps.update_position_price(remove_price)
            return True

    def remove_position_units(
            self, market, units, exposure, 
            add_price, remove_price
            ):
        if market not in self.positions:
            return False
            #TODO: check with position in trading.py and strategy.py for synchronization
        else:
            ps = self.positions[market]
            ps.units -= units
            exposure = float(units) #TODO: check decimal as potential unit measurement
            ps.exposure -= exposure
            ps.update_position_price(remove_price)
            pnl = ps.calculate_pips() * exposure / remove_price
            self.balance += pnl
            return True

    def close_position(
            self, market, remove_price
            ):
        if market not in self.positions:
            return False
        else:
            ps = self.positions[market]
            ps.update_position_price(remove_price)
            pnl = ps.calculate_pips() * ps.exposure / remove_price
            self.balance += pnl
            del[self.positions[market]]
            return True

    def execute_signal(self, signal_event):
        side = signal_event.side
        market = signal_event.instrument
        order_type = signal_event.order_type

        if side == "sell":
            units = -int(self.trade_units)
            add_price = self.ticker.cur_bid
            remove_price = self.ticker.cur_ask
            exposure = -units
        elif side == "buy":
            units = int(self.trade_units)
            add_price = self.ticker.cur_ask
            remove_price = self.ticker.cur_bid
            exposure = units

        if market not in self.positions:
            self.add_new_position(
                    side, market, units, exposure,
                    add_price, remove_price
                    )
            order = OrderEvent(market, units, order_type, side)
            self.events.put(order)

        else:
            ps = self.positions[market]
            if side == ps.side:
                add_position_units(
                        market, units, exposure,
                        add_price, remove_price
                        )
            else:
                if units == ps.units:
                    self.close_position(market, remove_price)
                    order = OrderEvent(market, units, "market", "sell")
                    self.events.put(order)
                elif units < ps.units:
                    self.remove_position_units(
                            market, units, remove_price
                            )
                else:
                    new_units = units - ps.units
                    self.close_position(market, remove_price)

                    if side == "buy":
                        new_side = "sell"
                    else: 
                        new_side = "buy"
                    new_exposure = float(units) #use decimals in next update
                    self.add_new_position(
                            new_side, market, new_units, 
                            new_exposure, add_price, remove_price
                            )
                    print("Balance: %0.2f" % self.balance)
                    #check stability 
    def data_viz(self):
        pass
    #TODO: visualize PnL realtime
        #TODO: modify to reflect new API. Should be easier to do than the old one. 
    #TODO: dynamic portfolio based on current bid/ask volume (when cur_volume<cur_bid/cur_ask)
