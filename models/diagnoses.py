from odoo import fields, models, api, modules


class NeomedConcomitantDiagnosis(models.Model):
    _name = 'neonatal_pathology_department.concomitant_diagnosis'

    @api.model
    def create_models_concomitant_diagnoses(self):
        concomitant_diagnoses = []
        path = modules.get_module_resource('neonatal_pathology_department', 'static/Journals_doc/Сопутствующие диагнозы.txt')
        openfile = open(path, 'r', encoding='utf-8')
        n = 0
        for line in openfile.readlines():
            concomitant_diagnoses.append(line.strip())
            n += 1
        openfile.close()
        for i in concomitant_diagnoses:
            self.env['neonatal_pathology_department.concomitant_diagnosis'].create({
                'name': i
            })
    name = fields.Char(string="Сопутствующий диагноз")ываыв
