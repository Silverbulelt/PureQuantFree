# -*- coding:utf-8 -*-

"""
交易模块

Author: eternal ranger
Date:   2020/07/09
email: interstella.ranger2020@gmail.com
"""
from purequant.exchange.okex import spot_api as okexspot
from purequant.time import ts_to_utc_str
from purequant.exchange.huobi import huobi_spot as huobispot



class OKEXSPOT:
    """okex现货操作  https://www.okex.com/docs/zh/#spot-README"""
    def __init__(self, access_key, secret_key, passphrase, instrument_id):
        """

        :param access_key:
        :param secret_key:
        :param passphrase:
        :param instrument_id: e.g. etc-usdt
        """
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__passphrase = passphrase
        self.__instrument_id = instrument_id
        self.__okex_spot = okexspot.SpotAPI(self.__access_key, self.__secret_key, self.__passphrase)

    def buy(self, price, size, order_type=None, type=None, notional=""):
        """
        okex现货买入
        :param price:价格
        :param size:数量
        :param order_type:参数填数字
        0：普通委托（order type不填或填0都是普通委托）
        1：只做Maker（Post only）
        2：全部成交或立即取消（FOK）
        3：立即成交并取消剩余（IOC）
        :param type:limit或market（默认是limit）。当以market（市价）下单，order_type只能选择0（普通委托）
        :param notional:买入金额，市价买入时必填notional
        :return:
        """
        order_type = order_type or 0
        type=type or "limit"
        receipt = self.__okex_spot.take_order(instrument_id=self.__instrument_id, side="buy", type=type, size=size, price=price, order_type=order_type, notional=notional)
        order_id = int(receipt['order_id'])
        if receipt['result'] == False:
            return '【交易提醒】：' + self.__instrument_id + '买入开多失败' + " 【错误信息】" + receipt['error_message']
        else:
            order_info = self.__okex_spot.get_order_info(instrument_id=self.__instrument_id, order_id=order_id)
            if order_info["订单状态"] == "等待成交":
                self.revoke_order(order_id=order_id)
                state = self.get_order_info(order_id=order_id)
            if order_info["订单状态"] == "完全成交" or order_info["订单状态"] == "失败 ":
                state = None
            if order_info["订单状态"] == "部分成交":
                self.revoke_order(order_id=order_id)
                state = self.get_order_info(order_id=order_id)
            return '【交易提醒】' + "下单结果：{} 撤单结果：{}".format(order_info, state)

    def sell(self, price, size, order_type=None, type=None):
        """
        okex现货卖出
        :param price: 价格
        :param size:卖出数量，市价卖出时必填size
        :param order_type:参数填数字
        0：普通委托（order type不填或填0都是普通委托）
        1：只做Maker（Post only）
        2：全部成交或立即取消（FOK）
        3：立即成交并取消剩余（IOC）
        :param type:limit或market（默认是limit）。当以market（市价）下单，order_type只能选择0（普通委托）
        :return:
        """
        order_type = order_type or 0
        type = type or "limit"
        receipt = self.__okex_spot.take_order(instrument_id=self.__instrument_id, side="sell", type=type, size=size, price=price, order_type=order_type)
        order_id = int(receipt['order_id'])
        if receipt['result'] == False:
            return '【交易提醒】：' + self.__instrument_id + '卖出平多失败' + " 【错误信息】" + receipt['error_message']
        else:
            order_info = self.__okex_spot.get_order_info(instrument_id=self.__instrument_id, order_id=order_id)
            if order_info["订单状态"] == "等待成交":
                self.revoke_order(order_id=order_id)
                state = self.get_order_info(order_id=order_id)
            if order_info["订单状态"] == "完全成交" or order_info["订单状态"] == "失败 ":
                state = None
            if order_info["订单状态"] == "部分成交":
                self.revoke_order(order_id=order_id)
                state = self.get_order_info(order_id=order_id)
            return '【交易提醒】' + "下单结果：{} 撤单结果：{}".format(order_info, state)

    def get_order_list(self, state, limit):
        receipt = self.__okex_spot.get_orders_list(self.__instrument_id, state=state, limit=limit)
        return receipt

    def revoke_order(self, order_id):
        receipt = self.__okex_spot.revoke_order(self.__instrument_id, order_id)
        if receipt['error_code'] == "0":
            return '【交易提醒】撤单成功'
        else:
            return '【交易提醒】撤单失败' + receipt['error_message']

    def get_order_info(self, order_id):
        receipt = self.__okex_spot.get_order_info(self.__instrument_id, order_id)
        return receipt

    def get_kline(self, time_frame):
        if time_frame == "1m" or time_frame == "1M":
            granularity = '60'
        elif time_frame == '3m' or time_frame == "3M":
            granularity = '180'
        elif time_frame == '5m' or time_frame == "5M":
            granularity = '300'
        elif time_frame == '15m' or time_frame == "15M":
            granularity = '900'
        elif time_frame == '30m' or time_frame == "30M":
            granularity = '1800'
        elif time_frame == '1h' or time_frame == "1H":
            granularity = '3600'
        elif time_frame == '2h' or time_frame == "2H":
            granularity = '7200'
        elif time_frame == '4h' or time_frame == "4H":
            granularity = '14400'
        elif time_frame == '6h' or time_frame == "6H":
            granularity = '21600'
        elif time_frame == '12h' or time_frame == "12H":
            granularity = '43200'
        elif time_frame == '1d' or time_frame == "1D":
            granularity = '86400'
        else:
            return ('【交易提醒】k线周期错误，只支持【1min 3min 5min 15min 30min 1hour 2hour 4hour 6hour 12hour 1day】')
        receipt = self.__okex_spot.get_kline(self.__instrument_id, granularity=granularity)
        return receipt

    def get_position(self):
        receipt = self.__okex_spot.get_position(self.__instrument_id)
        return receipt

    def get_ticker(self):
        receipt = self.__okex_spot.get_specific_ticker(instrument_id=self.__instrument_id)
        return receipt

    def get_contract_value(self):
        return {self.__instrument_id: 1}


class HUOBISPOT:
    """火币现货"""

    def __init__(self, access_key, secret_key, instrument_id):
        """

        :param access_key:
        :param secret_key:
        :param instrument_id: e.g. 'ETC-USDT'
        """
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__instrument_id = (instrument_id.split('-')[0] + instrument_id.split('-')[1]).lower()
        self.__huobi_spot = huobispot.HuobiSVC(self.__access_key, self.__secret_key)
        self.__currency = (instrument_id.split('-')[0]).lower()
        self.__account_id = self.__huobi_spot.get_accounts()['data'][0]['id']
        self.__symbol = (instrument_id).lower()  # 获取合约面值的函数中所用到的交易对未处理前的格式

    def buy(self, price, size, order_type=None):
        """
        火币现货买入开多
        :param price: 价格
        :param size: 数量
        :param order_type: 填 0或者不填都是限价单，
                            1：只做Maker（Post only）
                            2：全部成交或立即取消（FOK）
                            3：立即成交并取消剩余（IOC）
                            4.市价买入
        :return:
        """
        order_type=order_type or 'buy-limit'
        if order_type == 0:
            order_type = 'buy-limit'
        elif order_type == 1:
            order_type = 'buy-limit-maker'
        elif order_type == 2:
            order_type = 'buy-limit-fok'
        elif order_type == 3:
            order_type = 'buy-ioc'
        elif order_type == 4:
            order_type = 'buy-market'
        result = self.__huobi_spot.send_order(self.__account_id, size, 'spot-api', self.__instrument_id, _type=order_type, price=price)
        if result['status'] == 'error':
            order_info = None
            return "【交易提醒】交易所: Huobi {} 下单错误，错误信息：{}".format(self.__instrument_id, result['err-msg'])
        else:
            order_id = result['data']['order_id_str']
            order_info = self.get_order_info(order_id)
        if order_info["订单状态"] == "已提交" or order_info["订单状态"] == "部分成交":
            self.revoke_order(order_id=order_id)
            state = self.get_order_info(order_id=order_id)
        else:
            state = None
        return '【交易提醒】' + "下单结果：{} 撤单结果：{}".format(order_info ,state)

    def sell(self, price, size, order_type=None):
        """
        火币现货卖出平多
        :param price: 价格
        :param size: 数量
        :param order_type: 填 0或者不填都是限价单，
                            1：只做Maker（Post only）
                            2：全部成交或立即取消（FOK）
                            3：立即成交并取消剩余（IOC）
                            4.市价卖出
        :return:
        """
        order_type=order_type or 'sell-limit'
        if order_type == 0:
            order_type = 'sell-limit'
        elif order_type == 1:
            order_type = 'sell-limit-maker'
        elif order_type == 2:
            order_type = 'sell-limit-fok'
        elif order_type == 3:
            order_type = 'sell-ioc'
        elif order_type == 4:
            order_type = 'sell-market'
        result = self.__huobi_spot.send_order(self.__account_id, size, 'spot-api', self.__instrument_id, _type=order_type, price=price)
        if result['status'] == 'error':
            order_info = None
            return "【交易提醒】交易所: Huobi {} 下单错误，错误信息：{}".format(self.__instrument_id, result['err-msg'])
        else:
            order_id = result['data']['order_id_str']
            order_info = self.get_order_info(order_id)
        if order_info["订单状态"] == "已提交" or order_info["订单状态"] == "部分成交":
            self.revoke_order(order_id=order_id)
            state = self.get_order_info(order_id=order_id)
        else:
            state = None
        return '【交易提醒】' + "下单结果：{} 撤单结果：{}".format(order_info ,state)

    def get_order_info(self, order_id):
        result = self.__huobi_spot.order_info(order_id)
        instrument_id = result['data']['symbol']
        action = None
        if "buy" in result['data']['type']:
            action = "买入开多"
        if  "sell" in result['data']['type']:
            action = "卖出平多"

        if result["data"]['state'] == 'filled':
            dict = {"交易所": "Huobi", "合约ID": instrument_id, "方向": action, "订单状态": "完全成交", "成交均价": result['data']['price'],
                    "数量": result["data"]["amount"], "成交金额": result['data']["field-cash-amount"]}
            return dict
        elif result["data"]['state'] == 'canceled':
            dict = {"交易所": "Huobi", "合约ID": instrument_id, "方向": action, "订单状态": "撤单成功"}
            return dict
        elif result["data"]['state'] == 'partial-filled':
            dict = {"交易所": "Huobi", "合约ID": instrument_id, "方向": action, "订单状态": "部分成交", "成交均价": result['data']['price'],
                    "数量": result["data"]["field-amount"], "成交金额": result['data']["field-cash-amount"]}
            return dict
        elif result["data"]['state'] == 'partial-canceled':
            dict = {"交易所": "Huobi", "合约ID": instrument_id, "方向": action, "订单状态": "部分成交撤销"}
            return dict
        elif result["data"]['state'] == 'submitted':
            dict = {"交易所": "Huobi", "合约ID": instrument_id, "方向": action, "订单状态": "已提交"}
            return dict

    def revoke_order(self, order_id):
        receipt = self.__huobi_spot.cancel_order(order_id)
        if receipt['status'] == "ok":
            return '【交易提醒】交易所: Huobi 撤单成功'
        else:
            return '【交易提醒】交易所: Huobi 撤单失败' + receipt['data']['errors'][0]['err_msg']

    def get_kline(self, time_frame):
        if time_frame == '1m' or time_frame == '1M':
            period = '1min'
        elif time_frame == '5m' or time_frame == '5M':
            period = '5min'
        elif time_frame == '15m' or time_frame == '15M':
            period = '15min'
        elif time_frame == '30m' or time_frame == '30M':
            period = '30min'
        elif time_frame == '1h' or time_frame == '1H':
            period = '60min'
        elif time_frame == '4h' or time_frame == '4H':
            period = '4hour'
        elif time_frame == '1d' or time_frame == '1D':
            period = '1day'
        else:
            return ("【交易提醒】交易所: Huobi k线周期错误，k线周期只能是【1m, 5m, 15m, 30m, 1h, 4h, 1d】之一")
        records = self.__huobi_spot.get_kline(self.__instrument_id, period=period)['data']
        length = len(records)
        j = 1
        list = []
        while j < length:
            for item in records:
                item = [ts_to_utc_str(item['id']), item['open'], item['high'], item['low'], item['close'], item['vol'],
                        round(item['amount'], 2)]
                list.append(item)
                j += 1
        return list

    def get_position(self):
        """获取当前交易对的计价货币的可用余额，如当前交易对为ETC-USDT, 则获取的是ETC的可用余额"""
        receipt = self.__huobi_spot.get_balance_currency(self.__account_id, self.__currency)
        direction = 'long'
        amount = receipt[self.__currency]
        price = None
        result = {'direction': direction, 'amount': amount, 'price': price}
        return result

    def get_ticker(self):
        receipt = self.__huobi_spot.get_ticker(self.__instrument_id)
        last = receipt['tick']['close']
        return {"last": last}

    def get_contract_value(self):
        return {self.__symbol: 1}