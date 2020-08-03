from purequant.config import config
from purequant.monitor import position_update

config.loads('config.json')

position_update()