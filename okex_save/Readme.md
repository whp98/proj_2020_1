# Mongo DB 存储交易数据并且验证数据是否可靠


## 任务

- [x] 成功接受来自香港服务器转发的数据
- [x] 设计了一个很简单的数据存储方案也就是将转发的数据直接存入Mongo DB
- [x] 使用简单的代码验证连续的数据存入Mongo DB
- [x] depth 和 trade 数据分开存储 

## 具体过程

我之前想用java实现这些操作，没想到数据解压部分我用了几个小时都不行，虽然解压代码在python代码中我实在不能在java中重写这个解压代码，于是重新选择python来搞，直接在老代码的基础上进行修改


我决定使用比较简单的数据库来进行操作，最终选择Mongo DB，这玩意很简单

我就那交易数据直接放在里面
最后脚本放在ECS 使用nohup 直接长时间运行数据库插入脚本

为了测试数存储据的可靠性，我决定使用一个连续数据的验证策略，收集连续的数据来验证数据库中是否存储这些数据

下面是具体的策略


## 数据存储策略

我直接在docker 里面开启了一个Mongo DB容器
挂载了一个数据的文件夹
```bash
mkdir /mongo
docker run -p 27017:27017 -v /mongo:/data/db --name docker_mongodb -d mongo

```

连接数据库并且准备插入数据

```python
myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb=myclient['OKEx']
mycol_trade = mydb['spot/trade']
mycol_depth = mydb['spot/depth']
```

分开插入交易数据

```python
if tbData=="spot/trade" :
    for data_trade in dataCurr.get('data'):
        mycol_trade.insert_one(data_trade)
else:
    for data_depth in dataCurr.get('data'):
        mycol_depth.insert_one(data_depth)python

```

## 数据验证策略

在上面的代码上修改就可以了我这里的操作是将代码运行在我自己的电脑上，连续收集1000条数据，然后逐一去查询这个数据，然后将查出来的数据和收集到的数据做对比如果不符合就输出不可靠可靠就输出可靠

数据收集部分

```python
list_trade=[]
lise_depth=[]
i=0
for item in ps.listen():
    if i>999:
        break
    i=i+1
    if item['type'] == 'message': 
        if tbData=="spot/trade" :
            for data_trade in dataCurr.get('data'):
                list_trade.append(data_trade)
        else:
            for data_depth in dataCurr.get('data'):
                lise_depth.append(data_depth)
        
```

数据验证部分

```python
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
```

验证结果

![](img/2020-04-17-11-46-25.png)