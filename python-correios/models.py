import re
from datetime import datetime


class Status(object):
    re_localizacao = re.compile(r'(?P<correios>.*) - (?P<cidade>.*)/(?P<estado>\w{2})')
    # http://acheirelevante.blogspot.com.br/2012/02/significado-de-siglas-utilizadas-pelo.html

    def __init__(self, *args):
        self.atualizacao = datetime.strptime(args[0], '%d/%m/%Y %H:%M')
        self.agencia, self.cidade, self.estado = self.re_localizacao.match(args[1]).groups()
        self.situacao = args[2]

        try:
            self.observacao = args[3]
        except IndexError:
            self.observacao = None


class Encomenda(object):
    def __init__(self, identificador):
        self.identificador = identificador
        self.status = []

    def adicionar_status(self, status):
        self.status.append(status)
        self.status.sort(key=lambda status: status.atualizacao)
