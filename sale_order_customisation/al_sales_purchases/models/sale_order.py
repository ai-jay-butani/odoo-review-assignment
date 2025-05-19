# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """
        Handles the confirmation of a sales order by generating purchase requests for products
        configured to generate RFQ (Request for Quotation) upon sales order confirmation.
        Validates that the product has suppliers defined, ensures each product uses the primary
        supplier, and either updates an existing draft purchase order or creates a new one.

        Raises:
            ValidationError: If any product configured to generate an RFQ has no associated supplier.

        Parameters:
            None

        Returns:
            Any: The return value of the parent class's action_confirm method.
        """
        vendor_maps_dict = {}
        for line in self.order_line.filtered(lambda l: l.product_id.type == 'service' and
                                                       l.product_id.generate_rfq_on_so_confirm):
            if not line.product_id.seller_ids:
                raise ValidationError(f"Product {line.product_id.name} is configured to "
                                      f"automatically generate an "
                                      "RFQ on sales order confirmation but no supplier is "
                                      "maintained on the product. Please maintain one before "
                                      "attempting to save or confirm this Sales Order again.")

            for vendor in line.product_id.seller_ids.filtered(lambda s: s.sequence == 1):
                vendor_maps_dict[vendor] = line

        for vendor, line in vendor_maps_dict.items():
            exist_order = self.env['purchase.order'].search([
                ('partner_id', '=', vendor.partner_id.id), ('state', '=', 'draft')], limit=1)
            order_line_vals = [(0, 0, {
                'product_id': line.product_id.id,
                'product_qty': line.product_uom_qty,
                'price_unit': vendor.price,
                'sale_line_id': line.id,
            })]
            if exist_order:
                exist_order.update({
                    'origin': exist_order.origin + ', ' + line.order_id.name if exist_order
                    else line.order_id.name,
                    'order_line': order_line_vals
                })
            else:
                self.env['purchase.order'].create({
                    'partner_id': vendor.partner_id.id,
                    'origin': line.order_id.name,
                    'order_line': order_line_vals,
                })
        return super().action_confirm()
