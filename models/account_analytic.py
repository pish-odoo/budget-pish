from odoo import models, fields, api

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    budget_line_id = fields.Many2one('budget.line', string="Budget Line")