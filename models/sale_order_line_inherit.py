from odoo import api, models,fields
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLineInherit(models.Model):
    _inherit = ['sale.order.line']

    def write(self, values):
        result = super().write(values)
        _logger.info("Heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")