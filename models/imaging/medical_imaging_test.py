from odoo import models, fields

class MedicalImagingTest(models.Model):
    _name = 'medical.imaging.test'
    _description = 'Medical Imaging Test'

    name = fields.Char(size=255, string='Name', required=True)
    code = fields.Char(size=255, string='Code', required=True)
    product_id = fields.Many2one(string='Service', comodel_name='product.product', required=True, domain="[('type', '=', 'service')]")
    test_type = fields.Many2one(string='Type', comodel_name='medical.imaging.test.type', required=True, index=True)
