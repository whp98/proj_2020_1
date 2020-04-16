import pymongo
import json
import zlib
import numpy as np
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
    #外网测试
    #myclient = pymongo.MongoClient('mongodb://redis.intellij.xyz:27017/')
    # 内网运行
    myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    dblist = myclient.list_database_names()

    if "OKEx" in dblist:
        print("数据库存在")
    else:
        print("不存在")

    mydb=myclient['OKEx']

    collist = mydb.list_collection_names()

    # collist = mydb.collection_names()
    if "OKEx" in collist:   # 判断 sites 集合是否存在
        print("集合已存在！")
    else:
        print("集合不存在")

    mycol_trade = mydb['spot/trade']

    mycol_depth = mydb['spot/depth']

    for item in ps.listen():
        if item['type'] == 'message':               # data = {"table":"spot/depth","action":"partial",
            data = inflate(item['data'])            # "data":[{"instrument_id":"BTC-USDT"],
            dataCurr = json.loads(data)             # "asks":[["7227.1","2.8876",33],[]], "bids":[[],[]],
            tbData = dataCurr.get('table')          # "timestamp":" "}
            if tbData=="spot/trade" :
                for data_trade in dataCurr.get('data'):
                    mycol_trade.insert_one(data_trade)
            else:
                for data_depth in dataCurr.get('data'):
                    mycol_depth.insert_one(data_depth)



if __name__ == '__main__':
    prep()