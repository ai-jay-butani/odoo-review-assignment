from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_id = fields.Many2one(
        comodel_name="sale.order",
        string="Sales Order",
        readonly=True,
        store=True
    )
    customer_id = fields.Many2one(
        comodel_name="res.partner",
        related="sale_id.partner_id",
        string="Customer",
        readonly=False,
        store=True
    )

