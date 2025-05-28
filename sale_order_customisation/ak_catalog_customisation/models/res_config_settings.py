# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    price_filter_min_price = fields.Integer(
        related="company_id.price_filter_min_price", store=True,
        readonly=False
    )

    @api.constrains('price_filter_min_price')
    def _check_price_filter_min_price(self):
        """
        Validates the minimum price value for the price filter.
        
        Ensures that the minimum price is not set to a negative value,
        as prices cannot be negative in the system.
        
        :raises ValueError: If the minimum price is set to a negative value
        """
        if self.price_filter_min_price < 0:
            raise ValidationError("The minimum price cannot be negative.")
