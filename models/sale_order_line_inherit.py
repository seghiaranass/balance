from odoo import api, models,fields
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLineInherit(models.Model):
    _inherit = ['sale.order.line']

    def write(self, values):
        result = super().write(values)
        orders = self.mapped('order_id')
        for order in orders:
            order.message_post(body="Hello worlds")