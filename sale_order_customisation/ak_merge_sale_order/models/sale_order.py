# -*- coding: utf-8 -*-

from odoo import models, fields, Command
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    """
    Represents a sale order model, extending its functionality for merging products and orders.

    This class is designed to enhance the default sale order model by providing additional
    operations such as merging duplicate product lines in an order and consolidating multiple
    sale orders into a single order for the same customer and state.
    """
    _inherit = 'sale.order'

    def action_merge_product(self):
        """
        Merges products in the order line by combining quantities of duplicate product entries.

        The method iterates through the `order_line` attribute, identifies duplicate products by their
        `product_id`, and merges them by summing their `product_uom_qty`. Duplicate entries are subsequently
        removed after their quantities are summed into the original product entry.

        Returns
        -------
        None

        Raises
        ------
        Any exception raised during the `write` or `unlink` operations will propagate without handling.

        Parameters
        ----------
        self : object
            The instance of the class that holds the method, containing an attribute `order_line`
            with products to be processed. Assumes each product in `order_line` has attributes
            `product_id`, `write`, `unlink`, and `product_uom_qty`.
        """
        previous_product_dict = {}
        for product in self.order_line:
            if product.product_id not in previous_product_dict:
                previous_product_dict[product.product_id] = product
            else:
                previous_product_dict[product.product_id].write({
                    'product_uom_qty': previous_product_dict[product.product_id].product_uom_qty + product.product_uom_qty,
                })
                product.unlink()

    def action_merge_sale_order(self):
        """
        Merges sale orders for the same customer and state, consolidating their order lines.
        This method ensures that only orders with the same customer and state can be merged.
        If this condition is violated, an exception is raised.

        Raises:
            ValidationError: If the orders do not have the same customer or state.
        """
        partner_id = None
        state = None
        sale_order = None
        for order in self:
            if not partner_id or not state or not sale_order:
                partner_id = order.partner_id
                state = order.state
                sale_order = order
            elif order.partner_id != partner_id or order.state != state:
                raise ValidationError("Not same user or same state")
            else:
                sale_order.update(
                    {
                        'order_line': [(Command.link(line.id)) for line in order.order_line]
                    }
                )
                order.unlink()
        sale_order.action_merge_product()
