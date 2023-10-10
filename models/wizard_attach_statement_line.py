# models/wizard_attach_statement_line.py

from odoo import fields, models, api

class WizardAttachStatementLine(models.TransientModel):
    _name = 'wizard.attach.statement.line'
    _description = 'Attach Statement Line to Balance'

    balance_id = fields.Many2one('balance', string='Balance')
    statement_line_ids = fields.Many2many(
        'account.bank.statement.line', string='Statement Lines to Attach' )

    # def button_attach(self):
    #     for line in self.statement_line_ids:
    #         line.balance_id = [(6, 0, [self.balance_id])] 
    #     return {'type': 'ir.actions.act_window_close'}
    
    def button_attach(self):
        # Link the selected statement lines to the balance record
        self.balance_id.statement_line_ids = [(4, line.id) for line in self.statement_line_ids]
        return {'type': 'ir.actions.act_window_close'}
