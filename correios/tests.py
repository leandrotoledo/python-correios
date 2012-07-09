#-*- encoding: utf-8 -*-
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

import os
import sys
import unittest
from datetime import datetime

root = os.path.dirname(os.path.abspath(__file__))
os.chdir(root)
sys.path.insert(0, os.path.dirname(root))
sys.path.insert(0, root)

from correios import *


class CorreiosTests(unittest.TestCase):
    def test_get_encomenda(self):
        encomenda = Correios.get_encomenda('RA222491899CN')

        assert len(encomenda.status) == 4

        primeiro_status = encomenda.status[0]
        assert primeiro_status.atualizacao == datetime(2012, 2, 19, 3, 28)
        assert primeiro_status.pais == 'CHINA'
        assert primeiro_status.situacao == 'Postado'

        ultimo_status = encomenda.status[-1]
        assert ultimo_status.atualizacao == datetime(2012, 5, 03, 19, 36)
        assert ultimo_status.pais == 'BRASIL'
        assert ultimo_status.estado == 'SP'
        assert ultimo_status.cidade == 'SAO BERNARDO'
        assert ultimo_status.agencia == 'CDD RUDGE RAMOS'
        assert ultimo_status.situacao == 'Entrega Efetuada'


def main():
    unittest.main()


if __name__ == '__main__':
    main()
