from odoo import api, models,fields

class SaleOrderLineTrackVisibilityInherit(models.Model):
    _inherit = 'sale.order.line'

    product_uom_qty = fields.Float(track_visibility='always')