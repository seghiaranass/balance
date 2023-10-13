from odoo import api, models,fields

class SaleOrderLineTrackVisibilityInherit(models.Model):
    _inherit = 'sale.order.line'

    product_uom_qty = fields.Float(
        string="Quantity",
        compute='_compute_product_uom_qty',
        digits='Product Unit of Measure', default=1.0,
        store=True, readonly=False, required=True, precompute=True,track_visibility='always')