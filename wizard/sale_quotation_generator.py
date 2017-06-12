# -*- coding: utf-8 -*-

from openerp import api, fields, models
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)
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
        related='raw_material_product_id.standard_price'
    )
    raw_material_product_cost_currency_id = fields.Many2one(
        related='raw_material_product_id.cost_currency_id'
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
    new_product_generated = fields.Char('New product generated', required=True)
    total_thousands_new_product = fields.Float(
        'Thousands', compute='_compute_total_thousands')
    cut_based_on_bottle = fields.Float('Cut (mm)', required=True)
    current_rate_usd = fields.Float(compute='_compute_current_rate_usd')

    @api.depends('raw_material_product_id')
    def _compute_length_mm(self):
        """Compute value of field raw_material_product_length_mm, the value is
        the result of process of the attribute length of the product converting it from
        meters to millimeters."""

        for rec in self:
            rec.raw_material_product_length_mm = False

            if rec.raw_material_product_id:
                attr_length_object = self.env.ref(
                    'pky_sale_quotation_generator.product_attribute_length')
                product_has_attr_length = [attr.name for attr in
                    rec.raw_material_product_id.attribute_value_ids
                    if attr.attribute_id == attr_length_object]

                if product_has_attr_length:
                    rec.raw_material_product_length_mm = \
                        float(product_has_attr_length[0]) * 1000

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
