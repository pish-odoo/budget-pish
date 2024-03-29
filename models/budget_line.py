from odoo import models, fields, api
from collections import defaultdict


class BudgetLine(models.Model):
    _name = "budget.line"


    budget_id = fields.Many2one('budget.budget', string="Budget")
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    budget_amount = fields.Integer(string='budget amount')
    achived_amount = fields.Float(string="Achieved Amount" ,compute='_compute_achieved_amount')
    analytic_plan_id = fields.Many2one('account.analytic.plan', 'Analytic Plan',related='analytic_account_id.plan_id', readonly=True)
    budget_name = fields.Char(related='budget_id.name', string="Budget Name")
    achieved_percentage = fields.Float(compute = '_compute_percentage')
    start_date = fields.Date(string="from", related="budget_id.start_date")
    end_date = fields.Date(string="to", related="budget_id.end_date")


    def _compute_display_name(self):
        for incoterm in self:
            incoterm.display_name = f"{incoterm.analytic_account_id.name}"



#     @api.model
#     def _compute_achieved_amount(self):
#             lines = self.search([])
#             print(lines)
#             for line in lines:
#                   analytic_lines = self.env['account.analytic.line'].search([
#                         ('account_id', '=', line.analytic_account_id.id),
#                   ])
#                   print(analytic_lines.amount)
#                   achieved_amount = sum(line.amount for line in analytic_lines)
#                   line.write({'achived_amount': achieved_amount})
            
    def _compute_achieved_amount(self):
        for budget in self:
            achieved_amount = 0.0
            for analytic_plan in budget.analytic_plan_id:
                domain = [
                    ('analytic_account_id', 'in', analytic_plan.account_ids.ids),
                    ('amount', '<', 0.0),
                ]
                if budget.start_date:
                    domain.append(('date', '>=', budget.start_date))
                if budget.end_date:
                    domain.append(('date', '<=', budget.end_date))
                
                analytic_lines = self.env['account.analytic.line'].search(domain)
                for line in analytic_lines:
                    achieved_amount += abs(line.amount) 
            
            budget.achived_amount = achieved_amount
            


    def anlytic_line_tree_view_open(self):
      current_record = self.ensure_one()
      analytic_lines = self.env['account.analytic.line'].search([
          ('account_id', '=', current_record.analytic_account_id.id),
      ])
      print(analytic_lines)
      action = {
          'name': 'Analytic Lines',
          'type': 'ir.actions.act_window',
          'res_model': 'account.analytic.line',
          'view_mode': 'tree',
          'domain': [('id', 'in', analytic_lines.ids)],
      }
      return action



    @api.depends('budget_amount', 'achived_amount')
    def _compute_percentage(self):
       for record in self:
          if record.budget_amount != 0:
            record.achieved_percentage = (record.achived_amount / record.budget_amount) * 100
          else:
            record.achieved_percentage = 0.0


    @api.constrains('on_over_budget')
    def _check_over_budget(self):
        for record in self:
            if record.on_over_budget == 'restriction':
                # Check if any budget.line record has achieved quantity > budget amount
                over_budget_lines = self.env['budget.line'].search([
                    ('budget_id', '=', record.id),
                ])
                for line in over_budget_lines:
                 if line.achieved_amt > line.budget_amt:
                    raise ValidationError("Cannot create account.analytic.line for this period due to budget restrictions.")
            elif record.over_budget == 'warning':
                over_budget_lines = self.env['budget.line'].search([
                    ('budget_id', '=', record.id),
                ])
                for line in over_budget_lines:
                 if line.achieved_amt > line.budget_amt:
                    raise  ValidationError("Cannot create account.analytic.line for this period due to budget restrictions.")


