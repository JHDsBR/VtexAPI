from flask import Flask, request
import json
import base64
import tempfile
from time import sleep
import os
from flask_cors import CORS
from random import randint


app = Flask(__name__)
CORS(app)

@app.route("/")
def Index():
    return "<h1 style='color:blue;'>Olá, mundo2!</h1>"


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


@app.route("/verificar-cadastro")
def verificarCadastro():
    return str([x for x in os.walk("MyTmp")])


@app.post("/fazer-cadastro") # {"accountName":"","AppKey":"","AppToken":"","excel":""}
def Cadastro():
    print("teste")
    res                 = {}
    body                = json.loads(request.data)
    # temp_name = next(tempfile._get_candidate_names())
    # with tempfile.TemporaryDirectory() as tmp:
    #     path = os.path.join(tmp, 'something')
    #     os.mkdir(path)
    #     print(tmp)
    #     sleep(4)
    # return "😼"

    # print(body)
    bodyOk              = DataIsOk(body)
    res["body status"]  = bodyOk[1]

    if (bodyOk[0]):
        print("deu certo meu parceiro 😼")
        with open(f"MyTmp/{body["accountName"]}-{randint(0,9999999999)}.xlsx", "wb") as excel:
            excel.write(base64.b64decode(body["excel"]))
        SetProducts(body, res)

    return res


def Headers(AppKey, AppToken):

    return {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-VTEX-API-AppKey": str(AppKey),
                "X-VTEX-API-AppToken": str(AppToken)
           }


# verifica se o body da requisição está de acordo com o esperado
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


def ProductsPayloads():
    return {
            "Name":"",  # diferente
            "CategoryId":"", # igual
            "BrandName":"", # igual
            # "LinkId":"", # igual
            # "RefId":"", # igual
            # "IsVisible":"", # igual
            # "Description":"", # igual
            # "DescriptionShort":"", # igual
            # "KeyWords":"", # igual
            # "Title":"", # igual
            # "IsActive":"", # igual
            # "MetaTagDescription":"", # igual
            # "Score":"" # igual
           }






def SetProducts(body, res):
    # Cadastro de Produto: Name

    headers = Headers(body["AppKey"], body["AppToken"])

    #
    # for i, name in enumerate(df["Name"]):
    #     payloads = ProductsPayloads()
    #     categoria = int(df.loc[i, "CategoryId"])
    #     marca = str(df.loc[i, "BrandName"])
    #     link = str(df.loc[i, "LinkId"])
    #     ref = str(df.loc[i, "RefId"])
    #     visivel = bool(df.loc[i, "IsVisible"])
    #     descricao = str(df.loc[i, "Description"])
    #     descripequena = str(df.loc[i, "DescriptionShort"])
    #     palavrachave = str(df.loc[i, "KeyWords"])
    #     titulo = str(df.loc[i, "Title"])
    #     ativo = bool(df.loc[i, "IsActive"])
    #     metatag = str(df.loc[i, "MetaTagDescription"])
    #     ponto = int(df.loc[i, "Score"])
    #
    #     response = requests.post(url, headers=headers, json=payloads).json()
    #
    #     cadastrar_produto = load_workbook('/app/workspace/Planilha3.xlsx')
    #     ws = cadastrar_produto.active
    #     coluna = 'O'
    #     linha = str(i+2)  # responde
    #     ws[coluna+linha] = response['Id']
    #     cadastrar_produto.save('/app/workspace/Planilha3.xlsx')
    #

    # url = "https://{{accountName}}.vtexcommercestable.com.br/api/catalog/pvt/product"
    res["Produtos"] = "Ok"
    SetSku(headers, body, res)



def SetSku(headers, body, res):
    # Cadastro de SKU: ProductId, Name, PackagedHeight, PackagedLength, PackagedWidth, PackagedWeightKg
    # url = "https://{{accountName}}.vtexcommercestable.com.br/api/catalog/pvt/stockkeepingunit"
    res["Sku"] = "Ok"
    SetImages(headers, body, res)


def SetImages(headers, body, res):
    # Cadastro de Imagem: skuId, Name, url
    # url = f"https://{{accountName}}.vtexcommercestable.com.br/api/catalog/pvt/stockkeepingunit/{skuId}/file"
    res["Imagens"] = "Ok"
    SetPrice(headers, body, res)


def SetPrice(headers, body, res):
    # Cadastro de preço: itemId, tradePolicyId, markup, costprice
    # url = f"https://api.vtex.com/{{acountName}}/pricing/prices/{Id}"
    res["Price"] = "Ok"
    return res



# fluxo
"""
mandar produto com [Name,CategoryId,BrandId]

{
   "Name": "insert product test",
   "DepartmentId": 1,
   "CategoryId": 2,
   "BrandId": 2000000,
   "LinkId": "insert-product-test",
   "RefId": "310117869",
   "IsVisible": true,
   "Description": "texto de descrição",
   "DescriptionShort": "Utilize o CEP 04548-005 para frete grátis",
   "ReleaseDate": "2019-01-01T00:00:00",
   "KeyWords": "teste,teste2",
   "Title": "product de teste",
   "IsActive": true,
   "TaxCode": "",
   "MetaTagDescription": "tag test",
   "SupplierId": 1,
   "ShowWithoutStock": true,
   "AdWordsRemarketingCode": null,
   "LomadeeCampaignCode": null,
   "Score": 1
}

Nome
corda
requeridos
Nome do produto.

CategoryPath
corda
Caminho das categorias associadas a este produto, do nível mais alto da categoria ao nível mais baixo, separados por /. É obrigatório usar este campo ou o CategoryIdcampo.

Categoria ID
inteiro
ID de uma categoria existente que será associada a este produto. É obrigatório usar este campo ou o CategoryPathcampo.

Marca
corda
Nome da marca que será associada a este produto. É obrigatório usar este campo ou o BrandIdcampo. Caso deseje criar uma nova marca, ou seja, caso a marca ainda não exista, utilize este campo ao invés de BrandId.

ID da marca
inteiro
ID de uma Marca existente que será associada a este produto. É obrigatório usar este campo ou o BrandNamecampo.

LinkId
corda
Slug que será usado para construir a URL da página do produto. Caso não informado, será gerado de acordo com o nome do produto substituindo espaços e caracteres especiais por hífens ( -).

RefId
corda
Código de referência do produto.

É visível
boleano
Mostra ( true) ou oculta ( false) o produto no resultado da pesquisa e nas páginas do produto, mas o produto ainda pode ser adicionado ao carrinho de compras. Geralmente aplicável para presentes.

Descrição
corda
Descrição do produto.

DescriçãoCurta
corda
Breve descrição do produto. Essas informações podem ser exibidas na página do produto e na prateleira, usando os seguintes controles:
Estrutura da loja: $product.DescriptionShort.
Portal CMS legado: <vtex.cmc:productDescriptionShort/>.

Data de lançamento
corda
Usado para auxiliar na ordenação do resultado da pesquisa do site. Usando a O=OrderByReleaseDateDESCstring de consulta, você pode extrair esse valor e mostrar a ordem de exibição por data de lançamento. Esse atributo também é usado como condição para coleções dinâmicas.

Palavras-chave
corda
Estrutura da loja: obsoleta.
Portal CMS legado: palavras-chave ou sinônimos relacionados ao produto, separados por vírgula ( ,). "Televisão", por exemplo, pode ter uma palavra substituta como "TV". Este campo é importante para tornar suas pesquisas mais abrangentes.

Título
corda
Tag do título do produto. É apresentado na guia do navegador e corresponde ao título da página do produto. Este campo é importante para SEO.

Está ativo
boleano
Ativar ( true) ou inativar ( false) produto.

Código de Imposto
corda
Código de imposto do produto, usado para cálculo de imposto.

MetaTagDescrição
corda
Breve descrição do produto para SEO. Recomenda-se não exceder 150 caracteres.

Mostrar Sem Estoque
boleano
Se true, ativa a opção Notifique-me quando o produto estiver esgotado.


Pontuação
inteiro
Valor usado para definir a prioridade na página de resultados da pesquisa.

















"""
