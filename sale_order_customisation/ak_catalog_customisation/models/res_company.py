# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    price_filter_min_price = fields.Integer(string="Set Minimum Price")
