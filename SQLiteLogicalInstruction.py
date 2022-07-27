from msilib import type_binary
from multiprocessing.sharedctypes import Value
import sqlite3
import time
import json
import datetime
import pandas as pd
import re

sqldb_path = r'\\Tw100049146\data\Kaiying\0725\Data.db'


def InsertDataTabel(Tabel,InsertDataObj):
    mydb=sqlite3.connect(sqldb_path)
    cursor = mydb.cursor()
    # try:
    sql = f"INSERT INTO '{Tabel}' ("
    i=1
    for key,value in InsertDataObj.items():
        sql+=f"'{key}'"
        if len(InsertDataObj) != i:
            sql += f","
        else:
            sql +=f")"
        i+=1
    sql += "VALUES ("
    i=1
    for key,value in InsertDataObj.items():
        sql+=f"'{value}'"
        if len(InsertDataObj) != i:
            sql += f","
        else:
            sql +=f")"
        i+=1
    sql += ";"
    print(sql)
    cursor.execute(sql)
    mydb.commit()
    mydb.close()
    return sql
    # except:
    #     return False

def UpDataSetWhereTabel(Table,SetDataObj,WhereObj):
    mydb=sqlite3.connect(sqldb_path)
    cursor = mydb.cursor()
    try:
        sql = f"UPDATE '{Table}' SET "
        i=1
        for key,value in SetDataObj.items():
            sql += f"{key} = '{value}' "
            if len(SetDataObj) != i:
                sql += f", "
            else:
                sql +=f"WHERE "
            i+=1
        i=1
        for key,value in WhereObj.items():
            sql += f"{key} = '{value}' "
            if len(WhereObj) != i:
                sql += f"and "
            else:
                sql +=f"; "
            i+=1
        print(sql)
        # mydb.execute(sql)  
        cursor.execute(sql)
        mydb.commit()  
        cursor.close()
        mydb.close()
        return sql
    except:
        return False


def SelectWhatWhereTabel(Table,WhatArr,WhereObj):
    mydb=sqlite3.connect(sqldb_path)
    cursor = mydb.cursor()
    try:
        sql = f"SELECT "
        i=1
        for key in WhatArr:
            sql += f"{key}"
            if WhatArr.index(key) != len(WhatArr)-1:
                sql +=f","

        sql += f" from '{Table}' where "
        i=1
        for key,value in WhereObj.items():
            sql += f"{key} = '{value}' "
            if len(WhereObj) != i:
                sql += f"and "
            else:
                sql +=f";"
            i+=1
        print(sql)
        cursor.execute(sql)
        Redata = cursor.fetchall()
        mydb.commit()
        mydb.close()
        return Redata
    except:
        return False

#

def SelectWhereTabel(Table,WhereObj):
    mydb=sqlite3.connect(sqldb_path)
    cursor = mydb.cursor()
    try:
        sql = f"SELECT * from '{Table}' where "
        i=1
        for key,value in WhereObj.items():
            sql += f"{key} = '{value}' "
            if len(WhereObj) != i:
                sql += f"and "
            else:
                sql +=f";"
            i+=1
        print(sql)
        cursor.execute(sql)
        
        Redata = cursor.fetchall()
        col = cursor.description
        mydb.commit()
        mydb.close()
        return Redata
    except:
        return False


def DeleteWhereTabel(Table,WhereObj):
    mydb=sqlite3.connect(sqldb_path)
    cursor = mydb.cursor()
    try:
        sql = f"DELETE from '{Table}' where "
        i=1
        for key,value in WhereObj.items():
            sql += f"{key} = '{value}' "
            if len(WhereObj) != i:
                sql += f"and "
            else:
                sql +=f";"
            i+=1
        print(sql)
        cursor.execute(sql)
        mydb.commit()
        mydb.close()
        return sql
    except:
        return False

#----------------------------------pd 寫入與讀取--------------------------------------------

def PDInserDataTable(Tabel,InsertDataObj): 
    KeyArr = []
    for key,value in InsertDataObj.items():
        KeyArr.append(key)
    print(KeyArr)
    df_add = pd.DataFrame(columns=KeyArr)
    try :
        to_sql =df_add.append(InsertDataObj, ignore_index=True)
        mydb_1=sqlite3.connect(sqldb_path)
        cursor_1=mydb_1.cursor()
        to_sql.to_sql(name=Tabel ,con=mydb_1,if_exists='append',index=False)
        cursor_1.close()
        mydb_1.close()
        print("[正確] 資料庫更新")
        return True
    except:
        print("[錯誤] 資料庫未更新")
        return False

def PDSelectWhereTabel(Table,WhereObj = None):
    mydb=sqlite3.connect(sqldb_path)
    try:
        if WhereObj == None:
            sql =f"SELECT * from '{Table}'"
        else:
            sql = f"SELECT * from '{Table}' where "
            i=1
            for key,value in WhereObj.items():
                sql += f"{key} = '{value}' "
                if len(WhereObj) != i:
                    sql += f"and "
                else:
                    sql +=f";"
                i+=1
            print(sql)
        print(sql)
        qdf = pd.read_sql_query(f"{sql}", mydb)
        mydb.close()
        qdf = json.loads(qdf.to_json(orient='records'))
        return qdf
    except:
        return False


def PDSelectWhatWhereTabel(Table,WhatArr = None,WhereObj = None):
    mydb=sqlite3.connect(sqldb_path)
    try:
        if WhatArr==None:
            sql =f"SELECT * from '{Table}'"
        else:
            sql=f"SELECT "
            for i in range(len(WhatArr)):
                print(WhatArr[i])
                sql +=str(WhatArr[i])
                if len(WhatArr)-1 != i:
                    sql+=","
                else:
                    sql+=f" from '{Table}'"
        if WhereObj == None:
            pass
        else:
            sql += f" where "
            i=1
            for key,value in WhereObj.items():
                sql += f"{key} = '{value}' "
                if len(WhereObj) != i:
                    sql += f"and "
                else:
                    sql +=f";"
                i+=1
        
        qdf = pd.read_sql_query(f"{sql}", mydb)
        mydb.close()
        qdf = json.loads(qdf.to_json(orient='records'))
        return qdf
    except:
        return False

def PDSelectSQL(sql):
    mydb=sqlite3.connect(sqldb_path)
    try:
        print(sql)
        qdf = pd.read_sql_query(f"{sql}", mydb)
        mydb.close()
        qdf = json.loads(qdf.to_json(orient='records'))
        return qdf
    except:
        return False



def SELECTSQL(sql):
    mydb=sqlite3.connect(sqldb_path)
    cursor = mydb.cursor()
    try:
        cursor.execute(sql)
        Redata = cursor.fetchall()
        mydb.commit()
        mydb.close()
        return Redata
    except:
        return False

# SELECT * FROM web_action_history
# WHERE update_time <= '2022-06-16'

# SELECT * FROM web_action_history
# WHERE update_time > datetime('now','-3 days','localtime')

# SELECT * FROM web_action_history
# WHERE update_time BETWEEN '2022-06-13' and '2022-06-16'

# SELECT count(update_time)
# FROM web_action_history
# WHERE update_time BETWEEN '2022-06-13' and '2022-06-16' 
# AND Action = 'StartRun'

# SELECT count(update_time)
# FROM web_action_history
# WHERE update_time > datetime('now','-3 days','localtime')
# AND Action = 'Login'
