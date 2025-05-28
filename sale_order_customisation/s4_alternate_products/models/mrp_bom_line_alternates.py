from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class MrpBomLineAlternates(models.Model):
    _name = 'mrp.bom.line.alternates'
    _description = 'BOM Line Alternates'
    _rec_name = 'bom_line_id'

    bom_line_id = fields.Many2one(
        comodel_name="mrp.bom.line",
        string="BOM line",
        required=True,
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

    @api.constrains("alternate_product_id")
    def _check_alternate_product_id(self):
        """
            Used to check if alternative product is added twice or not.
        """
        for rec in self.filtered("alternate_product_id"):
            alternate_products = rec.search_count(
                [
                    ('alternate_product_id', '=', rec.alternate_product_id.id),
                    ('id', '!=', rec.id),
                    ('bom_line_id', '=', rec.bom_line_id.id)
                ]
            )
            if alternate_products:
                raise ValidationError(
                    _(
                        "You can't add same Product twice."
                    )
                )

    def _check_alternate_priority(self, vals):
        """
            Used to check if priority is greater than zero or not.
        """
        if 'alternate_priority' in vals and vals.get('alternate_priority') <= 0:
            raise ValidationError(_('Priority should be greater than zero!'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._check_alternate_priority(vals)
        return super(MrpBomLineAlternates, self).create(vals_list)

    def write(self, vals):
        self._check_alternate_priority(vals)
        return super(MrpBomLineAlternates, self).write(vals)