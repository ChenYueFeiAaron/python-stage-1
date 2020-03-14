import pymongo
conn = pymongo.MongoClient('localhost',27017)
db = conn.pic

myset = db.pict
'''
try:
    f = open('uk.jpg','rb')
except:
    pass
else:
    data = f.read()

    sql = [{'name':'bird','des':data}]
    myset.insert(sql)
f.close()
'''
try:
    f = open('tt.jpg','wb')
except:
    pass

data = myset.find_one({"name":"bird"})

data1 = data['des']
f.write(data1)
f.close()