from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
from datetime import datetime

class BudgetWizard(models.Model):
    _name = 'budget.wizard'
    _description = 'Add Offer Wizard'

    start_date = fields.Date()
    end_date = fields.Date()
    period = fields.Selection([('monthly','Monthly'),('quarterly','Quarterly')])
    budget_id = fields.Many2one('budget.budget', string="Budget")
    analytic_account_ids = fields.Many2many('account.analytic.plan', string='Analytic Plan') 


    

    # def make_offer(self):
    #     self.ensure_one()
    #     budget_obj = self.env['budget.budget']
    #     budget_line_obj = self.env['budget.line']
        
    #     # Convert start_date and end_date to string format
    #     start_date_str = self.start_date.strftime('%Y-%m-%d')
    #     end_date_str = self.end_date.strftime('%Y-%m-%d')
        
    #     start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    #     end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
    #     # Create budgets for each month within the specified period
    #     current_date = start_date
    #     while current_date <= end_date:
    #         # Determine the last day of the current month
    #         last_day_of_month = current_date + relativedelta(day=31)
    #         last_day_of_month = min(last_day_of_month, end_date)
            
    #         # Create or update budget with the provided data for the current month
    #         budget_values = {
    #             'name': f"Budget : {current_date.strftime('%Y-%m-%d')} to {last_day_of_month.strftime('%Y-%m-%d')}",
    #             'start_date': current_date.strftime('%Y-%m-%d'),
    #             'end_date': last_day_of_month.strftime('%Y-%m-%d'),
    #             # Add other fields here
    #         }
    #         budget = budget_obj.create(budget_values)
            
            
    #         for analytic_plan in self.analytic_account_ids:
    #             for analytic_account in analytic_plan.account_ids:
    #                 line_values = {
    #                     'budget_id': budget.id,
    #                     'analytic_account_id': analytic_account.id,
    #                     # Add other fields such as budget_amount and achieved_amount here
    #                 }
    #                 budget_line_obj.create(line_values)
            
    #         # Move to the next month
            
    #         if self.period == 'monthly':
    #             current_date += relativedelta(months=1)
    #         elif self.period == 'quarterly':
    #             current_date += relativedelta(months=3)
    #         else: current_date += relativedelta(months=1)
            
        
    #     # Optionally, perform additional actions or return an action
    #     return {
    #         'name': 'Budgets Created',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'budget.budget',
    #         'view_mode': 'tree,form',
    #         'target': 'current',
    #     }

    def make_offer(self):
        self.ensure_one()
        budget_obj = self.env['budget.budget']
        budget_line_obj = self.env['budget.line']
        
        
        start_date_str = self.start_date.strftime('%Y-%m-%d')
        end_date_str = self.end_date.strftime('%Y-%m-%d')
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        
        if self.period == 'monthly':
            date_range = relativedelta(months=1)
        elif self.period == 'quarterly':
            date_range = relativedelta(months=3)
        else:
           
            date_range = relativedelta(months=1)
        
        
        current_date = start_date
        while current_date <= end_date:
   
            last_day_of_period = current_date + date_range - relativedelta(days=1)
            last_day_of_period = min(last_day_of_period, end_date)
            
            
            budget_values = {
                'name': f"Budget : {current_date.strftime('%Y-%m-%d')} to {last_day_of_period.strftime('%Y-%m-%d')}",
                'start_date': current_date.strftime('%Y-%m-%d'),
                'end_date': last_day_of_period.strftime('%Y-%m-%d'),
            }
            budget = budget_obj.create(budget_values)
            
            for analytic_plan in self.analytic_account_ids:
                for analytic_account in analytic_plan.account_ids:
                    line_values = {
                        'budget_id': budget.id,
                        'analytic_account_id': analytic_account.id,
                        
                    }
                    budget_line_obj.create(line_values)
            
       
            current_date += date_range

        return {
            'name': 'Budgets Created',
            'type': 'ir.actions.act_window',
            'res_model': 'budget.budget',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    @api.constrains('start_date', 'end_date')
    def _check_date_range(self):
        for wizard in self:
            if wizard.start_date and wizard.end_date:
                
                start_date_str = wizard.start_date.strftime('%Y-%m-%d')
                end_date_str = wizard.end_date.strftime('%Y-%m-%d')
                
                
                start_year, start_month, _ = start_date_str.split('-')
                start_year = int(start_year)
                start_month = int(start_month)

                
                end_year, end_month, _ = end_date_str.split('-')
                end_year = int(end_year)
                end_month = int(end_month)

                
                if wizard.start_date.day != 1:
                    raise ValidationError("Start date should be the first day of the month")

               
                last_day_of_month = calendar.monthrange(end_year, end_month)[1]
                if wizard.end_date.day != last_day_of_month:
                    raise ValidationError("End date should be the last day of the month")
