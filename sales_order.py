from odoo import api, fields, models, exceptions

class SalesOrder(models.Model):
    _name = 'sales_order_system.sales_order'
    _description = 'sales_order'
    
    STATE_SELECTION = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('forceclosed', 'Force Closed'),
    ]

    so_code = fields.Text('So_code', default='new', readonly=True)
    cutomer_ = fields.Many2one('sales_order_system.customer_master', 'customer_name')
    item_rate_ = fields.Many2one('sales_order_system.item_rate', 'item_rate', domain="[('cutomer_', '=', cutomer_)],")
    qty = fields.Integer('Quantity', required=True)
    amount = fields.Float('Amount', compute="calculate_amount")
    mfgqty = fields.Integer('Mfgqty', compute="_mfgqty")
    dispqty = fields.Integer('Dispqty', compute="_dispqty")
    displayqty = fields.Integer('Displayqty')  # delete
    bal_to_mfg = fields.Integer('Bal_to_mfg', compute="_bal_to_mfg")
    bal_to_disp = fields.Integer('Bal_to_disp', compute="_bal_to_disp")
    bal_disp_amt = fields.Integer('Bal_disp_amt', compute="_bal_disp_amt")
    agree_rate = fields.Text('Agree Rate', related='item_rate_.agree_rate', readonly=True, store=True)

    
    mfg_s = fields.One2many('sales_order_system.mfg', 'sales_order_', 'mfg')
    dispatch_s = fields.One2many('sales_order_system.dispatch', 'sales_order_', 'dispatch')
    state = fields.Selection(STATE_SELECTION, 'State', default='open', readonly=True)

    _rec_name = "so_code"
    
    @api.model
    def create(self, vals):
        vals['so_code'] = self.env['ir.sequence'].next_by_code('sales_order_system.sales_order')
        ite = super().create(vals)
        return ite
    
    @api.constrains('mfgqty')
    def _check_mfgqty(self):
        for record in self:
            if record.mfgqty > record.qty:
                raise exceptions.ValidationError("Manufacturing quantity cannot be greater than order quantity.")
            
    @api.constrains('mfgqty', 'dispqty')
    def _check_mfg_and_disp_qty(self):
        for record in self:
            if record.dispqty > record.mfgqty:
                raise exceptions.ValidationError("Dispatch quantity cannot be greater than manufacturing quantity.")
            
    @api.onchange('item_rate_', 'qty')
    def calculate_amount(self):
        for o in self:
            o.amount = float(o.item_rate_.agree_rate) * o.qty

    @api.depends('mfg_s')
    def _mfgqty(self):
        for i in self:
            total = sum(o.qty for o in i.mfg_s)
            i.mfgqty = total
            
    @api.depends('dispatch_s')
    def _dispqty(self):
        for i in self:
            total = sum(o.qty for o in i.dispatch_s)
            i.dispqty = total   
            
    @api.depends('qty', 'mfgqty')
    def _bal_to_mfg(self):
        for o in self:
            o.bal_to_mfg = o.qty - o.mfgqty
                
    @api.depends('qty', 'dispqty')
    def _bal_to_disp(self):
        for o in self:
            o.bal_to_disp = o.qty - o.dispqty 
            if o.qty > 0 and o.qty == o.dispqty:                #this is wrong approach. cannot change other fields in compute functions
                o.state = 'closed'      
                    
    @api.depends('qty', 'dispqty')
    def _bal_disp_amt(self):
        for i in self:
            ab = 0
            if i.item_rate_ and i.dispqty:
                ab = float(i.item_rate_.agree_rate) * i.dispqty
            i.bal_disp_amt = i.amount - ab
       
    @api.depends('state')
    def action_force_close(self):
        for i in self.filtered(lambda o: o.state == 'open'):
            i.write({'state': 'forceclosed'})           # i.state = 'foreclosed'

    @api.model
    def get_all_data_dict(self):
        all_data_dict = {}
        all_data = self.search_read([], fields=[
            'so_code', 'cutomer_', 'item_rate_', 'qty', 'amount', 'mfgqty', 'dispqty',
            'displayqty', 'bal_to_mfg', 'bal_to_disp', 'bal_disp_amt', 'agree_rate', 'mfg_s', 'dispatch_s', 'state'
        ])

        for data in all_data:
            all_data_dict[data['so_code']] = data

        # Print the data with a custom message
        print("Data Dictionary:")
        print(all_data_dict)

        return all_data_dict
