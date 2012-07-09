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


class CorreiosScraper(object):
    def __init__(self):
        self.url = 'http://websro.correios.com.br/sro_bin/txect01$.QueryList?P_ITEMCODE=&P_LINGUA=001&P_TESTE=&P_TIPO=001&P_COD_UNI='
        self.re_date = re.compile(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}')

    def _get_encomenda_status(self, html):
        parser = EncomendaParser(html)
        data = parser.data[3:] # table header
        parser.close()

        intervals = [data.index(x) for x in data if self.re_date.match(x)]
        intervals.append(len(data))

        status = []
        for x in intervals:
            try:
                status.append(Status(*data[x:intervals[intervals.index(x)+1]]))
            except IndexError:
                break

        return status

    def get_encomenda(self, identificador):
        request = urllib2.urlopen('%s%s' % (self.url, identificador))
        html = request.read()
        request.close()

        if html:
            encomenda = Encomenda(identificador)
            [encomenda.adicionar_status(status) for status in self._get_encomenda_status(html)]
            return encomenda
