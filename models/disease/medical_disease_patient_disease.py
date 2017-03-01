# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MedicalPatientDisease(models.Model):
    _name = 'medical.patient.disease'
    _description = 'Medical Patient Disease'

    @api.one
    @api.depends('short_comment', 'pathology_id', 'pathology_id.name')
    def _compute_name(self):
        name = self.pathology_id.name
        if self.short_comment:
            name = '%s - %s' % (name, self.short_comment)
        self.name = name

    @api.one
    @api.depends('active')
    def _compute_expire_date(self):
        if self.active:
            self.expire_date = False
        else:
            self.expire_date = fields.Datetime.now()

    @api.one
    def action_invalidate(self):
        self.active = False

    @api.one
    def action_revalidate(self):
        self.active = True

    name = fields.Char(compute='_compute_name', store=True)
    treatment_description = fields.Char(string='Treatment Description')
    expire_date = fields.Datetime(compute='_compute_expire_date', store=True)
    short_comment = fields.Char(string='Short Comment')
    pathology_id = fields.Many2one(comodel_name='medical.pathology', string='Pathology', index=True, required=True)
    physician_id = fields.Many2one(comodel_name='medical.physician', string='Physician', index=True)
    patient_id = fields.Many2one(comodel_name='medical.patient', string='Patient', required=True, index=True)
    disease_severity = fields.Selection([
        ('1_mi', 'Mild'),
        ('2_mo', 'Moderate'),
        ('3_sv', 'Severe')
    ], string='Severity')
    state = fields.Selection([
        ('a', 'Acute'),
        ('c', 'Chronic'),
        ('u', 'Unchanged'),
        ('h', 'Healed'),
        ('i', 'Improving'),
        ('w', 'Worsening'),
    ], string='Status of the disease')
    allergy_type = fields.Selection([
        ('da', 'Drug Allergy'),
        ('fa', 'Food Allergy'),
        ('ma', 'Misc Allergy'),
        ('mc', 'Misc Contraindication'),
    ])
    weeks_of_pregnancy = fields.Integer(
        help='Week number of pregnancy when disease contracted',
        string='Pregnancy Week#')
    age = fields.Integer(string='Age when Diagnosed')
    active = fields.Boolean(default=True)
    is_infectious = fields.Boolean(string='Infectious Disease')
    is_allergy = fields.Boolean(string='Allergic Disease')
    pregnancy_warning = fields.Boolean()
    is_pregnant = fields.Boolean(string='Pregnancy Warning')
    is_on_treatment = fields.Boolean(string='Currently on Treatment')
    treatment_start_date = fields.Date(string='Treatment Start Date')
    treatment_end_date = fields.Date(string='Treatment End Date')
    diagnosed_date = fields.Date(string='Date of Diagnosis')
    healed_date = fields.Date(string='Date of Healing')
    notes = fields.Text()
