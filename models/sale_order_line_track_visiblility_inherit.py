from odoo import api, models,fields

class SaleOrderLineTrackVisibilityInherit(models.Model):
    _inherit = 'sale.order'

    product_uom_qty = fields.Float(track_visibility='always')