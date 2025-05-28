from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _prepare_mo_vals(
            self, product_id, product_qty, product_uom, location_dest_id, name, origin,
            company_id, values, bom):
        """
            Used to set customer in Manufacturing order.
        """
        res = super(StockRule, self)._prepare_mo_vals(
            product_id, product_qty, product_uom,
            location_dest_id, name, origin, company_id, values, bom)
        if values.get("move_dest_ids", []):
            res['sale_id'] = (
                values["move_dest_ids"].group_id.stock_move_ids.mapped(
                    'sale_line_id').filtered(
                    lambda l: l.product_id.id == product_id.id)[0].order_id.id
                if values.get("move_dest_ids") and
                   values["move_dest_ids"].group_id.stock_move_ids.mapped(
                       'sale_line_id').filtered(
                       lambda l: l.product_id.id == product_id.id)
                else False
            )
            if not res['sale_id'] and "move_dest_ids" in values:
                res["sale_id"] = values["move_dest_ids"].group_id.mrp_production_ids.mapped('sale_id')[0].id \
                    if (values.get("move_dest_ids") and
                        values["move_dest_ids"].group_id.mrp_production_ids and
                        values["move_dest_ids"].group_id.mrp_production_ids.mapped('sale_id')
                        ) else False
            if not res["sale_id"] and "procurement_group_id" in values:
                res["sale_id"] = values["procurement_group_id"].mrp_production_ids[0].move_dest_ids.group_id.sale_id.id if (
                        values["procurement_group_id"] and
                        values["procurement_group_id"].mrp_production_ids and
                        values["procurement_group_id"].mrp_production_ids[0].move_dest_ids
                ) else False
        return res
