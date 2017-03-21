from odoo import models, fields 

class MedicalOperatingSector(models.Model):
    _name = 'medical.operating.sector'
    _description = 'Medical Operating Sector'

    name = fields.Char(required=True)
    extra_information = fields.Text()
    operating_area_id = fields.Many2one(string='Operational Area', comodel_name='medical.operating.area', required=True, ondelete='cascade')