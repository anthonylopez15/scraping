import json

import requests

URL_BASE = 'https://veiculos.fipe.org.br/api/'

endpoints = {
    'CONSULTAR_MARCAS': URL_BASE + 'veiculos/ConsultarMarcas',
    'CONSULTAR_MODELOS': URL_BASE + 'veiculos/ConsultarModelos',
    'CONSULTAR_ANO_MODELO': URL_BASE + 'veiculos/ConsultarAnoModelo',
    'CONSULTAR_MODELO_ATRAVES_ANO': URL_BASE + 'veiculos/ConsultarModelosAtravesDoAno',
    'CONSULTAR_VALOR_COM_TODOS_OS_PARAM': URL_BASE + 'veiculos/ConsultarValorComTodosParametros',
}


def request_post(url, obj):
    jsonb = requests.post(url, data=obj)
    return jsonb


def request_get(url):
    jsonb = requests.get(url)
    return jsonb


class Carro:
    def __init__(self):
        self.veiculo = None
        self.ano = None
        self.marca = None
        self.descricao = None
        self.vendido = None


class Marca:
    def __init__(self):
        self.nome = None
        self.value = None


class Veiculos:
    def __init__(self):
        self.codigoTipoVeiculo = None
        self.codigoTabelaReferencia = None
        self.codigoModelo = None
        self.codigoMarca = None
        self.ano = None
        self.codigoTipoCombustivel = None
        self.anoModelo = None
        self.modeloCodigoExterno = None
        self.tipoConsulta = "tradicional"
        self.tipoVeiculo = "carro"

    def consultar_marcas(self):
        url = endpoints['CONSULTAR_MARCAS']
        body = {
            "codigoTipoVeiculo": self.codigoTipoVeiculo,
            "codigoTabelaReferencia": self.codigoTabelaReferencia
        }
        jsonb = request_post(url, body)
        return jsonb.text

    def consultar_modelos(self):
        url = endpoints['CONSULTAR_MODELOS']
        body = {
            "codigoTipoVeiculo": self.codigoTipoVeiculo,
            "codigoTabelaReferencia": self.codigoTabelaReferencia,
            "codigoMarca": self.codigoMarca
        }
        jsonb = request_post(url, body)
        return jsonb.text

    def consultar_ano_modelo(self):
        url = endpoints['CONSULTAR_ANO_MODELO']
        body = {
            "codigoTipoVeiculo": self.codigoTipoVeiculo,
            "codigoTabelaReferencia": self.codigoTabelaReferencia,
            "codigoMarca": self.codigoMarca,
            "codigoModelo": self.codigoModelo
        }
        jsonb = request_post(url, body)
        return jsonb.text

    def consultar_modelos_atravez_ano(self):
        url = endpoints['CONSULTAR_MODELO_ATRAVES_ANO']
        body = {
            "codigoTipoVeiculo": self.codigoTipoVeiculo,
            "codigoTabelaReferencia": self.codigoTabelaReferencia,
            "codigoMarca": self.codigoMarca,
            "codigoModelo": self.codigoModelo,
            "ano": self.ano,
            "codigoTipoCombustivel": self.codigoTipoCombustivel,
            "anoModelo": self.anoModelo,
        }
        jsonb = request_post(url, body)
        return jsonb.text

    def consultar_valor_com_todos_parametros(self):
        url = endpoints['CONSULTAR_VALOR_COM_TODOS_OS_PARAM']
        body = {
            "codigoTipoVeiculo": self.codigoTipoVeiculo,
            "codigoTabelaReferencia": self.codigoTabelaReferencia,
            "codigoMarca": self.codigoMarca,
            "codigoModelo": self.codigoModelo,
            "ano": self.ano,
            "codigoTipoCombustivel": self.codigoTipoCombustivel,
            "anoModelo": self.anoModelo,
            "modeloCodigoExterno": "",
            "tipoConsulta": self.tipoConsulta,
            "tipoVeiculo": self.tipoVeiculo
        }
        jsonb = request_post(url, body)
        return jsonb.text

    def popular_carro(self, carro: Carro):
        # url = "35.198.47.55:3333"
        url = "http://35.215.207.254:3333/veiculos"
        body = {
            "veiculo": carro.veiculo,
            "ano": carro.ano,
            "marca": carro.marca,
            "descricao": carro.descricao,
            "vendido": carro.vendido
        }
        jsonb = requests.post(url, data=json.dumps(body))
        return jsonb.text

    def popular_marca(self, m: Marca):
        # url = "35.198.47.55:3333"
        url = "http://35.215.207.254:3333/marcas"
        body = {
            "marca": m.nome,
            "value": m.value
        }
        jsonb = requests.post(url, data=json.dumps(body))
        return jsonb.text


if __name__ == '__main__':
    carros = list()
    marcs = list()

    count = 0

    veiculos = Veiculos()
    veiculos.codigoTipoVeiculo = 1
    veiculos.codigoTabelaReferencia = 274

    marcas = veiculos.consultar_marcas()
    marcas_list = json.loads(marcas)
    for item in marcas_list:
        if count == 5:
            break
        try:
            marca = Marca()
            marca.nome = item["Label"]
            marca.value = item["Value"]
            print(f"Marca: {marca.nome}")
            veiculos.popular_marca(marca)
            marcs.append(marca)

            veiculos.codigoMarca = item["Value"]
            modelos = veiculos.consultar_modelos()
            modelos_dict = json.loads(modelos)
            for mod in modelos_dict["Modelos"]:
                veiculos.codigoModelo = mod["Value"]
                ano_modelo = json.loads(veiculos.consultar_ano_modelo())
                for combustivel in ano_modelo:
                    veiculos.ano = combustivel["Value"]
                    veiculos.anoModelo = combustivel["Value"][:-2]
                    veiculos.codigoTipoCombustivel = combustivel["Value"][-1:]
                    all_params = veiculos.consultar_valor_com_todos_parametros()
                    params = json.loads(all_params)
                    # if params["codigo"] != "0":
                    carro = Carro()
                    carro.veiculo = params["Modelo"]
                    carro.marca = params["Marca"]
                    carro.ano = params["AnoModelo"]
                    combus = params["Combustivel"]
                    carro.descricao = f"{combus} - {carro.ano}"
                    if count % 3 == 0:
                        carro.vendido = True
                    else:
                        carro.vendido = False

                    print(f"Modelo: {carro.veiculo} - Marca: {carro.marca} - Ano: {carro.ano} - Vendido: {carro.vendido}")
                    veiculos.popular_carro(carro)
                    carros.append(carro)
                    count += 1
        except Exception as e:
            print(e)

