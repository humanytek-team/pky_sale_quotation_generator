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


class Product(models.Model):
    _inherit = 'product.product'

    raw_material_product_attrs_valid = fields.Boolean(
        'Product has attributes valid ?',
        help='Field used by wizard sale order generator',
        compute='_compute_attrs_valid',
        search='_search_attrs_valid')

    @api.depends('attribute_value_ids')
    def _compute_attrs_valid(self):
        """Compute value of field raw_material_product_attrs_valid, this field
        indicates wheater the product used as raw material has attributes valid
        """

        for rec in self:
            rec.raw_material_product_attrs_valid = False

            if rec.attribute_value_ids:

                attrs_valid = list()
                attr_density = self.env.ref(
                    'pky_sale_quotation_generator.product_attribute_density')
                attr_length = self.env.ref(
                    'pky_sale_quotation_generator.product_attribute_length')
                attr_thickness = self.env.ref(
                    'pky_sale_quotation_generator.product_attribute_thickness')

                if (attr_density and attr_length and attr_thickness):
                    attrs_valid.append(attr_density.name)
                    attrs_valid.append(attr_length.name)
                    attrs_valid.append(attr_thickness.name)

                raw_material_product_attrs = list()
                for attr_value in \
                        rec.attribute_value_ids:
                    raw_material_product_attrs.append(
                        attr_value.attribute_id.name
                    )

                rec.raw_material_product_attrs_valid = set(attrs_valid) \
                    .issubset(set(raw_material_product_attrs))

    def _search_attrs_valid(self, operator, value):
        """Implements search on the field raw_material_product_attrs_valid"""

        attrs_valid = list()
        attr_density = self.env.ref(
            'pky_sale_quotation_generator.product_attribute_density')
        attr_length = self.env.ref(
            'pky_sale_quotation_generator.product_attribute_length')
        attr_thickness = self.env.ref(
            'pky_sale_quotation_generator.product_attribute_thickness')

        if (attr_density and attr_length and attr_thickness):
            attrs_valid.append(attr_density.name)
            attrs_valid.append(attr_length.name)
            attrs_valid.append(attr_thickness.name)

        products_valid_attrs_ids = self.search([]).filtered(
            lambda product: product.id
            if set(attrs_valid).issubset(
                set(product.attribute_value_ids.mapped('attribute_id.name'))
                ) else False
        ).mapped('id')

        return [('id', 'in', products_valid_attrs_ids)]
