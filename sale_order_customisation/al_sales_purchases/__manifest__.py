# -*- coding: utf-8 -*-
{
    'name': 'Service Product Purchase Order',
    'version': '18.0.1.0.0',
    'author': 'Jay Butani',
    'sequence': 5,
    'summary': 'Service Product Purchase Order Module',
    'description': "Create purchase order of service type product when sale order confirm",
    'website': 'https://www.aktivsoftware.com',
    'data': [
        'views/product_template_views.xml',
        'views/product_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'al_sales_purchases/static/src/js/image_copy.js',
            'al_sales_purchases/static/src/xml/image_field.xml',
            'al_sales_purchases/static/src/scss/image_copy.scss',
        ]
    },
    'depends': ['sale_management', 'purchase'],
    'application': True,
    'license': 'LGPL-3',
}
