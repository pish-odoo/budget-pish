from odoo import models, fields

class BudgetLine(models.Model):
    _name = "budget.line"
#     _inherit = 'account.analytic.line'

    budget_id = fields.Many2one('budget.budget', string="Budget")

