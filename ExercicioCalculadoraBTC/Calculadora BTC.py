import yfinance as yf

from datetime import datetime, timedelta
from binance.client import Client


class Main():

    periodo_inicio = input("Escolha a data de inicio(%Y-%m-%d): ")
    periodo_fim = input("Escolha a data final(%Y-%m-%d): ")
    intervalo = int(input("Dia do mês: "))
    valor_investido =int(input("Valor que sera investido por mês: "))

    preco_btc = []  # 1 btc = preco_btc
    preco_dolar = []  # 1 dolar = R$ preco_dolar
    data_venda = datetime.strptime(periodo_fim, "%Y-%m-%d")

    data_format = data_venda + timedelta(days=1)

    def preco_bitcoin(self):
        ticker = yf.Ticker("BTC-USD")
        historico = ticker.history(start=self.periodo_inicio, end=self.periodo_fim)

        for data, row in historico.iterrows():
            data_formatada = data.strftime('%Y-%m-%d')
            if data.day == self.intervalo:
                fechamento = row["Close"]
                
                result = format(fechamento, '.2f')
                result = float(result)
                self.preco_btc.append(result)

    def preco_brl_to_usd(self):

        client = Client()
        symbol = "USDTBRL"
        interval = Client.KLINE_INTERVAL_1DAY
        klines = client.get_historical_klines(symbol, interval,self.periodo_inicio, self.periodo_fim)

        for k in klines:
            tempo = datetime.fromtimestamp(k[0] / 1000)
            abertura = float(k[1])
            alta = float(k[2])
            baixa = float(k[3])
            fechamento = float(k[4])
            if tempo.day == self.intervalo:

                self.preco_dolar.append(fechamento)


p1 = Main()
p1.preco_brl_to_usd()
p1.preco_bitcoin()


class Calculadora(Main):
    carteira_bitcoin = []
    carteira_dolar = []
    def compra_dolar(self):
        for i in range(len(super().preco_dolar)):
            dolar = super().valor_investido / super().preco_dolar[i]
            result = format(dolar, '.2f')
            result = float(result)
            self.carteira_dolar.append(result)

    def compra_btc(self):
        for i in range(len(self.carteira_dolar)):
            btc = self.carteira_dolar[i] / super().preco_btc[i]

            self.carteira_bitcoin.append(btc)


p2= Calculadora()
p2.compra_dolar()
p2.compra_btc()


class Resultado(Calculadora, Main):
    def soma_tudo(self):
        soma = sum(super().carteira_bitcoin)

        return soma

    def venda_btc(self):
        ticker = yf.Ticker("BTC-USD")
        historico = ticker.history(start=super().data_venda, end=super().data_format)
        for data, row in historico.iterrows():
            data_formatada = data.strftime('%Y-%m-%d')
            fechamento = row["Close"]
            preco_btc = format(fechamento, '.2f')
            preco_btc = float(preco_btc)
            lucro_in_usd = float(format(self.soma_tudo() * preco_btc, '.2f'))

        client = Client()
        symbol = "USDTBRL"
        interval = Client.KLINE_INTERVAL_1DAY
        klines = client.get_historical_klines(symbol, interval, str(super().data_venda), str(super().data_format))

        for k in klines:
            tempo = datetime.fromtimestamp(k[0] / 1000)
            abertura = float(k[1])
            alta = float(k[2])
            baixa = float(k[3])
            fechamento = float(k[4])
            preco_brl = format(fechamento, '.1f')
            preco_brl = float(preco_brl)
            lucro_in_brl = lucro_in_usd * preco_brl

        print("")
        print(f'Comprando todo dia {super().intervalo} de cada mês entre {super().periodo_inicio} e {super().periodo_fim} teriamos um aporte de: ')
        print(f'{self.soma_tudo()} em BITCOIN')
        print("")
        print(f'Realizando a venda de tudo na data {super().data_format} onde o preco do BITCOIN é/era ${preco_btc:.2f} e a cotação USD > BRL era R$ {preco_brl:.2f}' )
        print(f'Obtemos um lucro de R$ {lucro_in_brl:.2f} REAIS ')
        print("")
        print(f'TOTAL INVESTIDO: R$ {super().valor_investido * len(super().preco_btc):.2f}')
        print(f'RETORNO: R$ {lucro_in_brl:.2f}')


p3 = Resultado()
p3.venda_btc()
















