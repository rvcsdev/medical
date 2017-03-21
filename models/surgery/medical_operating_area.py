from odoo import models, fields

class MedicalOperatingArea(models.Model):
    _name = 'medical.operating.area'
    _description = 'Medical Operating Area'

    name = fields.Char(required=True)
    extra_information = fields.Text()
    operating_sector_ids = fields.One2many(string='Operational Sector', comodel_name='medical.operating.sector', inverse_name='operating_area_id')