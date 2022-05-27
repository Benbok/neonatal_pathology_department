from odoo import fields, models, api, modules
import openpyxl


class MKB(models.Model):
    _name = 'neonatal_pathology_department.mkb'
    name = fields.Char(string="Диагноз МКБ")

    @api.model
    def create_models(self):
        list_b = []
        path = modules.get_module_resource('neonatal_pathology_department', 'static/files/mkb10.xlsx')
        wb = openpyxl.load_workbook(path)
        for i in wb["МКБ-10"]:
            list_b.append([i[0].value, i[1].value])
        for i in list_b:
            self.env['neonatal_pathology_department.mkb'].create({
                'name': i[0] + ' ' + i[1]
            })