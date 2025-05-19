# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    generate_rfq_on_so_confirm = fields.Boolean(string="Generate RFQ on Sales Order Confirmation")
