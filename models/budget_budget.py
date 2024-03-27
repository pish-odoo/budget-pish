from odoo import models, fields, api

class Budget(models.Model):
    _name = "budget.budget"
    _description = "Budget Model"

    name = fields.Char(string='name')
    responsible = fields.Char()
    revised_id = fields.Char()
    start_date = fields.Date()
    end_date = fields.Date()
    company = fields.Char()
    partner_id = fields.Many2one('res.partner', string='Customer', auto_join=True, tracking=True, domain="['|', ('company_id', '=?', company_id), ('company_id', '=', False)]")
    user_id = fields.Many2one('res.users', string='Project Manager', default=lambda self: self.env.user, tracking=True)
    budget_ids = fields.One2many("budget.line", "budget_id", string="Items")
    color = fields.Integer(string='Color Index')
    state = fields.Selection([
        ('draft','Draft'),
        ('revised','Revised'),
        ('done','Done'),
        ('confirm','Confirm')
    ],
    default='draft')

    def demo(self):
        return None
    
    @api.model
    def open_budget_wizard(self):
        action = {
            'name': 'Budgets',
            'type': 'ir.actions.act_window',
            'res_model': 'budget.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('budget.view_budget_wizard_form').id,
            'target': 'new',
        }
        return action