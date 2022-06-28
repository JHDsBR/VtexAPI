from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/")
def Index():
    return "<h1>Olá, mundo!</h1>"


@app.route("/<user>")
def Users(user):
    return f"<h1>Olá, {user}</h1>"


@app.route("/mostrar-letra/<a>")
def Test_(a):
    # return f"<p>{str(a)*9999}</p>"
    return f"Test() -> {request.data}"


@app.get("/test")
def Test():
    return f"Test() -> {request.data}"


@app.post("/fazer-cadastro") # {"accountName":"","AppKey":"","AppToken":"","excel":""}
def Cadastro():
    res                 = {}
    body                = json.loads(request.data)
    bodyOk              = DataIsOk(body)
    res["body status"]  = bodyOk[1]

    if (bodyOk[0]):
        SetProducts(body, res)

    return res




def Headers(AppKey, AppToken):

    return {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-VTEX-API-AppKey": str(AppKey),
                "X-VTEX-API-AppToken": str(AppToken)
           }

def DataIsOk(body):
    expected = ["accountName","AppKey","AppToken","excel"]
    checkout = {"accountName":"Not Ok","AppKey":"Not Ok","AppToken":"Not Ok","excel":"Not Ok"}
    count = 0

    for k,v in body.items():
        if(k in expected):
            checkout[k] = "Ok"
            count+=1

        # checkout.pop(k, None)

    return count == 4 , checkout


def SetProducts(body, res):
    headers = Headers(body["AppKey"], body["AppToken"])
    # url = "https://{{accountName}}.vtexcommercestable.com.br/api/catalog/pvt/product"
    res["Produtos"] = "Ok"
    SetSku(headers, body, res)



def SetSku(headers, body, res):
    # url = "https://{{accountName}}.vtexcommercestable.com.br/api/catalog/pvt/stockkeepingunit"
    res["Sku"] = "Ok"
    SetImages(headers, body, res)


def SetImages(headers, body, res):
    # url = f"https://{{accountName}}.vtexcommercestable.com.br/api/catalog/pvt/stockkeepingunit/{skuId}/file"
    res["Imagens"] = "Ok"
    SetPrice(headers, body, res)


def SetPrice(headers, body, res):
    # url = f"https://api.vtex.com/{{acountName}}/pricing/prices/{Id}"
    res["Price"] = "Ok"
    return res
