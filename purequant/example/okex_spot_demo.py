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

# info = exchange.buy(7.35, 0.02)           # 以7.35的价格买入0.02个ETC，并打印下单信息
# info = market.last()                      # 打印ETC的最新成交价
# info = exchange.get_kline(time_frame)      # 获取k线数据
# info = indicators.MA(30)[-1]               # 计算30日收盘平均价指标
# info = position.amount()                  # 获取ETC-USDT交易对的USDT可用余额

# print(info)   # 打印信息