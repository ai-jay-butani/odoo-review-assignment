# -*- coding: utf-8 -*-

from odoo import models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_dest_id, name, origin, company_id, values, bom):
        """
        Prepares manufacturing order (MO) values based on provided parameters and additional data.

        This method overrides the parent class method to include custom logic for preparing MO values.
        It checks for a group associated with the given values and sets the origin of the MO accordingly
        when there is a parent manufacturing order.

        Returns:
            Prepared dictionary of values for creating a manufacturing order. The returned dictionary may
            include additional fields depending on the customizations applied by the method's implementation.
        """
        group = values.get('group_id')
        if group and group.mrp_production_ids:
            parent_mo = group.mrp_production_ids
            origin = parent_mo._get_origin()
        return super()._prepare_mo_vals(product_id, product_qty, product_uom, location_dest_id, name, origin, company_id, values, bom)
