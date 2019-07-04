# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_dimensions = fields.Char(u"Dimensions")
    is_matiere    = fields.Char(u"Matière")


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    def name_get(self):
        result = []
        for obj in self:
            name=u''
            if obj.default_code:
                name+=u'['+obj.default_code+u']'
            if obj.is_dimensions:
                name+=u'['+obj.is_dimensions+u']'
            if obj.is_matiere:
                name+=u'['+obj.is_matiere+u']'
            if name!=u'':
                name+=u' '
            name=name+obj.name
            result.append((obj.id, name))
        return result



    def get_product_multiline_description_sale(self):
        name = self.display_name
        name = self.name
        if self.description_sale:
            name += '\n' + self.description_sale

        #if self.is_dimensions:
        #    name += '\n' + u'Dimensions : '+self.is_dimensions
        #if self.is_matiere:
        #    name += '\n' + u'Matière : '+self.is_matiere

        return name


