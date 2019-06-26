from flask import Flask,request
from flask_restful import Resource, Api
from flask import jsonify
import pymysql

app = Flask(__name__)
api = Api(app)
host = "127.0.0.1"
user = "root"
password = ""
db = "gemdataset"
def db_connect() :
    con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()
    return cur

cur = db_connect()

def getDatabyCatnameAndOem(cat,oem,model) :

    query ='select * from oem_data where category = %s AND OEM =%s and Model =%s'

    cur.execute(query,(cat,oem,model))
    result = cur.fetchall()
    return result

def getAllkeydataByfieldName(index):
    names = ["Model", "OEM", "Category"]
    qry = 'selct distinct(%s) from oem_data'
    cur.execute(qry,names[index])
    result = cur.fetchall()
    return result

def getAllcat(oem):
    qry = 'select DISTINCT(Category) from oem_data where OEM =%s'
    cur.execute(qry,oem)
    result = cur.fetchall()
    return result

def getAllmodels(oem,cat):
    qry = 'select DISTINCT(Model) from oem_data where OEM =%s and Category= %s '
    cur.execute(qry,(oem,cat))
    result = cur.fetchall()
    return result

def getAlloems():
    qry = 'select DISTINCT(OEM) from oem_data'
    cur.execute(qry)
    result = cur.fetchall()
    return result

#example      
@app.route('/')
def db_query():
    cat = 'Laptop'
    oem = 'Dell'
    resultdata = getDatabyCatnameAndOem(cat,oem)

    return jsonify(resultdata) 

# endpoint to get data from oem
@app.route("/getdata", methods=["POST"])
def add_user():
    categ = request.json['cat']
    oem = request.json['oem']
    model = request.json['model']
    resultdata = getDatabyCatnameAndOem(categ,oem,model)
    return jsonify(resultdata)

@app.route("/getcategory", methods=["POST"])
def all_category():
    oem = request.json['oem']
    cats = getAllcat(oem)
    return jsonify(cats)

@app.route("/getmodel", methods=["POST"])
def all_model():
    categ = request.json['cat']
    oem = request.json['oem']
    
    models = getAllmodels(oem,categ)
    return jsonify(models)

@app.route("/getoem", methods=["GET"])
def all_oem():
    oems = getAlloems()
    return jsonify(oems)


if __name__ == '__main__':

    app.run(debug=True)
    