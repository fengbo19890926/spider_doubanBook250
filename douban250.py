import sqlite3
from spider_db import Spider
    
def insert(db_name,table_name,info):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql='insert into '+table_name+' values(?,?,?,?,?,?,?,?,?,?,?,?,?)'
    c.execute(sql,(None,
        info['作品'],
        info['作者'],
        info['出版社'],
        info['出品方'],
        info['原作名'],
        info['译者'],
        info['出版年'],
        info['页数'],
        info['定价'],
        info['装帧'],
        info['ISBN'],
        info['内容简介']))
    conn.commit() 
    conn.close()


def select_data(db_name,table_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql = 'select * from '+table_name
    result = c.execute(sql)
    return result

def create_table(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql = '''CREATE TABLE  IF NOT EXISTS doubanbook250 (
    ID INTEGER PRIMARY KEY,
    name           TEXT,
    writer         TEXT,
    pub_house      TEXT,
    pub_company    TEXT,
    origin_name    TEXT,
    interpreter    TEXT,
    pub_time       TEXT,
    page_num       TEXT,
    price          TEXT,
    bind           TEXT,   
    ISBN           TEXT,
    content        TEXT
);'''
    c.execute(sql)
    print('添加表成功')

spider = Spider()
infos = spider.go()
create_table('test.db')
for info in infos:
    insert('test.db','doubanbook250',info)
print('插入数据成功')



