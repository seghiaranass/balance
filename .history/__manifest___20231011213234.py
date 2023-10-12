{
    'name': 'Balance',
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/wizard_attach_statement_line_view.xml',
        'views/balance_views.xml',
        'views/balance_tags_views.xml',
        'views/balance_actions.xml',
        'views/balance_tags_actions.xml',
        'views/balance_menus.xml',
        'views/facture_clients_view_inherits.xml',
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
            # 'balance/static/src/js/tree_button.js',
            # 'balance/static/src/xml/tree_button.xml',
            
        ],
            'web.assets_qweb': [
                # 'balance/static/src/xml/tree_button.xml',
            ],

    },
    'depends': ['base','web','account','mail'],  # This is the key addition you should make
}
