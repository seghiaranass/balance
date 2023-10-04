from odoo import fields, models, api 
from datetime import datetime
class Balance(models.Model):
    _name = "balance"
    _description = "This model for calculationg balance every add or modification"
    _order = 'created_datetime desc'

    reference = fields.Char(required=True)
    created_datetime = fields.Datetime(string="Due Date", default=fields.Datetime.now)
    modified_datetime = fields.Datetime(string="Modified Date", readonly=True)
    amount = fields.Float(required=True)
    balance = fields.Float(compute="_compute_balance", store=True)
    description = fields.Html(string="Description")
    customer_id = fields.Integer()
    customer_name = fields.Many2one('res.partner', string="Customer Name")

    payment_type = fields.Selection([
            ('virement', 'Virement'),
            ('cheque', 'Chèque'),
            ('lcn', 'LCN'),
            ('prelevement', 'Prélèvement'),
            ('autre', 'Autre'),
        ], string='Payment Type', default='virement')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validate', 'Validated'),
        ('paid', 'Paid'),
        ], string='Status', readonly=True, default='draft')

    @api.depends('amount', 'created_datetime')
    def _compute_balance(self):
        # Fetching all records up to the current one
        all_records = self.env['balance'].search([], order='created_datetime, id')
        running_balance = 0.0  # Initializing a running balance
        
        for rec in all_records:
            # Calculate balance based on running balance and the record amount
            rec.balance = running_balance + rec.amount
            running_balance = rec.balance

    def write(self, vals):
        vals['modified_datetime'] = fields.Datetime.now()
        res = super(Balance, self).write(vals)
        
        if 'amount' in vals or 'created_datetime' in vals:
            # Recompute balance for all records
            all_records = self.env['balance'].search([], order='created_datetime')
            for record in all_records:
                record._compute_balance()

        return res

    @api.model
    def create(self, vals):
        record = super(Balance, self).create(vals)
        # Recompute balance for all records
        all_records = self.env['balance'].search([], order='created_datetime')
        for r in all_records:
            r._compute_balance()

        return record
    
    def unlink(self):
        # Get the earliest date being deleted
        earliest_date = min(self.mapped('created_datetime'))
        
        res = super(Balance, self).unlink()
        
        # Get all records from the earliest deleted date and recompute their balance
        subsequent_records = self.env['balance'].search(
            [('created_datetime', '>=', earliest_date)], order='created_datetime')
        
        for record in subsequent_records:
            record.balance = 0.0
            record._compute_balance()

        return res


    @api.model
    def fetch_invoice_data(self, *args):
        # Filtering invoices that are posted and are of type 'out_invoice'
        
        invoice_ids = self.env['account.move'].search([('state', '=', 'posted'), ('move_type', '=', 'out_invoice')])
        for invoice in invoice_ids:
            invoice_date = invoice.invoice_date_due
            current_time = fields.Datetime.from_string(invoice.create_date).time()
            combined_datetime = datetime.combine(invoice_date, current_time)
            existing_record = self.env['balance'].search([('reference', '=', invoice.name)], limit=1)
            if not existing_record:
                vals = {
                    'reference': invoice.name or '',
                    'customer_name': invoice.partner_id.id,
                    'created_datetime': fields.Datetime.to_string(combined_datetime),
                    'amount': invoice.amount_residual or 0.0,
                }
                # This will invoke the create method which already recomputes the balance
                self.create(vals)

    def set_to_validate(self):
        self.write({'state': 'validate'})

    def set_to_paid(self):
        self.write({'state': 'paid'})

    def set_to_draft(self):
        self.write({'state': 'draft'})
