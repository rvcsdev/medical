from odoo import api, models, fields, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class MedicalPatientHospitalizationTransfer(models.Model):
    _name = 'medical.patient.hospitalization.transfer'
    _description = 'Medical Patient Hospitalization Transfer'
    
    hospitalization_id = fields.Many2one(comodel_name='medical.patient.hospitalization', string='Hospitalization', ondelete='cascade', required=True, select=True, default=lambda self: self._context.get('hospitalization_id'))
    transfer_date = fields.Datetime(string='Date', default=fields.Datetime.now, readonly=True)
    transfer_from = fields.Many2one(string='From', comodel_name='medical.hospital.bed', required=True, select=True, default=lambda self: self._context.get('current_bed'))
    transfer_to = fields.Many2one(string='To', comodel_name='medical.hospital.bed', required=True, select=True, help='Assign new bed to patient.')
    transfer_reason = fields.Text(string='Reason')

    @api.multi
    def action_transfer(self):
        hospitalization = self.env['medical.patient.hospitalization'].browse(self.hospitalization_id.id)
        hospitalization.hospital_bed_id = self.transfer_to
        return {'type': 'ir.actions.act_window_close'}