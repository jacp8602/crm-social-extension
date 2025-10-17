{
    'name': 'CRM Social Extension',
    'version': '17.0.1.0.0',
    'category': 'Customer Relationship Management',
    'summary': 'Add social networks to customer profiles',
    'description': """
        Extension for CRM module that allows registering social network accounts
        for customers and displaying them in a dedicated tab.
    """,
    'author': 'Javier Alejandro Cobas',
    'depends': [
        'crm',
        'website',
    ],
    'data': [
        'views/res_partner_views.xml',
        # 'views/website_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'crm_social_extension/static/src/scss/crm_social.scss',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}