from odoo import api, fields, models
from datetime import timedelta
import time
from datetime import datetime ,timedelta
class BalanceChangeDueDateWizard(models.TransientModel):
    _name = 'balance.change.due.date.wizard'
    _description = 'Balance Change Wizard'

    new_datetime = fields.Datetime(string='New Datetime', required=True)

   

    def action_change_datetime(self):
        active_ids = self.env.context.get('active_ids', [])
        balance_records = self.env['balance'].browse(active_ids)
        for record in balance_records:
            record.created_datetime = self.new_datetime

        return {'type': 'ir.actions.act_window_close'}