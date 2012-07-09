#-*- encoding: utf-8 -*-
import urllib2
import re
from HTMLParser import HTMLParser
from models import Status, Encomenda


class EncomendaParser(HTMLParser):
    def __init__(self, html):
        HTMLParser.__init__(self)
        self.in_td = False
        self.data = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.in_td = True

    def handle_data(self, data):
        if self.in_td:
            self.data.append(data)

    def handle_endtag(self, tag):
        self.in_td = False


class Correios(object):
    URL = 'http://websro.correios.com.br/sro_bin/txect01$.QueryList?P_ITEMCODE=&P_LINGUA=001&P_TESTE=&P_TIPO=001&P_COD_UNI='
    RE_DATE = re.compile(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}')

    def _get_encomenda_status(self, html):
        parser = EncomendaParser(html)
        data = parser.data[3:] # table header
        parser.close()

        if not data:
            raise CorreiosException('Object not found')

        intervals = [data.index(x) for x in data if Correios.RE_DATE.match(x)]
        intervals.append(len(data))

        status = []
        for x in intervals:
            try:
                status.append(Status(*data[x:intervals[intervals.index(x)+1]]))
            except IndexError:
                break

        if not status:
            raise CorreiosException('Status not found')

        return status

    @staticmethod
    def get_encomenda(identificador):
        request = urllib2.urlopen('%s%s' % (Correios.URL, identificador))
        html = request.read()
        request.close()

        if html:
            encomenda = Encomenda(identificador)
            [encomenda.adicionar_status(status) for status in Correios()._get_encomenda_status(html)]

            return encomenda


class CorreiosException(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return repr(self.code)

