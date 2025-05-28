from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MrpProductionComponentAlternates(models.Model):
    _name = "mrp.production.component.alternates"
    _description = "Manufacturing Order Component Alternates"
    _order = "alternate_priority"

    move_id = fields.Many2one(
        comodel_name="stock.move",
        string="Move",
        required=True,
    )
    bom_line_id = fields.Many2one(
        comodel_name="mrp.bom.line",
        string="BOM line",
        related="move_id.bom_line_id",
        readonly=False,
        store=True
    )
    alternate_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Alternate Product",
        required=True,
    )
    alternate_type_id = fields.Many2one(
        comodel_name="product.alternate.types",
        string="Alternate Type",
        required=True,
    )
    alternate_priority = fields.Integer(
        string="Alternate Priority",
        required=True
    )
    select_alternate = fields.Boolean(
        string="Select Alternate"
    )

    @api.constrains('select_alternate')
    def _check_select_alternate(self):
        """
            Used to check if user has selected only one alternative or not.
        """
        if (self.select_alternate and
                self.move_id.mrp_production_components_alternates_ids.filtered(
                lambda l: l.id != self.id and l.select_alternate)):
            raise ValidationError(_('You can select only one Alternate at a time!'))
