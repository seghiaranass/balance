from odoo import http

class Main(http.Controller):

    @http.route('/balance/download_sql', type='http', auth='user')
    def saveas(self, record_ids, **kwargs):
        Record = http.request.env['balance']
        records = Record.browse(map(int, record_ids.split(',')))

        # Generate SQL statements
        sql_statements = [
            "INSERT INTO balance_table (id, name, amount, balance, created_datetime, balance_correction) VALUES (%d, '%s', %f, %f, '%s', %s);" % (
                rec.id, rec.name, rec.amount, rec.balance, rec.created_datetime, rec.balance_correction)
            for rec in records
        ]

        # Check if we have any SQL statements
        if not sql_statements:
            return "No valid records found."

        content = "\n".join(sql_statements)
        return http.request.make_response(content, headers=[
            ('Content-Type', 'application/sql'),
            ('Content-Disposition', 'attachment; filename="balance_records.sql"')
        ])
