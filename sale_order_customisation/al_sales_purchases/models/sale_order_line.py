# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def write(self, vals):
        """
        Updates records and adjusts related purchase order line quantities.

        The method extends the `write` function to enable updating of related
        purchase order lines' quantities based on changes to the `product_uom_qty`
        field of sale order lines. If the `product_uom_qty` field is modified in
        the provided values, the method searches for associated purchase order
        lines that are still in the draft state and updates their `product_qty`
        values accordingly to match the updated `product_uom_qty`.

        Parameters:
            vals (dict): A dictionary of field values to update. If 'product_uom_qty'
            is included, related purchase order lines in draft state will have their
            `product_qty` updated to match the new value.

        Returns:
            bool: Returns the result of the superclass' `write` method execution.
        """
        res = super().write(vals)
        if 'product_uom_qty' in vals:
            for line in self:
                po_line = self.env['purchase.order.line'].search([
                    ('sale_line_id', '=', line.id),
                    ('order_id.state', '=', 'draft')
                ])
                po_line.product_qty = line.product_uom_qty
        return res
