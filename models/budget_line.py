from odoo import models, fields, api
from collections import defaultdict

class BudgetLine(models.Model):
    _name = "budget.line"


    budget_id = fields.Many2one('budget.budget', string="Budget")
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    budget_amount = fields.Integer(string='budget amount')
    achived_amount = fields.Float(string="Achieved Amount")

    achieved_percentage = fields.Float(compute = '_compute_percentage')

    



    @api.depends('budget_amount', 'achived_amount')
    def _compute_percentage(self):
       for record in self:
          if record.budget_amount != 0:
            record.achieved_percentage = (record.achived_amount / record.budget_amount) * 100
          else:
            record.achieved_percentage = 0.0


