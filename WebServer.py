from flask import Flask,jsonify,render_template,request, url_for,redirect,session,make_response
from urllib.parse import unquote
import datetime
import json,requests
import os
import csv
import json
import codecs
#自定義模組
from SQLiteDB import SQLiteLogicalInstruction
#籃圖impoet
#宣告flask基本註冊
app = Flask(__name__, static_folder='public', static_url_path="")

#設置flask-Key
key =os.urandom(16).hex()
app.secret_key=key #session key
#連結flask_restful與flask

#登入網址 #設置IP與Port
LocIP = "10.96.78.216" #伺服器API-IP
Port = 5000

@app.route('/') #登入後首頁
def index():
    return render_template('index.html')
#/TEST
@app.route('/TEST',methods=['GET','POST']) #登入後首頁
def TEST():
    if request.method =='GET':
        r=SQLiteLogicalInstruction.PDSelectWhereTabel('Test')
        return jsonify(r)
    if request.method =='POST':
        data =json.loads(request.get_data(as_text=True))
        print(data)
        rArr = []
        for i in data:
            r = SQLiteLogicalInstruction.UpDataSetWhereTabel('Test',i,{'D1':i['D1']})
            rArr.append(r)
        return jsonify({"r":r})

		@app.route('/ABC',methods=['GET','POST']) # IP:5000/ABC 路由API
def ABC():
    data=json.loads(request.get_data(as_text=True)) #<<<收到資料
    print(data)
    #     InsertDataTabel(Tabel,InsertDataObj)
    # Obj代表傳入物件會根據key = value
    # Ex: InsertDataObj = {
    #  Name:鄭楷穎
    # }會新增欄位Name為鄭楷穎的一筆資料

    SQLiteLogicalInstruction.InsertDataTabel('Test',data)
    return jsonify({"Result":"OK"})

##呼叫這個API (其他電腦)python 
#data {
# KEY:Value
# }
# data = 123,456,789  
#Arr = data.split(',')
#Arr = [123,456,789]

#----↓ B電腦(無SQL) 自強當自強
# data {
# "欄位一",Value,
# "欄位二",vAlue,
# }
# r = requests.post("http://10.96.78.216:5000/ABC",data =  json.dumps(data))
# print(r.text) >>{"Result":"OK"}
if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False 
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
    app.run(host=f"{LocIP}",debug='true',port=Port)
