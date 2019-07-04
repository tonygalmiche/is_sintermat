# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_dimensions = fields.Char(u"Dimensions")
    is_matiere    = fields.Char(u"Matière")
