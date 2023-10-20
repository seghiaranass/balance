{
    'name': 'Balance',
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/wizard_attach_statement_line_view.xml',
        'views/wizard/view_balance_change_wizard_form.xml',
        'views/balance_views.xml',
        'views/balance_tags_views.xml',
        'views/balance_actions.xml',
        'views/balance_tags_actions.xml',
        'views/balance_menus.xml',
        'views/facture_clients_view_inherits.xml',
        'views/report_balance.xml',
        # 'views/edit_lock_template.xml',

        # 'views/automated_actions_data.xml',


        # 

        # 'views/tree_button.xml'
        # 'assets.xml',
    ],
    'images': ['static/description/icon.png'],
    'assets': {
        'web.assets_backend': [
            'balance/static/src/js/custom_buttons.js',
            'balance/static/src/js/odoo_js.js',
            'balance/static/src/css/balance.css',
            'balance/static/src/css/balance_style.scss',
            'balance/static/src/xml/balance_button.xml',
            'balance/static/src/js/balance_button.js',
            'balance/static/src/js/testjs.js',
            'balance/static/src/xml/add_pin.xml',
            # 'balance/static/src/xml/edit_lock_template.xml'
            'balance/static/src/js/edit_lock.js',
            # 'balance/static/src/js/notification.js',
            # 'balance/static/src/js/add_pin.xml',
            
        ],
            'web.assets_qweb': [
                'balance/static/src/xml/tree_button.xml',
                
            ],

    },
    'depends': ['base','web','account','mail','sale'],  # This is the key addition you should make
}
