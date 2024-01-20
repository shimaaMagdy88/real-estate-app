{
    'name': 'App One',
    'version': '1.0.0',
    'summary': 'App One Practising',
    'sequence': 4,
    'description': """app for testing and practising""",
    'depends': ['base', 'sale', 'mail', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/building_view.xml',
    ],
    'assets': {
        'web.assets_backend': ['app_one\static\src\css\property.css']
    },
    'application': True,
    'license': 'LGPL-3',
}
