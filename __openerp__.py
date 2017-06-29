# -*- coding: utf-8 -*-
{
    'name': "pky_sale_quotation_generator",
    'summary': """
        Adds a wizard that allow generate new quotations based on parameters
        asociated to the operations of the company Pack System.""",
    'description': """
        Extension of addon sale for add a wizard that allow generate new quotations
        based on parameters asociated to the operations of the company Pack System.
    """,
    'author': "Humanytek",
    'website': "http://www.humanytek.com",
    'category': 'Sales Management',
    'version': '0.1.0',
    'depends': ['sale', 'mrp', 'purchase_product_cost_currency'],
    'data': [
        'data/product_attribute.xml',
        'data/product_uom.xml',
        'wizard/sale_quotation_generator_view.xml',
    ],
    'demo': [
        'demo/suppliers.xml',
        'demo/products.xml',
    ],
}
