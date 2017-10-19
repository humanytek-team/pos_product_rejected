odoo.define('pos_product_rejected.pos', function (require) {
    "use strict";

    var screens = require('point_of_sale.screens');
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var _t = core._t;
    var Model = require('web.DataModel');

    screens.PaymentScreenWidget.include({
        validate_order: function(force_validation) {
            var self = this;
            var _super = this._super;
            var order = this.pos.get_order();
            var orderlines = order.get_orderlines();
            var client = order.get_client();
            var PosOrderLine = new Model('pos.order.line');
            var partner_id = client === null ? client : client.id;
            var orderlines_data = [];
            var order_data = {'partner_id': partner_id};

            for (var i = 0; i < orderlines.length; i++) {
                var line = orderlines[i];
                var line_data = {};
                line_data.product_id = line.product.id;
                line_data.quantity = line.quantity;
                orderlines_data.push(line_data);
            }

            PosOrderLine
              .call(
                'check_product_stock',
                [order_data, orderlines_data])
              .then(function(result){                
                _super.call(self, force_validation);
              });
        }
    });
});
