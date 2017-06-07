# -*- coding: utf-8 -*-

from openerp import api, fields, models
from openerp.tools.translate import _

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
    new_product_generated = fields.Char('New product generated', required=True)
    cut_based_on_bottle = fields.Float('Cut (mm)', required=True)
