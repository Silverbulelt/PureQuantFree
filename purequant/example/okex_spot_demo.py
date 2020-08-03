from purequant.trade import OKEXSPOT
from purequant.market import MARKET
from purequant.indicators import INDICATORS
from purequant.position import POSITION

# 账户和策略参数等信息
accessy_key = 'your access_key'
secret_key = 'your secret_key'
passphrase = 'your passphrase'
instrument_id = 'ETC-USDT'
time_frame = '1d'

# 初始化交易所、行情模块与指标等模块
exchange = OKEXSPOT(accessy_key, secret_key, passphrase, instrument_id)
market = MARKET(exchange, instrument_id, time_frame)
indicators = INDICATORS(exchange, instrument_id, time_frame)
position = POSITION(exchange, instrument_id, time_frame)

# 下单交易，买入和卖出
# info = exchange.buy(7.35, 0.02)           # 以7.35的价格买入0.02个ETC
# info = exchange.sell(7.35, 0.01)            # 卖出0.02个ETC

# 获取行情信息
# info = exchange.get_kline(time_frame)      # 获取k线数据
# info = market.last()                      # 获取ETC-USDT的最新成交价
# info = market.open(-1)                      # 获取ETC-USDT的当日开盘价
# info = market.high(-1)                      # 获取ETC-USDT的当日最高价
# info = market.low(-1)                      # 获取ETC-USDT的当日最低价
# info = market.close(-1)                      # 获取ETC-USDT的当日收盘价

# 持仓信息
# info = position.amount()                  # 获取ETC-USDT交易对的ETC可用余额

# 计算指标
# info = indicators.MA(30)[-1]               # 计算当根k线上的30日收盘平均价指标
# info = indicators.CurrentBar()           # 计算获取的k线长度
# info = indicators.EMA(30)[-1]           # 计算当根k线上的30日EMA
# info = indicators.VOLUME()[-1]              # 计算当根k线上的成交量
# info = indicators.HIGHEST(30)[-1]           # 30日周期内最高价
# info = indicators.LOWEST(30)[-1]            # 30日周期内最低价

# print(info)   # 打印信息