from odoo import api, models, fields
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLineInherit(models.Model):
    _inherit = ['sale.order.line']

    def write(self, values):
        old_values = {field: self[field] for field in values.keys()}
        
        result = super().write(values)
        
        messages = []
        for field, old_value in old_values.items():
            new_value = self[field]
            if old_value != new_value:
                field_label = self._fields[field].string or field
                messages.append(f"{field_label}: {old_value} -> {new_value}")
        
        message_body = "<br/>".join(messages)
        if message_body and 'order_id' in self._fields:
            orders = self.mapped('order_id')
            for order in orders:
                order.message_post(body=message_body)

        return result
