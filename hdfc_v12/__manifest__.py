{
    'name' : 'HDFC Payment Gateway',
    'version' : '1.1',
    'summary': '',
    'sequence': -1,
    'description': """
    """,
    'category': '',
    'website': 'https://agaramsoft.com/',
    'images' : [],
    'depends' : ['base','website_sale', 'payment'],
    'data': [
        'views/payment_acquirer_view.xml',
        'views/template.xml',
        'views/hdfc_payment_template.xml',
        'views/assets.xml',
        'data/hdfc.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
