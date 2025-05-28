# -*- coding: utf-8 -*-
{
    "name": "Alternate Products",
    "summary": """
            Alternate Products
       """,
    "description": """
        User Story 1,
    """,
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    "category": "Manufacturing",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ['mrp', 'sale_management', 'purchase'],
    "data": [
        'security/ir.model.access.csv',
        'data/product_alternate_types_data.xml',
        'views/product_global_alternates_views.xml',
        'views/product_alternate_types_views.xml',
        'views/mrp_bom_views.xml',
        'views/mrp_bom_line_views.xml',
        'views/mrp_production_views.xml',
        'views/stock_move_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
     "assets": {
        "web.assets_backend": [
            "s4_alternate_products/static/src/scss/alternate_btn.scss",
        ],
    },
}

