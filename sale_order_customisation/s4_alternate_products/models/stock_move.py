from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    alternate_product = fields.Boolean(
        string="Alternate Product"
    )
    original_primary_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Primary Product",
    )
    show_available_alternates = fields.Boolean(
        compute='_compute_show_available_alternates',
        store=True,
        readonly=False,
        string="Show Available Alternates?"
    )
    mrp_production_components_alternates_ids = fields.One2many(
        comodel_name='mrp.production.component.alternates',
        inverse_name='move_id',
        string="Manufacturing Order Component Alternates"
    )
    show_use_alternate = fields.Boolean(
        compute="_compute_show_use_alternate",
        store=True
    )

    @api.depends(
        'mrp_production_components_alternates_ids',
        'mrp_production_components_alternates_ids.select_alternate'
    )
    def _compute_show_use_alternate(self):
        """
            Used to show/hide Use Alternative Button.
        """
        for rec in self:
            rec.show_use_alternate = any(
                rec.mrp_production_components_alternates_ids.mapped('select_alternate'))

    def _get_global_product_alternates(self, product_id, customer_id):
        """
            Used to get a global product alternates.
        """
        return self.env['product.global.alternates'].search(
            [
                ('primary_product_id', '=', product_id),
                ('customer_id', '=', customer_id)
            ]
        )

    @api.depends(
        'product_id',
        'bom_line_id',
        'raw_material_production_id',
        'raw_material_production_id.state',
        'raw_material_production_id.customer_id',
        'alternate_product'
    )
    def _compute_show_available_alternates(self):
        """
            Used to show/hide Available Alternates Button.
        """
        for move in self:
            move.show_available_alternates = False
            production_id = move.raw_material_production_id
            bom_line_id = move.bom_line_id
            global_alternates = False
            if move.product_id and production_id and production_id.customer_id:
                global_alternates = self._get_global_product_alternates(
                    move.product_id.id, production_id.customer_id.id)
            if (production_id and production_id.state not in ('done', 'cancel') and
                    ((bom_line_id and bom_line_id.mrp_bom_line_alternates_ids) or
                     global_alternates or move.alternate_product)):
                move.show_available_alternates = True

    def create_component_alternate_recs(self, alternate_recs):
        """
            Used to create a Manufacturing Order Component Alternates.
        """
        return self.env['mrp.production.component.alternates'].create([{
            'move_id': self.id,
            'alternate_product_id': alternate.alternate_product_id.id,
            'alternate_type_id': alternate.alternate_type_id.id,
            'alternate_priority': self._context.get('from_bom_line') and
                                  alternate.alternate_priority or alternate.priority,
        } for alternate in alternate_recs])

    def available_alternates(self):
        """
            Manage available alternates pop-up.
        """
        self.mrp_production_components_alternates_ids.unlink()
        production_id = self.raw_material_production_id
        components_alternates_recs = self.mrp_production_components_alternates_ids
        bom_line_alternates = (self.bom_line_id and
                               self.bom_line_id.mrp_bom_line_alternates_ids or [])
        global_alternates = self._get_global_product_alternates(
            self.product_id.id, production_id.customer_id.id)
        if bom_line_alternates:
            components_alternates_recs += self.with_context(
                {'from_bom_line': True}).create_component_alternate_recs(
                bom_line_alternates)
        if global_alternates:
            components_alternates_recs += self.with_context(
                {'from_global_alternate': True}).create_component_alternate_recs(
                global_alternates)

        for rec in self.mrp_production_components_alternates_ids:
            filter_same_alternates = (
                self.env['mrp.production.component.alternates'].search(
                [
                    ('alternate_product_id', '=', rec.alternate_product_id.id),
                    ('alternate_type_id', '=', rec.alternate_type_id.id),
                    ('move_id', '=', self.id),
                    ('id', '!=', rec.id)
                ]
            ))
            if filter_same_alternates:
                rec.unlink()
        return {
            'name': 'Select Alternate Products for Component',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.move',
            'view_id': self.env.ref('s4_alternate_products.stock_move_form_view').id,
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id,
        }

    def btn_reset_primary(self):
        """
            Manage reset primary button.
        """
        if self.original_primary_product_id:
            production_id = self.raw_material_production_id
            production_id.do_unreserve()
            self.product_id = self.original_primary_product_id.id
            self.move_line_ids.product_id = self.original_primary_product_id.id
            production_id.action_assign()
            self.alternate_product = False

    def use_alternate(self):
        """
            Manage Use Alternate button.
        """
        if not self.original_primary_product_id:
            self.original_primary_product_id = self.product_id.id
        production_id = self.raw_material_production_id
        production_id.do_unreserve()
        components_alternates_ids = self.mrp_production_components_alternates_ids
        alternate_product_id = components_alternates_ids.filtered(
            lambda l: l.select_alternate)[0].alternate_product_id.id or False
        self.product_id = alternate_product_id
        self.move_line_ids.product_id = alternate_product_id
        production_id.action_assign()
        self.alternate_product = True
