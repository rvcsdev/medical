from odoo import models, fields, api, _
# from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta


class MedicalPatient(models.Model):
    '''
    The concept of Patient included in medical.
    '''
    _name = 'medical.patient'
    _description = 'Medical Patient'
    _inherits = {'res.partner': 'partner_id', }

    age = fields.Char(string='Age', compute='_compute_age')
    identification_code = fields.Char(string='Internal Identification', help='Patient Identifier provided by the Health Center. (different from the Social Security Number)')
    general_info = fields.Text(string='General Information')
    dob = fields.Date(string='Date of Birth')
    dod = fields.Datetime(string='Deceased Date')
    active = fields.Boolean(default=True)
    deceased = fields.Boolean(compute='_compute_deceased', store=True, help='Automatically true if deceased date is set')
    partner_id = fields.Many2one(comodel_name='res.partner', required=True, ondelete='cascade', index=True)
    gender = fields.Selection(
        selection=[
            ('m', 'Male'),
            ('f', 'Female'),
        ])
    medical_center_id = fields.Many2one(
        comodel_name='res.partner',
        domain="[('is_institution', '=', True)]",
        string='Medical Center'
    )
    primary_care_doctor = fields.Many2one('medical.physician', string='Primary Care Doctor', select=True)
    hospitalization_status = fields.Selection([
        ('outpatient','Outpatient'),
        ('hospitalized', 'Hospitalized'),
    ], readonly=True, string='Hospitalization Status')
    insurance_id = fields.Many2one('medical.insurance', string='Insurance', select=True)
    marital_status = fields.Selection(
        selection=[
            ('s', 'Single'),
            ('m', 'Married'),
            ('w', 'Widowed'),
            ('d', 'Divorced'),
            ('x', 'Separated'),
            ('z', 'law marriage'),
        ], required=True, string='Marital Status')

    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ], string='Blood Type')

    rh_factor = fields.Selection([
        ('+', '+'),
        ('-', '-'),
    ], string='Rhesus (RH) Factor')

    ethnic_group = fields.Many2one(string='Ethnic Group', comodel_name='medical.ethnic.group')

    family_id = fields.Many2one(string='Family', comodel_name='medical.patient.family')

    ## Lifestyle

    # Excercise
    is_excercise = fields.Boolean(string='Excercise')
    excercise_minutes_per_day = fields.Integer(string='Minutes / Day', default=0)

    # Sleep
    hours_of_sleep = fields.Integer(string='Hours of Sleep', default=0)
    sleeps_at_daytime = fields.Boolean(string='Sleeps at Daytime')

    # Diet Info 
    meals_per_day = fields.Integer(string='Meals Per Day')
    is_soft_drink = fields.Boolean(string='Soft Drink (Sugar)')
    is_eat_alone = fields.Boolean(string='Eats Alone')
    is_salt = fields.Boolean(string='Salt')
    is_coffee = fields.Boolean(string='Coffee')
    coffee_cups_per_day = fields.Char(string='Cups Per Day')
    is_currently_on_diet = fields.Boolean(string='Currently on Diet')
    diet_info = fields.Char(string='Diet Info')

    lifestyle_info = fields.Text(string='Lifestyle Information')

    is_pregnant = fields.Boolean(
        help='Check if the patient is pregnant',
    )

    appointment_ids = fields.One2many('medical.appointment', inverse_name='patient_id', string="Appointments", ondelete="cascade")

    visit_ids = fields.One2many('medical.visit', inverse_name='patient_id', string='Visits', ondelete='cascade')

    hospitalization_ids = fields.One2many('medical.patient.hospitalization', inverse_name='patient_id', string='Hopsitalizations', ondelete='cascade')

    laboratory_ids = fields.One2many('medical.lab', inverse_name='patient_id', string='Laboratory Tests', ondelete='cascade')
    # @api.multi
    # @api.onchange('state_id')
    # def onchange_state(self):
    #     """ Hack to allow for onchange_state on partner.
    #     Uses current user's partner, as there should be no correlation
    #     between the partner and the response from this method anyways
    #     """
    #     res = self.env.user.partner_id.onchange_state(self.state_id.id)
    #     for key, val in res.get('value', {}).items():
    #         setattr(self, key, val)
    #     return res
    surgery_ids = fields.One2many(string='Surgeries', comodel_name='medical.surgery', inverse_name='patient_id', ondelete='cascade')

    @api.one
    def _compute_age(self):
        """ Age computed depending on the birth date of the patient """
        now = fields.Datetime.from_string(
            self.env.context.get('date', fields.Datetime.now())
        )
        if self.dob:
            dob = fields.Datetime.from_string(self.dob)

            if self.deceased:
                dod = fields.Datetime.from_string(self.dod)
                delta = relativedelta(dod, dob)
                deceased = _(' (deceased)')
            else:
                delta = relativedelta(now, dob)
                deceased = ''
            years_months_days = str(delta.years) + _('y ') + str(
                delta.months) + _('m ') + str(delta.days) + _('d')\
                + deceased
        else:
            years_months_days = _('No DoB !')
        self.age = years_months_days

    @api.multi
    @api.constrains('is_pregnant', 'gender')
    def _check_is_pregnant(self):
        for rec_id in self:
            if rec_id.is_pregnant and rec_id.gender != 'f':
                raise ValidationError(_(
                    'Invalid selection - males cannot be pregnant.',
                ))

    @api.one
    def action_invalidate(self):
        for rec_id in self:
            rec_id.active = False
            rec_id.partner_id.active = False

    @api.multi
    @api.depends('dod')
    def _compute_deceased(self):
        for rec_id in self:
            rec_id.deceased = bool(rec_id.dod)

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        vals['is_patient'] = True
        if not vals.get('identification_code'):
            sequence = self.env['ir.sequence'].get('medical.patient')
            vals['identification_code'] = sequence
        return super(MedicalPatient, self).create(vals)
