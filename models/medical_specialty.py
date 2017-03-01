from odoo import models, fields

class MedicalSpecialty(models.Model):
    _name = 'medical.specialty'
    
    code = fields.Char(size=256, string='Code')
    name = fields.Char(size=256, string='Specialty', required=True,transalate=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]
