from odoo import fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    mrp_bom_line_alternates_ids = fields.One2many(
        comodel_name='mrp.bom.line.alternates',
        inverse_name='bom_line_id',
        string="BOM Line Alternates"
    )

    def maintain_alternates(self):
        """
            Used to open maintain alternates pop-up.
        """
        return {
            'name': 'Maintain Alternate Products for Component',
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.bom.line',
            'view_id': self.env.ref('s4_alternate_products.mrp_bom_line_form_view').id,
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id,
        }
