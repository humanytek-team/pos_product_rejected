# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Record automatically a negation for a product in pos orders',
    'description': '''Records automatically a negation for products that is
    intended be sold but has no stock.
    The record is done on validation of a pos order. Extends function (JS) of
    validation of POS order to check stock for products, if the stock is
    negative then is registered automatically a negation (product_rejected) for
    product.''',
    'version': '9.0.0.1.0',
    'category': 'Point Of Sale',
    'author': 'Humanytek',
    'website': "http://www.humanytek.com",
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
        'stock',
        'product_rejected',
        ],
    'data': [
        'templates.xml',
    ],
    'installable': True,
    'auto_install': False
}
