{
    'name': 'Balance',
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/balance_views.xml',
        'views/balance_menus.xml',
    ],
    'images': ['static/description/icon.png'],
    'assets': {
        'web.assets_backend': [
            'balance/static/src/js/custom_buttons.js',
            'balance/static/src/css/balance.css'
            
        ],
    },
    'depends': ['base','web','account'],  # This is the key addition you should make
}
