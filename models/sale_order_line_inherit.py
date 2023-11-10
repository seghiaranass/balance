from odoo import api, models, fields
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLineInherit(models.Model):
    _inherit = ['sale.order.line']


    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if 'order_id' in vals and 'purchase_price' in vals:
    #             order = self.env['sale.order'].browse(vals['order_id'])
    #             if order.partner_id.property_account_position_id:
    #                 _logger.info("Applying multiplier to purchase_price...")
    #                 vals["purchase_price"] = float(vals["purchase_price"]) * 1.2
    #             else:
    #                 _logger.info("property_account_position_id is not set for the partner.")

    #     return super().create(vals_list)
    
    
    def write(self, values):


        if self.purchase_price and self.order_id.partner_id.property_account_position_id:
            _logger.info(self.order_id.partner_id.property_account_position_id)

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
