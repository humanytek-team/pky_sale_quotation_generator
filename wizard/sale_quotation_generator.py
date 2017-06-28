# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Manuel Márquez <manuel@humanytek.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import api, fields, models


class SaleQuotationGenerator(models.TransientModel):
    """
    This wizard will generate quotations based on parameters asociated to the
    operations of pack system.
    """

    _name = "sale.quotation.generator"
    _description = """This wizard will generate quotations based on parameters
    asociated to the operations of pack system."""

    raw_material_product_id = fields.Many2one(
        'product.product', 'Material', required=True)
    raw_material_product_standard_price = fields.Float(
        related='raw_material_product_id.standard_price',
        readonly=True,
        required=True
    )
    raw_material_product_cost_currency_id = fields.Many2one(
        related='raw_material_product_id.cost_currency_id',
        readonly=True
    )
    raw_material_product_seller_ids = fields.One2many(
        related='raw_material_product_id.seller_ids'
    )
    raw_material_product_attr_value_ids = fields.Many2many(
        related='raw_material_product_id.attribute_value_ids'
    )
    raw_material_product_length_mm = fields.Float(
        compute='_compute_length_mm'
    )
    raw_material_product_length_cm = fields.Float(
        compute='_compute_length_cm'
    )
    raw_material_product_thickness_cm = fields.Float(
        compute='_compute_thickness_cm'
    )
    new_product_generated = fields.Char('New product generated', required=True)
    total_thousands_new_product = fields.Float(
        'Thousands', compute='_compute_total_thousands')
    cut_based_on_bottle = fields.Float('Cut (mm)', required=True)
    current_rate_usd = fields.Float(compute='_compute_current_rate_usd')
    ink_product_id = fields.Many2one('product.product', 'Ink')
    ink_product_standard_price = fields.Float(
        related='ink_product_id.standard_price'
    )
    ink_product_cost_currency_id = fields.Many2one(
        related='ink_product_id.cost_currency_id'
    )
    ink_product_quantity = fields.Integer('Number of inks')
    total_ink_cost = fields.Float(
        'Total ink cost', compute='_compute_total_ink_cost')
    glue_other_expenses = fields.Float('Glue and Other Expenses')
    flat_width_mm = fields.Float('Flat Width (mm)', required=True)
    overlapping = fields.Float('Overlapping', required=True)
    coil_width_mm = fields.Float(
        'Coil Width (mm)', compute='_compute_coil_width_mm')
    coil_width_cm = fields.Float(
        'Coil Width (cm)', compute='_compute_coil_width_cm')
    max_percentage_raw_material_on_sale_price = fields.Float(
        'Max percentage')
    min_percentage_raw_material_on_sale_price = fields.Float(
        'Min percentage')
    coil_weight_kg = fields.Float(
        'Coil Weight (kg)', compute='_compute_coil_weight_kg')
    total_cost_coil = fields.Float(
        'Total Cost of the Coil', compute='_compute_total_cost_coil'
    )
    cost_per_thousand = fields.Float(
        'Cost per thousand', compute='_compute_cost_per_thousand'
    )
    max_sale_price_per_thousand_without_printing = fields.Float(
        'Maximum Sale Price per Thousand Without Printing',
        compute='_compute_sale_price_per_thousand_without_printing'
    )
    min_sale_price_per_thousand_without_printing = fields.Float(
        'Minimum Sale Price per Thousand Without Printing',
        compute='_compute_sale_price_per_thousand_without_printing'
    )
    max_mxn_sale_price_per_thousand_with_printing = fields.Float(
        'Maximum Sale Price (MXN) per Thousand With Printing',
        compute='_compute_mxn_sale_price_per_thousand_with_printing'
    )
    min_mxn_sale_price_per_thousand_with_printing = fields.Float(
        'Minimum Sale Price (MXN) per Thousand With Printing',
        compute='_compute_mxn_sale_price_per_thousand_with_printing'
    )
    max_usd_sale_price_per_thousand_with_printing = fields.Float(
        'Maximum Sale Price (USD) per Thousand With Printing',
        compute='_compute_usd_sale_price_per_thousand_with_printing'
    )
    min_usd_sale_price_per_thousand_with_printing = fields.Float(
        'Minimum Sale Price (USD) per Thousand With Printing',
        compute='_compute_usd_sale_price_per_thousand_with_printing'
    )
    required_initial_volume = fields.Integer('Required initial volume')
    business_value = fields.Float(
        'Business Value', compute='_compute_business_value')
    price_range_per_thousand_ids = fields.One2many(
        comodel_name='price.range.per.thousand',
        inverse_name='sale_quotation_generator_id',
        string='Range of prices per thousand',
        required=True
    )
    customer_id = fields.Many2one(
        'res.partner',
        'Customer',
        required=True,
        domain=[('customer', '=', True)])

    @api.depends('raw_material_product_id')
    def _compute_length_mm(self):
        """Compute value of field raw_material_product_length_mm, the value is
        the result of process of the attribute length of the product converting
        it from meters to millimeters."""

        for rec in self:
            rec.raw_material_product_length_mm = False

            if rec.raw_material_product_id:
                attr_length_object = self.env.ref(
                    'pky_sale_quotation_generator.product_attribute_length')
                product_has_attr_length = [
                    attr.name for attr in
                    rec.raw_material_product_id.attribute_value_ids if
                    attr.attribute_id == attr_length_object]

                if product_has_attr_length:
                    rec.raw_material_product_length_mm = \
                        float(product_has_attr_length[0]) * 1000

    @api.depends('raw_material_product_length_mm')
    def _compute_length_cm(self):
        """Compute value of field raw_material_product_length_cm, the value is
        the result of process the value of field raw_material_product_length_mm
        converting it from millimeters to cm."""

        for rec in self:
            rec.raw_material_product_length_cm = False
            if rec.raw_material_product_length_mm:
                rec.raw_material_product_length_cm = \
                    rec.raw_material_product_length_mm * 0.1

    @api.depends('raw_material_product_id')
    def _compute_thickness_cm(self):
        """Compute value of field raw_material_product_thickness_cm, the value is
        the result of process of the attribute thickness of the product
        converting it from microns to centimeters."""

        for rec in self:
            rec.raw_material_product_thickness_cm = False

            if rec.raw_material_product_id:
                attr_thickness_object = self.env.ref(
                    'pky_sale_quotation_generator.product_attribute_thickness')
                product_has_attr_thickness = [
                    attr.name for attr in
                    rec.raw_material_product_id.attribute_value_ids
                    if attr.attribute_id == attr_thickness_object]
                if product_has_attr_thickness:
                    rec.raw_material_product_thickness_cm = \
                        float(product_has_attr_thickness[0]) / 10000

    @api.depends('raw_material_product_length_mm', 'cut_based_on_bottle')
    def _compute_total_thousands(self):
        """Compute value of field total_thousands_new_product, the value will be
        the total thousands of the new product in the quotation to generate."""

        for rec in self:
            rec.total_thousands_new_product = False

            if rec.raw_material_product_length_mm and rec.cut_based_on_bottle:
                rec.total_thousands_new_product = (
                    rec.raw_material_product_length_mm / (
                        rec.cut_based_on_bottle * 1000
                    )) * 0.9

    @api.depends('raw_material_product_id')
    def _compute_current_rate_usd(self):
        """Compute value of field current_rate_usd, return current rate of
        currency USD."""

        for record in self:
            record.current_rate_usd = False
            usd_currency = self.env.ref('base.USD')
            mxn_currency = self.env.ref('base.MXN')
            if usd_currency and mxn_currency:
                record.current_rate_usd = usd_currency.compute(1, mxn_currency)

    @api.depends(
        'ink_product_standard_price',
        'ink_product_quantity',
        'current_rate_usd',
        'ink_product_cost_currency_id')
    def _compute_total_ink_cost(self):
        """Compute value of field total_ink_cost"""

        for record in self:
            record.total_ink_cost = False
            if (record.ink_product_standard_price and
                    record.ink_product_quantity and
                    record.current_rate_usd):

                if record.ink_product_cost_currency_id:
                    usd_currency = self.env.ref('base.USD')
                    mxn_currency = self.env.ref('base.MXN')
                    if record.ink_product_cost_currency_id == usd_currency:
                        record.total_ink_cost = (
                            record.ink_product_standard_price *
                            record.current_rate_usd) \
                            * record.ink_product_quantity
                    elif record.ink_product_cost_currency_id == mxn_currency:
                        record.total_ink_cost = \
                            record.ink_product_standard_price * \
                            record.ink_product_quantity
                else:
                    record.total_ink_cost = \
                        record.ink_product_standard_price * \
                        record.ink_product_quantity

    @api.depends('flat_width_mm', 'overlapping')
    def _compute_coil_width_mm(self):
        """Compute the value of field coil_width_mm"""

        for record in self:
            record.coil_width_mm = False
            if record.flat_width_mm and record.overlapping:
                record.coil_width_mm = \
                    record.flat_width_mm * 2 + record.overlapping

    @api.depends('coil_width_mm')
    def _compute_coil_width_cm(self):
        """Compute the value of field coil_width_cm"""

        for record in self:
            record.coil_width_cm = False
            if record.coil_width_mm:
                record.coil_width_cm = record.coil_width_mm * 0.1

    @api.depends(
        'raw_material_product_id',
        'coil_width_cm',
        'raw_material_product_thickness_cm',
        'raw_material_product_length_cm')
    def _compute_coil_weight_kg(self):
        """Compute value of field coil_weight_kg."""

        for rec in self:
            rec.coil_weight_kg = False

            if rec.raw_material_product_id:
                attr_density = self.env.ref(
                    'pky_sale_quotation_generator.product_attribute_density')
                product_has_attr_density = [
                    attr.name for attr in
                    rec.raw_material_product_id.attribute_value_ids
                    if attr.attribute_id == attr_density]

                if product_has_attr_density:
                    if (rec.coil_width_cm and
                            rec.raw_material_product_thickness_cm and
                            rec.raw_material_product_length_cm):

                        rec.coil_weight_kg = \
                            (
                                float(product_has_attr_density[0]) *
                                rec.coil_width_cm *
                                rec.raw_material_product_thickness_cm *
                                rec.raw_material_product_length_cm
                            ) / 1000

    @api.depends('raw_material_product_standard_price', 'coil_weight_kg')
    def _compute_total_cost_coil(self):
        """Compute value of field total_cost_coil."""

        for rec in self:
            rec.total_cost_coil = False

            if rec.raw_material_product_standard_price and rec.coil_weight_kg:
                rec.total_cost_coil = \
                    rec.coil_weight_kg * \
                    rec.raw_material_product_standard_price

    @api.depends('total_cost_coil', 'total_thousands_new_product')
    def _compute_cost_per_thousand(self):
        """Compute value of field cost_per_thousand"""

        for rec in self:
            rec.cost_per_thousand = False

            if rec.total_cost_coil and rec.total_thousands_new_product:
                rec.cost_per_thousand = rec.total_cost_coil / \
                    rec.total_thousands_new_product

    @api.depends(
        'max_percentage_raw_material_on_sale_price',
        'min_percentage_raw_material_on_sale_price',
        'cost_per_thousand')
    def _compute_sale_price_per_thousand_without_printing(self):
        """Compute value of fields max_sale_price_per_thousand_without_printing
        and min_sale_price_per_thousand_without_printing."""

        for rec in self:
            rec.max_sale_price_per_thousand_without_printing = False
            rec.min_sale_price_per_thousand_without_printing = False

            if rec.max_percentage_raw_material_on_sale_price:
                rec.max_sale_price_per_thousand_without_printing = \
                    rec.cost_per_thousand / \
                    float('0.{0}'.format(
                        int(round(
                            rec.max_percentage_raw_material_on_sale_price
                            ))
                    ))

            if rec.min_percentage_raw_material_on_sale_price:
                rec.min_sale_price_per_thousand_without_printing = \
                    rec.cost_per_thousand / float('0.{0}'.format(
                        int(round(
                            rec.min_percentage_raw_material_on_sale_price
                            ))
                    ))

    @api.depends(
        'max_sale_price_per_thousand_without_printing',
        'min_sale_price_per_thousand_without_printing',
        'current_rate_usd',
        'total_ink_cost',
        'total_thousands_new_product',
        'glue_other_expenses')
    def _compute_mxn_sale_price_per_thousand_with_printing(self):
        """Compute value of fields max_mxn_sale_price_per_thousand_with_printing
        and min_mxn_sale_price_per_thousand_with_printing."""

        for rec in self:
            rec.max_mxn_sale_price_per_thousand_with_printing = False
            rec.min_mxn_sale_price_per_thousand_with_printing = False

            if (rec.max_sale_price_per_thousand_without_printing and
                    rec.current_rate_usd):

                    rec.max_mxn_sale_price_per_thousand_with_printing = \
                        rec.max_sale_price_per_thousand_without_printing * \
                        rec.current_rate_usd

                    if rec.total_thousands_new_product:

                        if rec.total_ink_cost:
                            rec. \
                                max_mxn_sale_price_per_thousand_with_printing \
                                += rec.total_ink_cost / \
                                rec.total_thousands_new_product

                        if rec.glue_other_expenses:
                            rec. \
                                max_mxn_sale_price_per_thousand_with_printing \
                                += rec.glue_other_expenses / \
                                rec.total_thousands_new_product

            if (rec.min_sale_price_per_thousand_without_printing and
                    rec.current_rate_usd):

                    rec.min_mxn_sale_price_per_thousand_with_printing = \
                        rec.min_sale_price_per_thousand_without_printing * \
                        rec.current_rate_usd

                    if rec.total_thousands_new_product:

                        if rec.total_ink_cost:
                            rec. \
                                min_mxn_sale_price_per_thousand_with_printing \
                                += rec.total_ink_cost / \
                                rec.total_thousands_new_product

                        if rec.glue_other_expenses:
                            rec. \
                                min_mxn_sale_price_per_thousand_with_printing \
                                += rec.glue_other_expenses / \
                                rec.total_thousands_new_product

    @api.depends(
        'max_mxn_sale_price_per_thousand_with_printing',
        'min_mxn_sale_price_per_thousand_with_printing',
        'current_rate_usd')
    def _compute_usd_sale_price_per_thousand_with_printing(self):
        """Compute value of fields max_usd_sale_price_per_thousand_with_printing
        and min_usd_sale_price_per_thousand_with_printing."""

        for rec in self:
            rec.max_usd_sale_price_per_thousand_with_printing = False
            rec.min_usd_sale_price_per_thousand_with_printing = False

            if (rec.max_mxn_sale_price_per_thousand_with_printing and
                    rec.current_rate_usd):

                rec.max_usd_sale_price_per_thousand_with_printing = \
                    rec.max_mxn_sale_price_per_thousand_with_printing / \
                    rec.current_rate_usd

            if (rec.min_mxn_sale_price_per_thousand_with_printing and
                    rec.current_rate_usd):

                rec.min_usd_sale_price_per_thousand_with_printing = \
                    rec.min_mxn_sale_price_per_thousand_with_printing / \
                    rec.current_rate_usd

    @api.depends(
        'required_initial_volume',
        'min_mxn_sale_price_per_thousand_with_printing')
    def _compute_business_value(self):
        """Compute value of field business_value."""

        for rec in self:
            rec.business_value = False

            if (rec.required_initial_volume and
                    rec.min_mxn_sale_price_per_thousand_with_printing):

                rec.business_value = rec.required_initial_volume * \
                    rec.min_mxn_sale_price_per_thousand_with_printing

    @api.one
    def generate_quotations(self):
        """Generates quotations of the data obtained from the form of the
        wizard"""

        SaleOrder = self.env['sale.order']
        sale_order_data = dict()
        Product = self.env['product.product']
        product_data = dict()
        product_data['name'] = self.new_product_generated

        product_uom_thousand = self.env.ref(
            'pky_sale_quotation_generator.product_uom_thousand')
        if product_uom_thousand:
            product_data['uom_id'] = product_uom_thousand.id

        product_data['sale_ok'] = True
        product_data['purchase_ok'] = False

        route_warehouse_manufacture = self.env.ref(
            'mrp.route_warehouse0_manufacture')
        route_warehouse_mto = self.env.ref(
            'stock.route_warehouse0_mto')

        if route_warehouse_manufacture or route_warehouse_mto:
            product_data['route_ids'] = []

        if route_warehouse_manufacture:
            product_data['route_ids'].append(
                (4, route_warehouse_manufacture.id)
            )

        if route_warehouse_mto:
            product_data['route_ids'].append(
                (4, route_warehouse_mto.id)
            )

        product = Product.create(product_data)

        sale_order_data['partner_id'] = self.customer_id.id
        if self.price_range_per_thousand_ids:
            sale_order_data['order_line'] = list()
            for prices_range in self.price_range_per_thousand_ids:
                sale_order_data['order_line'].append(
                    (0, 0, {
                        'product_id': product.id,
                        'price_unit': prices_range.sale_price_per_thousand_usd
                    })
                )

        sale_order = SaleOrder.create(sale_order_data)
        if sale_order:
            view = self.env.ref('sale.view_order_form')

            sale_order_form_view = {
                'name': 'Enter transfer details',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'sale.order',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'current',
                'res_id': sale_order.id,
                'context': self.env.context,
            }

            return sale_order_form_view
