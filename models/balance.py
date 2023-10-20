from odoo import fields, models, api, _
from datetime import datetime ,timedelta
from odoo.exceptions import UserError
from datetime import date
import random
import logging
_logger = logging.getLogger(__name__)

class Balance(models.Model):
    _name = "balance"
    _sql_constraints = [
    ('unique_reference', 'UNIQUE(reference)', _('Reference must be unique.')),
    ]
    
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _description = "This model for calculationg balance every add or modification"
    _order = 'created_datetime desc, amount desc , state asc'

    _rec_name = 'display_name'
    invoice_id = fields.Many2many('account.move', 'account_balance_rel', 'balance_id', 'account_move_id',string="Invoice", domain=[('move_type', 'in', ['in_invoice', 'out_invoice'])],tracking=True)
    is_favorite = fields.Boolean(string='Favorite',default=False)

    create_uid = fields.Many2one('res.users', 'Created by')
    creator_image = fields.Binary(related='create_uid.image_1920', string="Creator's Image", readonly=True)
    creator_display = fields.Html(string="Created By", compute="_compute_creator_display")
    reference = fields.Char(required=True,tracking=True)
    created_datetime = fields.Datetime(string="Due Date", default=fields.Datetime.now,tracking=True)
    new_due_datetime = fields.Datetime(string="Original Date", default=fields.Datetime.now,tracking=True)
    paymentDate = fields.Datetime(string="Payment Date", default=False,tracking=True)

    modified_datetime = fields.Datetime(string="Modified Date", readonly=True)
    amount = fields.Float(required=True,tracking=True)
    amount_str = fields.Char(string='Amount String', compute='_compute_amount_str',store=True)

    balance = fields.Float(compute="_compute_balance", store=True)
    description = fields.Html(string="Description")
    customer_id = fields.Integer()
    customer_name = fields.Many2one('res.partner', string="Customer Name",tracking=True)
    customer_display = fields.Html(string="Customer", compute="_compute_customer_display")

    customer_image = fields.Binary(related='customer_name.image_1920', string="Logo", readonly=True)
    balance_tags_ids = fields.Many2many(
            'balance.tags', 
            'balance_balance_tags_rel', 
            'balance_id', 'tag_id', 
            string='Tags',
            tracking=True
        )
    payment_type = fields.Selection([
            ('virement', 'Virement'),
            ('cheque', 'Chèque'),
            ('lcn', 'LCN'),
            ('prelevement', 'Prélèvement'),
            ('autre', 'Autre'),
            ('versement', 'Versement'),
        ], string='Payment Type', default='virement')
        
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validate', 'Validated'),
        ('paid', 'Paid'),
        ], string='Status', readonly=True, default='draft')
    

    balance_correction = fields.Boolean(string="Balance Correction", default=False,tracking=True)
    estimated_payment = fields.Boolean(string="Estimated",default=False,tracking=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    
    tooltip_field = fields.Char(string="Tooltip Field", compute="_compute_tooltip_field")


    last_in_month = fields.Boolean(string="Malik ?", compute='_compute_last_in_month' ,default=False,store=True)


    
    transaction_type = fields.Selection([
    ('debit', 'DEBIT'),
    ('credit', 'CREDIT')
], string='Transaction Type', default=False,tracking=True)


    month_year = fields.Char(string='Month & Year', compute='_compute_month_year')
    # statement_line_ids = fields.One2many(
    #         'account.bank.statement.line', 'balance_id', string='Statement Lines' ,)

    statement_line_ids = fields.Many2many(
    'account.bank.statement.line',
    'balance_statement_line_rel',
    'balance_id',
    'statement_line_id',
    string='Statement Lines')


    created_date_part = fields.Date(string='Created Date', compute='_compute_created_datetime_only_date_part',store=True)
    is_week = fields.Boolean(string='Is Week', compute='_compute_is_week' , default=False,store=True)
    is_month = fields.Boolean(string='Is Month', compute='_compute_is_month' , default=False,store=True)
    is_next_month = fields.Boolean(string='Is Next Month', compute='_compute_is_next_month' , default=False,store=True)
    

    # po number of client 
    invoice_order_number = fields.Char(string = "Order Number")



    @api.depends('created_datetime')
    def _compute_created_datetime_only_date_part(self):
        for record in self:
            record.created_date_part = fields.Datetime.from_string(record.created_datetime).date()





    # @api.depends('created_datetime')
    # def _compute_is_week(self):
    #     today = date.today()
    #     start_of_week = today - timedelta(days=today.weekday())
    #     end_of_week = start_of_week + timedelta(days=6)

    #     for record in self:
    #         if start_of_week <= record.created_datetime.date() <= end_of_week:
    #             record.is_week = record.created_datetime
    #         else:
    #             record.is_week = False

    # @api.depends('created_datetime')
    # def _compute_is_month(self):
    #     today = date.today()
    #     start_of_month = today.replace(day=1)
    #     if today.month == 12:
    #         end_of_month = today.replace(year=today.year+1,month=1,day=1)
    #     else:
    #         end_of_month = today.replace(month=today.month + 1, day = 1)

    #     for record in self:
    #         if start_of_month  <= record.created_datetime.date() <= end_of_month:
    #             record.is_month = record.created_datetime
    #         else:
    #             record.is_month = False
                
    # @api.depends('created_datetime')
    # def _compute_is_next_month(self):
    #     today = date.today()

    #     if today.month == 12:
    #         start_of_next_month  = today.replace(year=today.year+1, month=1, day=1)
    #     else:
    #         start_of_next_month  =  today.replace(month=today.month+1, day=1)

    #     if start_of_next_month.month == 12:
    #         end_of_next_month   = start_of_next_month.replace(year=start_of_next_month.year+1, month=1, day=1) - timedelta(days=1)
    #     else:
    #         end_of_next_month   =  start_of_next_month.replace(month=start_of_next_month.month+1, day=1) - timedelta(days=1)

    #     for record in self:
    #         if start_of_next_month  <= record.created_datetime.date() <= end_of_next_month:
    #             record.is_next_month = record.created_datetime
    #         else:
    #             record.is_next_month = False


    @api.depends('amount')
    def _compute_amount_str(self):
        for record in self:
            record.amount_str = "{:.2f}".format(record.amount)


    @api.depends('created_datetime')
    def _compute_month_year(self):
        for record in self:
            if record.created_datetime:
                date_obj = fields.Date.from_string(record.created_datetime)
                record.month_year = date_obj.strftime('%B %Y')
            else:
                record.month_year = ''
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        res = super(Balance, self).name_search(name, args, operator, limit)
        if not args:
            args = []

        # Search for amount_str
        domain = [('amount_str', operator, name)]
        matches = self.search(domain + args, limit=limit)
        res = matches.name_get()
        return res

    @api.depends('description')
    def _compute_tooltip_field(self):
        for index, record in enumerate(self, start=1):
            record.tooltip_field = str(index)


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
            rec.creator_display = '<img t-att-a="42" src="%s" style="width: 19px; height: 19px;  border-radius:50%%; vertical-align: middle; margin-right: 5px;"/> %s' % (image_url,rec.create_uid.name)

   
   
   
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
            random_minutes = random.randint(1, 59)
            random_seconds = random.randint(1, 59)
            current_time = fields.Datetime.from_string(fields.Datetime.now() +  timedelta(minutes=random_minutes,seconds=random_seconds)).time() 
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
                    'invoice_id': invoice.id,
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



    @api.model
    def update_invoice_number(self):
        for balance_record in self.search([]):  # Loop through all balance records
            get_fac = self.env['account.move'].search([('name', '=', balance_record.reference)], limit=1)
            if get_fac:
                balance_record.invoice_order_number = get_fac.x_studio_n_de_commande_


    def action_open_attach_statement_line_wizard(self):
        return {
            'name': 'Attach Statement Line',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.attach.statement.line',
            'view_mode': 'form',
            'view_id': self.env.ref('balance.view_wizard_attach_statement_line_form').id,
            'target': 'new',
            'context': {'default_balance_id': self.id}
        }
    

    # def button_attach(self):
    #     for line in self.statement_line_ids:
    #         line.balance_id = self.balance_id
    #     return {'type': 'ir.actions.act_window_close'}





    def action_open_wizard(self):
        context = {
            'default_new_datetime': fields.Datetime.now(),
            'active_ids': self.ids
        }
        return {
            'name': 'Change Datetime',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'balance.change.due.date.wizard',
            'target': 'new',
            'context': context,
        }


    @api.onchange('reference')
    def lock_for_editing(self):
        _logger.info("woooooow woooooooooooow woooooooooooooooooooooooooooooooow")