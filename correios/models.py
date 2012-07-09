import re
from datetime import datetime


class Status(object):
    re_localizacao_nacional = re.compile(r'(?P<correios>.*) - (?P<cidade>.*)/(?P<estado>\w{2})')
    re_localizacao_internacional = re.compile(r'(?P<pais>.*) - .*')
    # http://acheirelevante.blogspot.com.br/2012/02/significado-de-siglas-utilizadas-pelo.html

    def __init__(self, *args):
        self.atualizacao = datetime.strptime(args[0], '%d/%m/%Y %H:%M')
        try:
            self.agencia, self.cidade, self.estado = self.re_localizacao_nacional.match(args[1]).groups()
            self.pais = 'BRASIL'
        except AttributeError:
            self.agencia = self.cidade = self.estado = None
            self.pais = self.re_localizacao_internacional.match(args[1]).groups()[0]
        self.situacao = args[2]

        try:
            self.observacao = args[3]
        except IndexError:
            self.observacao = None

    def __str__(self):
        return '{} {} em {}\n{} {}\n{}, {}/{}'.format(
            self.atualizacao.date(),
            self.atualizacao.time(),
            self.agencia,
            self.situacao,
            self.observacao or '',
            self.pais,
            self.cidade,
            self.estado
        )


class Encomenda(object):
    def __init__(self, identificador):
        self.identificador = identificador
        self.status = []

    def adicionar_status(self, status):
        self.status.append(status)
        self.status.sort(key=lambda status: status.atualizacao)

    def __str__(self):
        return repr(self.identificador)
