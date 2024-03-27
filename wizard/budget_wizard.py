from odoo import models, fields, api

class BudgetWizard(models.TransientModel):
    _name = 'budget.wizard'
    _description = 'Add Offer Wizard'

    start_date = fields.Date()
    end_date = fields.Date()
    period = fields.Selection([('monthly','Monthly'),('quarterly','Quarterly')])
    # analytic_plans = fields.Many2many('account.analytic.plan')


    
    def make_offer(self):

        
        properties = self.env['budget.budget'].browse(self._context.get('active_ids'))
    
        for p in properties :
            self.env['budget.budget'].create({
                'start_date':p.id,
                'end_date' : self.price,
                'analytic_plans' : self.buyer_id.id
            })
        return {'type':'ir.actions.act_window_close'}
    


