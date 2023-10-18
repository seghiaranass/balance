from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)

class SaleOrderInherit(models.Model):
    _inherit = ['sale.order']

    def write(self, values):
        old_values = {}
        for field in values.keys():
            if self._fields[field].type == 'many2one' and self[field]:
                old_values[field] = self[field].name or self[field].display_name
            else:
                old_values[field] = self[field]
        
        result = super().write(values)
        
        messages = []
        for field, old_value in old_values.items():
            if self._fields[field].type == 'many2one' and self[field]:
                new_value = self[field].name or self[field].display_name
            else:
                new_value = self[field]
                
            if old_value != new_value:
                field_label = self._fields[field].string or field
                messages.append(f"{field_label}: {old_value} -> {new_value}")
        
        message_body = "<br/>".join(messages)
        if message_body:
            for order in self:
                order.message_post(body=message_body)

        return result
