{
    'name' : 'HDFC Payment Gateway',
    'version' : '14.0.1.0.0',
    'summary': 'It helps to Integrate your ecommerce with HDFC Payment Gateway',
    'sequence': -1,
    'description': """
    """,
    'category': 'Payment Gateway',
    'website': 'https://agaramsoft.com/',
    'images' : 'static/description/icon.png',
    'live_test_url':'',
    'license': 'AGPL-3',
    'price': 1.00,
    'currency': 'USD',
    'depends' : ['base','website_sale', 'payment'],
    'data': [
        'views/payment_acquirer_view.xml',
        'views/template.xml',
        'views/hdfc_payment_template.xml',
        # 'views/assets.xml',
        'data/hdfc.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
