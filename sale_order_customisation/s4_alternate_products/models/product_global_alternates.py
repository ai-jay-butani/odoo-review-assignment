from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class ProductGlobalAlternates(models.Model):
    _name = 'product.global.alternates'
    _description = 'Global Product Alternates'
    _rec_name = 'primary_product_id'

    primary_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Primary Product",
        required=True,
    )
    alternate_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Alternate Product",
        required=True,
    )
    customer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        required=True
    )
    alternate_type_id = fields.Many2one(
        comodel_name="product.alternate.types",
        string="Alternate Type",
        required=True,
    )
    priority = fields.Integer(
        string="Priority",
        required=True,
    )
    active = fields.Boolean(default=True)

    def _check_priority(self, vals):
        """
            Used to check priority added is be greater than zero or not.
        """
        if 'priority' in vals and vals.get('priority') <= 0:
            raise ValidationError(_('Priority should be greater than zero!'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._check_priority(vals)
        return super(ProductGlobalAlternates, self).create(vals_list)

    def write(self, vals):
        self._check_priority(vals)
        return super(ProductGlobalAlternates, self).write(vals)

