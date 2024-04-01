from odoo import models, fields, api
from collections import defaultdict
import math
from odoo.exceptions import UserError, ValidationError

class BudgetLine(models.Model):
    _name = "budget.line"


    budget_id = fields.Many2one('budget.budget', string="Budget")
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    budget_amount = fields.Integer(string='budget amount', default=1000)
    achived_amount = fields.Float(string="Achieved Amount" ,compute='_compute_achieved_amount')
    rel_achived_amount = fields.Float(related='achived_amount', store=True)
   
    budget_name = fields.Char(related='budget_id.name', string="Budget Name")
    achieved_percentage = fields.Float(compute = '_compute_percentage')
    start_date = fields.Date(string="from", related="budget_id.start_date")
    end_date = fields.Date(string="to", related="budget_id.end_date")
  

    def _compute_display_name(self):
        for incoterm in self:
            incoterm.display_name = f"{incoterm.analytic_account_id.name}"


   
    @api.depends('analytic_account_id')
    def _compute_achieved_amount(self):
        for line in self:
            print('jii')
            print(line.analytic_account_id.id)
            analytic_lines = self.env['account.analytic.line'].search([
            ('auto_account_id', '=', line.analytic_account_id.id),
            ('date', '>=', line.start_date),
            ('date', '<=', line.end_date),
            # ('amount'< '0')
            ])
            achieved_amount = sum(analytic_line.amount for analytic_line in analytic_lines)
            line.achived_amount = abs(achieved_amount)

            
    
    def anlytic_line_tree_view_open(self):
        if self.analytic_account_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Analytic Line',
                'res_model': 'account.analytic.line',
                'res_id': self.analytic_account_id.id,
                'view_mode': 'tree',
                'view_type': 'tree',
                'target': 'current',
            }



    @api.depends('budget_amount', 'achived_amount')
    def _compute_percentage(self):
       for record in self:
          if record.budget_amount != 0:
            record.achieved_percentage = (record.achived_amount / record.budget_amount) * 100
          else:
            record.achieved_percentage = 0.0


#     @api.constrains('on_over_budget')
#     def _check_over_budget(self):
#         for record in self:
#             if record.on_over_budget == 'restriction':
               
#                 over_budget_lines = self.env['budget.line'].search([
#                     ('budget_id', '=', record.id),
#                 ])
#                 for line in over_budget_lines:
#                  if line.achived_amount > line.budget_amount:
#                     raise ValidationError("Cannot create budget because achived amount is greater than budget amount .")
#             elif record.over_budget == 'warning':
#                 over_budget_lines = self.env['budget.line'].search([
#                     ('budget_id', '=', record.id),
#                 ])
#                 for line in over_budget_lines:
#                  if line.achived_amount > line.budget_amount:
#                     raise  ValidationError("Cannot create budget because achived amount is greater than budget amount")

