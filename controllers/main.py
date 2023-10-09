from odoo import http

class Main(http.Controller):

    @http.route('/balance/download_sql', type='http', auth='user')
    def saveas(self, record_ids, **kwargs):
        Record = http.request.env['balance']
        records = Record.browse(map(int, record_ids.split(',')))

        # Get all fields of the 'balance' model
        all_fields = Record.fields_get()

        # Fields to exclude from the SQL statements
        excluded_fields = ['id']  # Add other fields if needed

        # Filter out unwanted fields
        included_fields = [f for f in all_fields if f not in excluded_fields]

        # Generate SQL statements
        sql_statements = []
        for rec in records:
            columns = ", ".join('"%s"' % field for field in included_fields)
            vals = ", ".join(repr(getattr(rec, field)) for field in included_fields)
            stmt = "INSERT INTO balance_table_name (%s) VALUES (%s);" % (columns, vals)
            sql_statements.append(stmt)

        # Check if we have any SQL statements
        if not sql_statements:
            return "No valid records found."

        content = "\n".join(sql_statements)
        return http.request.make_response(content, headers=[
            ('Content-Type', 'application/sql'),
            ('Content-Disposition', 'attachment; filename="balance_records.sql"')
        ])