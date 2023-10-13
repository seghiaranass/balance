from odoo import api, models,fields

class SaleOrderLineTrackVisibilityInherit(models.Model):
    _inherit = 'sale.order.line'
    _name = "sale.order.line.track.visibility.inherit"
    _description = "This model only to add track visiblity to sale order line model  "



    product_uom_qty = fields.Float(track_visibility='always')