from odoo import api, fields, models

class BalanceTags(models.Model):
    _name = 'balance.tags'
    _description = 'Balance Tags'

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index', default=10)  # This gives a color to the tag in the UI

    # If you want a tag description or other fields, add them here
