from odoo import api, models,fields
from datetime import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'


    def action_post(self):
        # First, call the super method to actually post the invoice
        res = super(AccountMove, self).action_post()

        # Then, create the balance record for posted invoices
        for move in self:
            if move.state == 'posted' and move.move_type == 'out_invoice':
                invoice_date = move.invoice_date_due
                current_time = fields.Datetime.from_string(fields.Datetime.now()).time()
                combined_datetime = datetime.combine(invoice_date, current_time)
                # Create values for the balance record
                vals = {
                    'reference': move.name or '',
                    'customer_name': move.partner_id.id,
                    'created_datetime':  fields.Datetime.to_string(combined_datetime),
                    'amount': move.amount_residual or 0.0,
                    'invoice_id': move.id
                }
                # Create the balance record
                self.env['balance'].create(vals)

        return res


    def unlink(self):
        # Find related balance records based on the reference
        for move in self:
            if move.state == 'posted' and move.move_type == 'out_invoice':
                balance_records = self.env['balance'].search([('reference', '=', move.name)])
                # Unlink (delete) related balance records
                balance_records.unlink()

        # Then, proceed to delete the invoice by calling the super method
        return super(AccountMove, self).unlink()
    

    def button_draft(self):
            # Find related balance records based on the reference
            for move in self:
                if move.state == 'posted' and move.move_type == 'out_invoice':
                    balance_records = self.env['balance'].search([('reference', '=', move.name)])
                    # Unlink (delete) related balance records
                    balance_records.unlink()

            # Then, proceed to reset the invoice to draft by calling the super method
            return super(AccountMove, self).button_draft()
    