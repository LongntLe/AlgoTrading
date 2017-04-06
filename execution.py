import v20

class Execution(object):
    def __init__(self, domain, access_token, account_id):
        self.domain = domain
        self.access_token = access_token
        self.account_id = account_id
        self.ctx = v20.Context(
                self.domain,
                443,
                True,
                application="sample_code",
                token=self.access_token,
                datetime_format="RFC3339"
                )
    def execute_order(self, event):
        if event.side == 1:
            pass
        elif event.side == -1:
            event.units = -event.units
        request = self.ctx.order.market(
                self.account_id,
                instrument=event.instrument,
                units=event.units
                )
        order = request.get("orderFillTransaction")
        print("\n\n", order.dict(), "\n")
