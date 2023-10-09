{
    'name': 'Balance',
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/balance_views.xml',
        'views/balance_tags_views.xml',
        'views/balance_actions.xml',
        'views/balance_tags_actions.xml',
        'views/balance_menus.xml',
        # 'assets.xml',
    ],
    'images': ['static/description/icon.png'],
    'assets': {
        'web.assets_backend': [
            'balance/static/src/js/custom_buttons.js',
            'balance/static/src/css/balance.css',
            'balance/static/src/css/balance_style.scss'
            
        ],
    },
    'depends': ['base','web','account','mail'],  # This is the key addition you should make
}
