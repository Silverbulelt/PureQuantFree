from purequant.indicators import INDICATORS
from purequant.trade import OKEXFUTURES
from purequant.position import POSITION
from purequant.market import MARKET
from purequant.synchronize import SYNCHRONIZE
from purequant.push import push
from purequant.storage import storage
from purequant.time import get_localtime
from purequant.config import config
import traceback


class Strategy:

    def __init__(self, instrument_id, time_frame, fast_length, slow_length, long_stop, short_stop, start_asset, initial_position_direction, initial_position_amount):
        """双均线策略"""
        try:
            print("{} {} 双均线多空策略已启动！".format(get_localtime(), instrument_id))
            config.loads('config.json')  # 载入配置文件

            self.instrument_id = instrument_id  # 合约ID
            self.time_frame = time_frame  # k线周期
            self.exchange = OKEXFUTURES(config.access_key, config.secret_key, config.passphrase, self.instrument_id)  # 初始化交易所
            self.position = POSITION(self.exchange, self.instrument_id, self.time_frame)  # 初始化potion
            self.market = MARKET(self.exchange, self.instrument_id, self.time_frame)  # 初始化market
            self.indicators = INDICATORS(self.exchange, self.instrument_id, self.time_frame)
            self.synchronize = SYNCHRONIZE("mongodb", "position", self.instrument_id[0:3], self.exchange, self.instrument_id, self.time_frame)
            # 在第一次运行程序时，将初始资金数据、初始无持仓信息保存至mongodb数据库中
            if config.first_run == "true":
                storage.mongodb_save({"时间": get_localtime(), "profit": 0, "asset": start_asset}, 'asset', self.instrument_id[0:3])
                self.synchronize.save_strategy_position(initial_position_direction, initial_position_amount)
            # 读取数据库中保存的总资金数据
            self.total_asset = storage.mongodb_read_data('asset', self.instrument_id[0:3])[-1][0]['asset']
            self.overprice_range = config.overprice_range # 超价下单幅度
            self.counter = 0  # 计数器
            self.fast_length = fast_length  # 短周期均线长度
            self.slow_length = slow_length  # 长周期均线长度
            self.long_stop = long_stop   # 多单止损幅度
            self.short_stop = short_stop    # 空单止损幅度
        except:
            storage.mongodb_save({"warning! 时间": get_localtime(), "error message": str(traceback.format_exc())}, 'logger', self.instrument_id[0:3])  # 将异常信息保存至mongodb数据库

    def begin_trade(self):
        try:
            synchronize_info = self.synchronize.match()     # 运行持仓同步功能，并返回持仓同步信息
            if "匹配" not in synchronize_info:    # 如果策略持仓与账户持仓不匹配，保存持仓同步信息至mongodb数据库
                storage.mongodb_save({"时间": get_localtime(), "持仓同步信息": synchronize_info}, 'synchronize', self.instrument_id[0:3])    # 运行持仓同步
            # 计算策略信号
            fast_ma = self.indicators.MA(self.fast_length)
            slow_ma = self.indicators.MA(self.slow_length)
            cross_over = fast_ma[-2] >= slow_ma[-2] and fast_ma[-3] < slow_ma[-3]
            cross_below = slow_ma[-2] >= fast_ma[-2] and slow_ma[-3] < fast_ma[-3]
            if self.indicators.BarUpdate():
                self.counter = 0

            if self.counter < 2:
                # 按照策略信号开平仓
                if cross_over and self.counter < 1:     # 金叉时
                    if self.position.amount() == 0:
                        info = self.exchange.buy(self.market.last() * (1 + self.overprice_range), round(self.total_asset/self.market.last()/self.market.contract_value()))
                        push(info)
                        self.synchronize.save_strategy_position("long", round(self.total_asset/self.market.last()/self.market.contract_value()))
                        self.counter += 1
                    if self.position.direction() == 'short':
                        profit = self.position.covershort_profit()
                        self.total_asset += profit
                        storage.mongodb_save({"时间": get_localtime(), "profit": profit, "asset": self.total_asset}, 'asset', self.instrument_id[0:3])
                        info = self.exchange.BUY(self.market.last() * (1 - self.overprice_range), self.position.amount(), self.market.last() * (1 + self.overprice_range), round(self.total_asset/self.market.last()/self.market.contract_value()))
                        push("此次盈亏：{} 当前总资金：{}".format(profit, self.total_asset) + info)
                        self.synchronize.save_strategy_position("long", round(self.total_asset / self.market.last() / self.market.contract_value()))
                        self.counter += 1
                if cross_below and self.counter < 1:     # 死叉时
                    if self.position.amount() == 0:
                        info = self.exchange.sellshort(self.market.last() * (1 - self.overprice_range), round(self.total_asset/self.market.last()/self.market.contract_value()))
                        push(info)
                        self.synchronize.save_strategy_position("short", round(self.total_asset / self.market.last() / self.market.contract_value()))
                        self.counter += 1
                    if self.position.direction() == 'long':
                        profit = self.position.coverlong_profit()
                        self.total_asset += profit
                        storage.mongodb_save({"时间": get_localtime(), "profit": profit, "asset": self.total_asset}, 'asset', self.instrument_id[0:3])
                        info = self.exchange.SELL(self.market.last() * (1 + self.overprice_range), self.position.amount(), self.market.last() * (1 - self.overprice_range), round(self.total_asset/self.market.last()/self.market.contract_value()))
                        push("此次盈亏：{} 当前总资金：{}".format(profit, self.total_asset) + info)
                        self.synchronize.save_strategy_position("short", round(self.total_asset / self.market.last() / self.market.contract_value()))
                        self.counter += 1
                # 止损
                if self.position.amount() > 0:
                    if self.position.direction() == 'long' and self.market.last() <= self.position.price() * self.long_stop:
                        profit = self.position.coverlong_profit()
                        self.total_asset += profit
                        storage.mongodb_save({"时间": get_localtime(), "profit": profit, "asset": self.total_asset}, 'asset', self.instrument_id[0:3])
                        info = self.exchange.sell(self.market.last() * (1 - self.overprice_range), self.position.amount())
                        push("此次盈亏：{} 当前总资金：{}".format(profit, self.total_asset) + info)
                        self.synchronize.save_strategy_position("none", 0)
                        self.counter += 2
                    if self.position.direction() == 'short' and self.market.last() >= self.position.price() * self.short_stop:
                        profit = self.position.covershort_profit()
                        self.total_asset += profit
                        storage.mongodb_save({"时间": get_localtime(), "profit": profit, "asset": self.total_asset}, 'asset', self.instrument_id[0:3])
                        info = self.exchange.buytocover(self.market.last() * (1 + self.overprice_range), self.position.amount())
                        push("此次盈亏：{} 当前总资金：{}".format(profit, self.total_asset) + info)
                        self.synchronize.save_strategy_position("none", 0)
                        self.counter += 2
        except TypeError:
            pass
        except:
            storage.mongodb_save({"error! 时间": get_localtime(), "error message": str(traceback.format_exc())}, 'logger', self.instrument_id[0:3])  # 将异常信息保存至mongodb数据库

if __name__ == "__main__":
    strategy = Strategy("TRX-USDT-201225", "1m", 5, 10, 0.98, 1.02, 20, "none", 0)
    while True:
        strategy.begin_trade()