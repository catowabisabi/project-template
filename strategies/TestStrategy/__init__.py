from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils


class TestStrategy(Strategy):

    @property
    def short_ema(self):
        return ta.ema(self.candle, 21)

    @property    
    def long_ema(self):
        return ta.ema(self.candle, 50)

    def should_long(self) -> bool:
        return self.short_ema > self.long_ema

    def go_long(self):
        entry_price = self.price
        qty = utils.size_to_qty(self.balance, entry_price)

        self.buy = qty, entry_price

    def update_position(self) -> None:
        if self.short_ema <= self.long_ema:
            self.liquidate()

    def should_short(self) -> bool:
        # For futures trading only
        return False

    def go_short(self):
        # For futures trading only
        pass

    def should_cancel_entry(self) -> bool:
        return True
