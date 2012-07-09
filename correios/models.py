"""
API Python Correios - Rastreamento de Encomendas
Copyright (C) 2012  Leandro T. de Souza <leandrotoledo@member.fsf.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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


class Encomenda(object):
    def __init__(self, identificador):
        self.identificador = identificador
        self.status = []

    def adicionar_status(self, status):
        self.status.append(status)
        self.status.sort(key=lambda status: status.atualizacao)

    def __str__(self):
        return repr(self.identificador)
