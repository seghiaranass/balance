from odoo import fields, models, api, _
from datetime import datetime ,timedelta
from odoo.exceptions import UserError

from calendar import monthrange
import logging
_logger = logging.getLogger(__name__)

class Balance(models.Model):
    _name = "balance"
    _sql_constraints = [
    ('unique_reference', 'UNIQUE(reference)', _('Reference must be unique.')),
    ]
    
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _description = "This model for calculationg balance every add or modification"
    _order = 'created_datetime desc'

    _rec_name = 'display_name'
    invoice_id = fields.Many2one('account.move', string="Invoice")

    create_uid = fields.Many2one('res.users', 'Created by')
    creator_image = fields.Binary(related='create_uid.image_1920', string="Creator's Image", readonly=True)
    creator_display = fields.Html(string="Created By", compute="_compute_creator_display")
    reference = fields.Char(required=True,track_visibility='always')
    created_datetime = fields.Datetime(string="Due Date", default=fields.Datetime.now)
    new_due_datetime = fields.Datetime(string="Original Date", default=fields.Datetime.now)
    paymentDate = fields.Datetime(string="Payment Date", default=False)

    modified_datetime = fields.Datetime(string="Modified Date", readonly=True)
    amount = fields.Float(required=True)
    balance = fields.Float(compute="_compute_balance", store=True)
    description = fields.Html(string="Description")
    customer_id = fields.Integer()
    customer_name = fields.Many2one('res.partner', string="Customer Name")
    customer_display = fields.Html(string="Customer", compute="_compute_customer_display")

    customer_image = fields.Binary(related='customer_name.image_1920', string="Logo", readonly=True)
    balance_tags_ids = fields.Many2many(
            'balance.tags', 
            'balance_balance_tags_rel', 
            'balance_id', 'tag_id', 
            string='Tags'
        )
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
    

    balance_correction = fields.Boolean(string="Balance Correction", default=False)
    estimated_payment = fields.Boolean(string="Estimated",default=False)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    
    tooltip_field = fields.Char(string="Tooltip Field", compute="_compute_tooltip_field")


    last_in_month = fields.Boolean(string="Malik ?", compute='_compute_last_in_month' ,default=False,store=True)


    
    transaction_type = fields.Selection([
    ('debit', 'DEBIT'),
    ('credit', 'CREDIT')
], string='Transaction Type', default=False)


    month_year = fields.Char(string='Month & Year', compute='_compute_month_year')

    @api.depends('created_datetime')
    def _compute_month_year(self):
        for record in self:
            if record.created_datetime:
                date_obj = fields.Date.from_string(record.created_datetime)
                record.month_year = date_obj.strftime('%B %Y')
            else:
                record.month_year = ''

    @api.depends('description')
    def _compute_tooltip_field(self):
        for record in self:
            record.tooltip_field = record.description 


    @api.onchange('transaction_type')
    def _onchange_transaction_type(self):
        # If the transaction type is 'debit', ensure the amount is negative
        if self.transaction_type == 'debit' and self.amount > 0:
            self.amount = -self.amount
        # If the transaction type is 'credit', ensure the amount is positive
        elif self.transaction_type == 'credit' and self.amount < 0:
            self.amount = abs(self.amount)

    @api.onchange('amount')
    def _onchange_amount(self):
        # This ensures the sign is correct even if the user manually changes the amount
        if self.transaction_type == 'debit' and self.amount > 0:
            self.amount = -self.amount
        elif self.transaction_type == 'credit' and self.amount < 0:
            self.amount = abs(self.amount)

    @api.depends('create_uid', 'create_uid.image_1920')
    def _compute_creator_display(self):
        for rec in self:
            image_url = "/web/image?model=res.users&id=%s&field=image_1920" % rec.create_uid.id
            rec.creator_display = '<img src="%s" title="" style="width: 19px; height: 19px;  border-radius:50%%; vertical-align: middle; margin-right: 5px;"/> %s' % (image_url, rec.create_uid.name)
    @api.depends('customer_name', 'customer_name.image_1920')
    def _compute_customer_display(self):
        for rec in self:
            if rec.customer_name:
                image_url = "/web/image?model=res.partner&id=%s&field=image_1920" % rec.customer_name.id
                rec.customer_display = '<img src="%s" title="" style="width: 70px; height: 15px; vertical-align: middle; margin-right: 5px;"/> %s' % (image_url, rec.customer_name.name)
            else:
                rec.customer_display = "No Customer"

    @api.depends('reference')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.reference or ''

    # @api.depends('amount', 'created_datetime', 'balance_correction')
    # def _compute_balance(self):
    #     # Fetch all records, sorted by datetime
    #     all_records = self.env['balance'].search([], order='created_datetime, id')
        
    #     running_balance = 0

    #     for rec in all_records:
    #         if rec.balance_correction:
    #             # If it's a correction, set balance to the record's amount
    #             rec.balance = rec.amount
    #             # Also update the running balance
    #             running_balance = rec.amount
    #         else:
    #             # Else, keep adding the record's amount to running balance
    #             running_balance += rec.amount
    #             rec.balance = running_balance
    def recompute_balances_from_date(self, start_date):
        
        prior_record = self.env['balance'].search([('created_datetime', '<', start_date)], order='created_datetime desc', limit=1)

        running_balance = prior_record.balance if prior_record else 0

        affected_records = self.env['balance'].search([('created_datetime', '>=', start_date)], order='created_datetime, id')
        
        for record in affected_records:
            if record.balance_correction:
                running_balance = record.amount
            else:
                running_balance += record.amount
            record.balance = running_balance

    def write(self, vals):
        recalculate_from_date = False

        if 'created_datetime' in vals:
            original_date = self.created_datetime
    
            adjusted_datetime = fields.Datetime.from_string(vals['created_datetime']) + timedelta(hours=1)
            selected_date = adjusted_datetime.date()
            current_time = fields.Datetime.from_string(fields.Datetime.now()).time()
            combined_datetime = datetime.combine(selected_date, current_time)
            vals['created_datetime'] = combined_datetime

            new_date = fields.Datetime.from_string(vals['created_datetime'])
            if new_date < original_date:
                recalculate_from_date = new_date
            else:
                recalculate_from_date = original_date
        elif 'amount' in vals or 'balance_correction' in vals:
            recalculate_from_date = self.created_datetime

        res = super(Balance, self).write(vals)

        if recalculate_from_date:
            self.recompute_balances_from_date(recalculate_from_date)


        return res

    @api.model
    def create(self, vals):
        if 'created_datetime' in vals:
            adjusted_datetime = fields.Datetime.from_string(vals['created_datetime']) + timedelta(hours=1)
            selected_date = adjusted_datetime.date()
            current_time = fields.Datetime.from_string(fields.Datetime.now()).time()
            combined_datetime = datetime.combine(selected_date, current_time)
            vals['created_datetime'] = combined_datetime

        rec = super(Balance, self).create(vals)

        # If the new record is created with 'balance_correction', or it affects the order
        if vals.get('balance_correction', False) or 'amount' in vals or 'created_datetime' in vals:
            self.recompute_balances_from_date(vals['created_datetime'])

        return rec

    
    def unlink(self):
        # Get the earliest date being deleted
        earliest_date = min(self.mapped('created_datetime'))
        
        res = super(Balance, self).unlink()
        
        # Recompute balances from the earliest deleted date onwards
        self.recompute_balances_from_date(earliest_date)

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
                    'new_due_datetime': fields.Datetime.to_string(combined_datetime),
                    'amount': invoice.amount_residual or 0.0,
                }
                # This will invoke the create method which already recomputes the balance
                self.create(vals)



    def action_open_invoice(self):
        self.ensure_one()
        
        if not self.invoice_id:
            raise UserError(_("This balance does not have a linked invoice."))
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.invoice_id.id,
            'target': 'current',
        }

    
    def copy(self, default=None):
        default = dict(default or {})  # ensure default is a dictionary

        # modify reference field value
        ref = self.reference or ''
        default['reference'] = '{}_copy'.format(ref)

        return super(Balance, self).copy(default) 

    def set_to_validate(self):
        self.write({'state': 'validate'})

    def set_to_paid(self):
        self.write({'state': 'paid'})

    def set_to_draft(self):
        self.write({'state': 'draft'})
        
    def your_button_method(self):
        # Your action code here
        pass


    def download_as_sql(self):
        # Ensure some records are selected
        if not self:
            raise UserError(_('Please select some records.'))

        # Return the SQL as a downloadable file
        record_ids = ','.join(str(record.id) for record in self)
        url = '/balance/download_sql?record_ids=%s' % record_ids
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }



    @api.depends('month_year')
    def _compute_last_in_month(self):
        _logger.info("`````````````````````````````````*******************************")
