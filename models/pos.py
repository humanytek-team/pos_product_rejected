# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from datetime import datetime

from openerp import api, models


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    @api.model
    def _create_product_negation(self, product_qty, partner_id, product):
        """Record a negation for product of pos order line"""

        ProductRejected = self.env['product.rejected']
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ProductRejected.create({
            'product_tmpl_id': product.product_tmpl_id.id,
            'product_id': product.id,
            'partner_id': partner_id,
            'qty': product_qty,
            'date': date_now,
            'company_id': self.env.user.company_id.id,
            })

    @api.model
    def check_product_stock(self, order_data, orderlines_data):
        """Checks stock for products in lines of POS orders"""

        Product = self.env['product.product']
        ProductRejected = self.env['product.rejected']

        for line in orderlines_data:
            product = Product.browse(line['product_id'])

            if product.type == 'product':
                product_qty = line['quantity']

                if product_qty > (product.qty_available - product.outgoing_qty):

                    if order_data['partner_id']:

                        limit_hours = \
                            self.env.user.company_id.product_rejected_limit_hours
                        if limit_hours > 0:

                            last_product_negation = ProductRejected.search([
                                ('product_id', '=', product.id),
                                ('partner_id', '=', order_data['partner_id']),
                                ('company_id', '=', self.env.user.company_id.id),
                                ], order='date')

                            if last_product_negation:

                                last_product_negation_date = \
                                    last_product_negation[-1].date
                                last_product_negation_datetime = \
                                    datetime.strptime(
                                        last_product_negation_date,
                                        '%Y-%m-%d %H:%M:%S')
                                now = datetime.now()
                                diff = now - last_product_negation_datetime
                                hours_diff = (diff.seconds / 60.0) / 60
                                if hours_diff > limit_hours:
                                    self._create_product_negation(
                                        product_qty,
                                        order_data['partner_id'],
                                        product)

                            else:
                                self._create_product_negation(
                                    product_qty,
                                    order_data['partner_id'],
                                    product)

                        else:
                            self._create_product_negation(
                                product_qty,
                                order_data['partner_id'],
                                product)

                    else:
                        self._create_product_negation(
                            product_qty,
                            order_data['partner_id'],
                            product)
