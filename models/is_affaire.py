# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning


class IsPhase(models.Model):
    _name = 'is.phase'
    _description = "Phase"
    _order = 'name'

    name        = fields.Char("Phase", required=True, index=True)
    probabilite = fields.Integer(u"Probabilité (%)")
    description = fields.Text("Description")


class IsAffaire(models.Model):
    _name = 'is.affaire'
    _description = u"Affaire"
    _order='name'

    name        = fields.Char("Affaire", readonly=True)
    description = fields.Text("Description")
    phase_id    = fields.Many2one('is.phase', 'Phase', required=True)


    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('is.affaire')
        res = super(IsAffaire, self).create(vals)
        return res




