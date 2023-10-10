from odoo import fields, models

class BankStatementLineInherited(models.Model):
    _inherit = 'account.bank.statement.line'
    
    balance_id = fields.Many2one('balance', string='Balance')
