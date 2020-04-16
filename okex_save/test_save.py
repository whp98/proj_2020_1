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
    myclient = pymongo.MongoClient('mongodb://redis.intellij.xyz:27017/')
    # 内网运行
    #myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    dblist = myclient.list_database_names()

    if "OKEx" in dblist:
        print("数据库存在")
    else:
        print("不存在")

    mydb=myclient['OKEx']

    collist = mydb.list_collection_names()

    # collist = mydb.collection_names()
    if "spot/trade" in collist:   # 判断 sites 集合是否存在
        print("集合已存在！")
    else:
        print("集合不存在")

    mycol_trade = mydb['spot/trade']

    mycol_depth = mydb['spot/depth']
    #代码测试策略
    #连续接受1000条数据，开始精确查询
    #如果这些数据全部找到就输出可靠
    #否则输出不可靠
    list_trade=[]
    lise_depth=[]
    i=0
    for item in ps.listen():
        if i>999:
            break
        i=i+1
        if item['type'] == 'message':               # data = {"table":"spot/depth","action":"partial",
            data = inflate(item['data'])            # "data":[{"instrument_id":"BTC-USDT"],
            dataCurr = json.loads(data)             # "asks":[["7227.1","2.8876",33],[]], "bids":[[],[]],
            tbData = dataCurr.get('table')          # "timestamp":" "}
            if tbData=="spot/trade" :
                for data_trade in dataCurr.get('data'):
                    list_trade.append(data_trade)
            else:
                for data_depth in dataCurr.get('data'):
                    lise_depth.append(data_depth)

    #开始查询
    flag1 = True
    flag2 = True
    for dataOfTrade in list_trade:
        myquery=dataOfTrade
        result = mycol_trade.find(myquery)
        for x in result:
            if x['trade_id']!=dataOfTrade['trade_id'] :
                flag1=False

    for dataOfDpeth in lise_depth:
        myquery=dataOfDpeth
        result = mycol_trade.find(myquery)
        for x in result:
            if x['checksum']!=dataOfDpeth['checksum']:
                flag2=False
    if(flag1 and flag2):
        print("可靠")
    else:
        print("不可靠")
if __name__ == '__main__':
    prep()
