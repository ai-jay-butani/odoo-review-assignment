# -*- coding: utf-8 -*-

from odoo import models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def _get_origin(self):
        """
        Retrieves the origin for the current instance.

        This method retrieves the origin by first calling the
        superclass's `_get_origin` method, then returning the
        current instance's `origin` attribute if it is set;
        otherwise, it returns the value retrieved from the
        superclass.

        Returns
        -------
        Any
            The origin associated with the current instance. If
            the `origin` attribute of the instance is set, that
            value is returned. Otherwise, the origin from the
            superclass method is returned.
        """
        origin = super()._get_origin()
        return self.origin or origin

    def _get_children(self):
        """
        Retrieves the child manufacturing production records associated with the current record.

        This method fetches all related manufacturing production records by traversing through
        procurement moves, their child moves, and associated productions. It ensures that
        the manufacturing production records do not include the current record.

        Returns:
            RecordSet: A set of related mrp.production records excluding the current record.
        """
        self.ensure_one()
        procurement_moves = self.procurement_group_id.stock_move_ids
        child_moves = procurement_moves.move_orig_ids
        return (procurement_moves | child_moves).created_production_id.procurement_group_id.mrp_production_ids - self

    def _get_sources(self):
        """
        Retrieves source manufacturing production records related to the current
        record. The function analyzes stock movement and procurement data to
        identify relevant production records to process.

        Returns
        -------
        RecordSet
            The manufacturing production records linked to the current record,
            excluding the current record itself.
        """
        self.ensure_one()
        dest_moves = self.procurement_group_id.mrp_production_ids.move_dest_ids
        parent_moves = self.procurement_group_id.stock_move_ids.move_dest_ids
        return (dest_moves | parent_moves).group_id.mrp_production_ids - self

    def write(self, vals):
        """
        Updates the current record with provided values and ensures any necessary updates
        to related child record origins are performed when the origin is changed. Calls
        the parent write method for completing the update operation.

        Parameters:
        vals: dict
            Dictionary of values to update. If the key 'origin' exists, related child
            records' origins are also updated through `_update_all_child_origins`.

        Returns:
        bool
            The return value from the parent `write` method, indicating the success or
            failure of the update operation.
        """
        origin_updated = vals.get('origin')
        if origin_updated:
                self._update_all_child_origins(vals['origin'])
        return super().write(vals)

    def _update_all_child_origins(self, new_origin):
        """
        Updates the origin attribute of all child objects recursively.

        This method iterates through all child objects retrieved from the _get_children
        method of the current instance. For each child, if the origin attribute does not
        match the specified new origin, it updates the origin to the new value. The method
        is then called recursively on the modified child objects to ensure all descendants
        have the updated origin.

        Arguments:
            new_origin: The new origin value to be applied to all child objects.

        Arguments Types:
            new_origin: Any
        """
        for child_mo in self._get_children():
            if child_mo.origin != new_origin:
                child_mo.origin = new_origin
                child_mo._update_all_child_origins(new_origin)
