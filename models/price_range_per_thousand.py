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


class PriceRangePerThousand(models.TransientModel):

    _name = 'price.range.per.thousand'

    lower_limit = fields.Integer('Lower Limit', required=True)
    upper_limit = fields.Integer('Upper Limit', required=True)
    percentage_raw_material_on_sale_price = fields.Float(
        'Percentage of Raw Material', required=True)
    sale_price_per_thousand_without_printing = fields.Float(
        'Sale Price Per Thousand Without Printing',
        compute='_compute_sale_price_per_thousand_without_printing')
    sale_price_per_thousand_usd = fields.Float(
        'Sale Price Per Thousand (USD)',
        compute='_compute_sale_price_per_thousand_usd')
    sale_price_per_thousand_mxn = fields.Float(
        'Sale Price Per Thousand (MXN)',
        compute='_compute_sale_price_per_thousand_mxn')
    sale_quotation_generator_id = fields.Many2one(
        'sale.quotation.generator',
        'Sale Quotation Generator (Wizard)',
        required=True)

    @api.depends(
        'percentage_raw_material_on_sale_price',
        'sale_quotation_generator_id')
    def _compute_sale_price_per_thousand_without_printing(self):
        """Compute value of fields sale_price_per_thousand_without_printing for
        range of thousands taking into account the percentage of raw material.
        """

        for rec in self:
            rec.sale_price_per_thousand_without_printing = False

            if rec.percentage_raw_material_on_sale_price:
                rec.sale_price_per_thousand_without_printing = \
                    rec.sale_quotation_generator_id.cost_per_thousand / \
                    float('0.{0}'.format(
                        int(round(
                            rec.percentage_raw_material_on_sale_price
                            ))
                    ))

    @api.depends(
        'sale_quotation_generator_id',
        'sale_price_per_thousand_without_printing')
    def _compute_sale_price_per_thousand_mxn(self):
        """Compute sale price in MXN per thousand for range of thousands taking
        into account the percentage of raw material"""

        for rec in self:
            rec.sale_price_per_thousand_mxn = False

            if rec.sale_price_per_thousand_without_printing:
                if (rec.sale_quotation_generator_id.current_rate_usd and
                        rec.sale_quotation_generator_id.total_ink_cost and
                        rec
                        .sale_quotation_generator_id
                        .total_thousands_new_product
                        and
                        rec.sale_quotation_generator_id.glue_other_expenses):

                    rec.sale_price_per_thousand_mxn = \
                        (rec.sale_price_per_thousand_without_printing *
                            rec.sale_quotation_generator_id.current_rate_usd) \
                        + (rec.sale_quotation_generator_id.total_ink_cost /
                            rec
                            .sale_quotation_generator_id
                            .total_thousands_new_product) \
                        + (rec.sale_quotation_generator_id.glue_other_expenses
                            / rec
                            .sale_quotation_generator_id
                            .total_thousands_new_product)

    @api.depends(
        'sale_quotation_generator_id',
        'sale_price_per_thousand_mxn')
    def _compute_sale_price_per_thousand_usd(self):
        """Compute sale price in USD per thousand for range of thousands taking
        into account the percentage of raw material"""

        for rec in self:
            rec.sale_price_per_thousand_usd = False

            if (rec.sale_price_per_thousand_mxn and
                    rec.sale_quotation_generator_id.current_rate_usd):

                rec.sale_price_per_thousand_usd = \
                    rec.sale_price_per_thousand_mxn / \
                    rec.sale_quotation_generator_id.current_rate_usd
