# -*- coding: utf-8 -*-
{
    'name': 'Catalog Customisation',
    'version': '18.0.1.0.0',
    'author': 'Jay Butani',
    'sequence': 5,
    'summary': 'Catalog Customisation Module',
    'description': "Catalog Customisation",
    'website': 'https://www.aktivsoftware.com',
    'data':[
        "views/res_config_settings_views.xml",
    ],
    "assets":{
        "web.assets_backend": [
                "ak_catalog_customisation/static/src/scss/price_filter.scss",
                "ak_catalog_customisation/static/src/search/price_filter.js",
                "ak_catalog_customisation/static/src/search/price_filter_kanban.js",
                "ak_catalog_customisation/static/src/search/price_filter.xml",
        ],
    },
    'depends': ['sale_management'],
    'application': True,
    'license': 'LGPL-3',
}