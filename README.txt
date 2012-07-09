===============
python-correios
===============

API Python Correios para rastreamento de encomendas.


Exemplo
=======

Utilização básica::

    #-*- encoding: utf-8 -*-
    from correios import Correios
    encomenda = Correios.get_encomenda('RA222491899CN')

    print 'Encomenda:', encomenda.identificador
    for status in encomenda.status:    
        print 'Data da atualização:', status.atualizacao.date()
        print 'Hora da atualização:', status.atualizacao.time()
        print 'País:', status.pais
        print 'Estado:', status.estado
        print 'Cidade:', status.cidade
        print 'Agência:', status.agencia
        print 'Situação:', status.situacao
        print 'Observação:', status.observacao
        print
