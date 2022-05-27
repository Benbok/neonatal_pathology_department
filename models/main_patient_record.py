from odoo import fields, models, api, modules
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from datetime import datetime

class PatientRecord(models.Model):
    _name = 'neonatal_pathology_department.patient_record'
    # _sql_constraints = [('case_history_number_unique', 'unique(case_history_number)', 'Такой номер истории уже существует!')]

    @api.multi
    def open_pathology_department(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f'Медицинская документация пациента {self.name}',
            'res_model': 'neonatal_pathology_department.department_record',
            'views': [[False, 'tree'], [False, 'form']],
            'domain': [('pathology_department_id', '=', self.id)],
            'context': {'default_mother_id': self.id}
        }

    @api.onchange('concomitant_diagnosis_id')
    def concomitant_diagnoses_editing(self):
        if self.concomitant_diagnosis_id.name == False:
            pass
        elif self.concomitant_of_the_primary_diagnosis == False:
            self.concomitant_of_the_primary_diagnosis = self.concomitant_diagnosis_id.name
        else:
            self.concomitant_of_the_primary_diagnosis += " " + self.concomitant_diagnosis_id.name
        self.concomitant_diagnosis_id = False


    case_history_number = fields.Char(string='Номер истории', required=True)
    name = fields.Char(string='ФИО матери')
    date_of_birth = fields.Datetime(string='Дата рождения')
    baby_gender = fields.Selection([
        ('мужской', 'мужской'),
        ('женский', 'женский')], string='Пол ребенка')
    history_of_pregnancy = fields.Text(string='Анамнез матери', required=True)
    number_of_births = fields.Integer('Роды по счету')
    number_of_pregnancies = fields.Integer('Беременность по счету')
    severity_of_the_condition = fields.Selection([
        ('удовлетворительное', 'удовлетворительное'),
        ('средней тяжести', 'средней тяжести'),
        ('тяжелое', 'тяжелое')], string="Состояние при рождении")
    apgar_scores = fields.Char(string='Апгар', required=True)
    birth_weight = fields.Integer(string='Масса при рождении(гр)', required=True)
    growth_at_birth = fields.Integer(string='Рост(см)')
    head_circumference = fields.Integer(string='Окружность головы(см)')
    chest_circumference = fields.Integer(string='Окружность грудной клетки(см)')
    gestational_age = fields.Integer(string='Гестационный возраст(недель)')

    obstetric_diagnosis = fields.Text(string='Акушерский диагноз', required=True)

    primary_diagnosis = fields.Many2one('neonatal_pathology_department.mkb', string='Основной: ')
    complication_of_the_primary_diagnosis = fields.Char(string='Осложнение: ')
    concomitant_of_the_primary_diagnosis = fields.Text(string='Сопутсвующий: ')
    concomitant_diagnosis_id = fields.Many2one('neomed_new.concomitant_diagnosis', string='')

    @api.one
    def check_pathology_department_function(self):
        for module in self:
            for rec in module.patient_movement_ids:
                if rec.no != False:
                    module.check_pathology_department = "ОПН"
    check_pathology_department = fields.Char(string=' ', compute='check_pathology_department_function')

# Связанные поля
    patient_movement_ids = fields.One2many('neonatal_pathology_department.patient_movement', 'patient_movement_id', ondelete='cascade')
    pathology_department_ids = fields.One2many('neonatal_pathology_department.department_record', 'pathology_department_id', ondelete='cascade')

class MotionPatient(models.Model):
    _name = 'neonatal_pathology_department.patient_movement'

    @api.one
    @api.depends('date_of_case_closing')
    def compute_bed_day(self):
        if self.date_of_case_closing != False:
            self.bed_day = (self.date_of_case_closing - self.date_of_case_opening).days

    @api.depends("date_of_case_opening")
    def _get_row_no(self):
        count = 1
        for rec in self:
            if self.env['neonatal_pathology_department.patient_movement'].search(
                    [('patient_movement_id', '=', rec.patient_movement_id.id)]):
                rec.no = count
                count += 1

# Связанные поля
    patient_movement_id = fields.Many2one('neonatal_pathology_department.patient_record', string='Движение пациента', required=True)
    case_history_number = fields.Char(string='Номер истории')

# Основные поля формы
    no = fields.Integer("№", compute="_get_row_no")
    date_of_case_opening = fields.Datetime(string='Дата открытия случая', default=lambda self: fields.datetime.now(), required=True)
    date_of_case_closing = fields.Datetime(string='Дата закрытия случая')
    bed_day = fields.Char(string='Койка-день', compute='compute_bed_day', readonly=True)
    motion = fields.Selection([('Выписка', 'Выписка'),
                               ('Перевод в ОПН роддома №3', 'Перевод в ОПН роддома №3'),
                               ('Перевод в ОРИТН роддома №3', 'Перевод в ОРИТН роддома №3'),
                               ('Перевод в другое ЛПУ', 'Перевод в другое ЛПУ')], string='Исход')



class Pathology_department(models.Model):
    _name = 'neonatal_pathology_department.department_record'
    _inherits = {'neonatal_pathology_department.patient_record': 'pathology_department_id'}

    @api.depends("date_of_case_opening")
    def _get_row_no(self):
        count = 1
        for rec in self:
            if self.env['neonatal_pathology_department.department_record'].search(
                    [('pathology_department_id', '=', rec.pathology_department_id.id)]):
                rec.no = count
                count += 1

    @api.depends("pathology_department_id")
    # @api.constrains('pathology_department_id')
    # @api.one
    def admission_pathology_department(self):
        for rec in self:
            for module in self.env['neonatal_pathology_department.patient_movement'].search(
                    [('patient_movement_id', '=', rec.pathology_department_id.id)]):


                if module.no == rec.no:
                    rec.date_of_case_opening = module.date_of_case_opening
                    rec.case_history_number = module.case_history_number

                # else:
                #     raise Warning("Данное поступление пациента не отражено в поле Движение пациента")

    pathology_department_id = fields.Many2one('neonatal_pathology_department.patient_record')
    no = fields.Integer("№", compute="_get_row_no")
    case_history_number = fields.Char(string='Номер истории', compute='admission_pathology_department')
    date_of_case_opening = fields.Datetime(string='Дата поступления', compute='admission_pathology_department', store=True)
