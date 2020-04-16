# import websocket
import zlib
import json
import numpy as np
import time
import redis

def inflate(data):
    decompress = zlib.decompressobj(
        -zlib.MAX_WBITS
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    if isinstance(inflated, bytes):
        return str(inflated, encoding='utf-8')
    return inflated

def prep():
    # recv = redis.StrictRedis(host='127.0.0.1', port='6379', db=0)
    recv = redis.StrictRedis(host='149.129.87.222', port='6379', db=0)
    ps = recv.pubsub()
    ps.subscribe('OKEx')
    # asksDeep = {}
    # bidsDeep = {}
    # turnover = [0.0] * 2
    # deeplimit = [0.0] * 204
    # price = 0
    # f = open('OKEx.csv', 'w', newline='')
    # csv_writer = csv.writer(f)

    for item in ps.listen():
        if item['type'] == 'message':               # data = {"table":"spot/depth","action":"partial",
            data = inflate(item['data'])            # "data":[{"instrument_id":"BTC-USDT"],
            dataCurr = json.loads(data)             # "asks":[["7227.1","2.8876",33],[]], "bids":[[],[]],
            tbData = dataCurr.get('table')          # "timestamp":" "}
            print(dataCurr)
            print(tbData)



if __name__ == '__main__':
    prep()