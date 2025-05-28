# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


class ProductPriceController(http.Controller):

    @http.route('/product_catalog/max_price', type='json', auth='user', website=True)
    def get_product_max_price(self):
        """
        Returns the maximum product price and configured minimum price for price filtering.
        
        This endpoint is used by the product catalog to get the price range for the price
        filter component.
        
        :return: Dictionary containing:
            - max_price (int): The highest list price among all products
            - min_price (int): The minimum price configured in company settings
        :rtype: dict
        """
        max_price = request.env['product.product'].search([], order="list_price desc", limit=1).list_price
        min_price = request.env.user.company_id.price_filter_min_price
        return {'max_price': int(max_price), 'min_price': min_price}
