from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Budget(models.Model):
    _name = "budget.budget"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Budget Model"

    name = fields.Char(string='name')
    revised_id = fields.Many2one('budget.budget', string='Revised Budget')

    start_date = fields.Date()
    end_date = fields.Date()
    company = fields.Char()
    favorite = fields.Boolean('Favorite', copy=False, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Responsible')
    user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user)
    budget_lines = fields.One2many("budget.line", "budget_id", string="Items")
    color = fields.Integer(string='Color Index')
    
    is_above_budget = fields.Boolean()
    
    on_over_budget = fields.Selection([
        ('warning','Warning'),
        ('restriction','Restriction')
    ])
    state = fields.Selection([
        ('draft','Draft'),
         ('confirm','Confirm'),
        ('revised','Revised'),
        ('done','Done'),
       
    ],
    default='draft')

    def demo(self):
        return None
    
    


    def confirm_revised_budget(self):
        self.ensure_one()
        # Confirm the revised budget
        self.state = 'confirm'

       
        if self.revised_id:
            self.revised_id.state = 'revised'
            message_body = """
            <p>The revised budget has been confirmed. You can view the original budget 
            <a href='#id={0}&view_type=form&model=budget.budget'>{1}</a>.</p>
            """.format(self.revised_id.id, self.revised_id.name)

           
            message_body2 = """
            <p>The revised budget has been confirmed. You can view the revised budget 
            <a href='#id={0}&view_type=form&model=budget.budget'>{1}</a>.</p>
            """.format(self.id, self.name)


            self.env['mail.message'].create({
            'model': 'budget.budget',
            'res_id': self.id,
            'body': message_body,
            'message_type': 'comment',
            'subtype_id': self.env.ref('mail.mt_comment').id,
            })

            self.env['mail.message'].create({
            'model': 'budget.budget',
            'res_id': self.revised_id.id,
            'body': message_body2,
            'message_type': 'comment',
            'subtype_id': self.env.ref('mail.mt_comment').id,
            })

        

        return True
    
    def open_form(self):
        current_record = self.ensure_one()
        budget = self.env['budget.budget'].search([('id', '=', current_record.id)], limit=1)
        action = {
            'name': 'Budget',
            'type': 'ir.actions.act_window',
            'res_model': 'budget.budget',
            'view_mode': 'form',
            'res_id': budget.id,
        }
        return action
    
    def done_btn(self):
        self.state = 'done'
    
    def reset_to_draft(self):
        self.state = 'draft'

    def open_budget_lines(self):
        self.ensure_one()
        
        budget_lines = self.env['budget.line'].search([('budget_id', '=', self.id)])
      #   budget_lines = self.env['budget.line'].search([])
        
        action = {
            'name': 'Budget Lines',
            'type': 'ir.actions.act_window',
            'res_model': 'budget.line',
            'view_mode': 'tree,pivot,gantt,graph',
            'domain': [('id', 'in', budget_lines.ids)],
        }
        return action
        

    def revised_budget(self):
        new_budget_data = self.copy_data()[0]
        new_budget_data.update({
            'name': f"{self.name}: Revised",
            'state': 'draft',
            'revised_id': self.id,  # Link to the original budget
        })

        new_budget = self.create(new_budget_data)
        self.revised_id = new_budget.id

        # Copy budget lines
        for line in self.budget_lines:
            line_data = line.copy_data()[0]
            line_data['budget_id'] = new_budget.id
            new_line = self.env['budget.line'].create(line_data)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Revised Budget',
            'res_model': 'budget.budget',
            'res_id': new_budget.id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
        }


    @api.model
    def open_budget_wizard(self):
        action = {
            'name': 'Budgets',
            'type': 'ir.actions.act_window',
            'res_model': 'budget.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('budget.view_budget_wizard_form').id,
            'target': 'new',
            'context': {'default_budget_id': self.id},
        }
        return action
    
    @api.constrains('on_over_budget')
    def _check_over_budget(self):
        for record in self:
            budget_lines = self.env['budget.line'].search([('budget_id', '=', record.id)])
            
           
            for line in budget_lines:
                if line.achived_amount > line.budget_amount:
                    if record.on_over_budget == 'restriction':
                        raise ValidationError("Cannot create budget because achived amount is greater than budget amount ")
                    elif record.on_over_budget == 'warning':
                        record.is_above_budget = True