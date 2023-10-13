from odoo import api, models,fields

class SaleOrderLineTrackVisibilityInherit(models.Model):
    _name = "sale_order.line.track.visiblility.inherit"
    _description = "This model only to add track visiblity to sale order line model  "

    _inherit = 'sale.order.line'


    product_uom_qty = fields.Float(track_visibility='always')