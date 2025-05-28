from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    bom_line_id = fields.Many2one(
        comodel_name="mrp.bom.line",
        string="BOM Line",
    )
    customer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer"
    )
    alternate_product = fields.Boolean(
        string="Alternate Product",
    )
