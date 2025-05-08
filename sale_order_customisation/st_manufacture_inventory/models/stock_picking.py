# -*- coding: utf-8 -*-

from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    origin = fields.Char(string='Source Document', compute='_compute_origin')

    def _compute_origin(self):
        """
        Computes the origin of a picking based on its associated group and
        manufacturing production IDs.

        This method iterates through pickings and updates the origin of each
        picking if it is associated with a group that has manufacturing
        production IDs. The origin is set to the origin of the related
        manufacturing production.

        Raises
        ------
        None
        """
        for picking in self:
            if picking.group_id.mrp_production_ids:
                picking.origin = picking.group_id.mrp_production_ids.origin