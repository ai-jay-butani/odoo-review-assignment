from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductAlternateTypes(models.Model):
    _name = 'product.alternate.types'
    _description = 'Product Alternates Types'

    name = fields.Char(string="Alternate type", readonly=True)
    description = fields.Text(string="Description", readonly=True)
    default = fields.Boolean(string="Default")
    active = fields.Boolean(default=True)

    @api.constrains("default")
    def _check_default(self):
        """
            Used to allow user to make only one alternative is selected a s a default.
        """
        for rec in self.filtered("default"):
            alternate_types = rec.search_count(
                [('default', '=', True), ('id', '!=', rec.id)])
            if alternate_types:
                raise ValidationError(
                    _(
                        "Only one Alternate Type may be set as ‘Default’. You must "
                        "first uncheck the ‘Default’ selection on the existing default "
                        "record before setting it here."
                    )
                )
