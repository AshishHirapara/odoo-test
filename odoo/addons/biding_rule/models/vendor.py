from datetime import datetime, date, timedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import Warning
import json
from odoo.exceptions import UserError, ValidationError


class HrEmployeeDocument(models.Model):
    _name = 'hr.employee.document'
    _description = 'HR Employee Documents'

    vendor_document_count = fields.Integer(compute='_vendor_document_count', string='# Documents')

# class HrEmployeeAttachment(models.Model):
#     _inherit = 'ir.attachment'
#
#     doc_attach_rel = fields.Many2many('vendor.partner', string="Attachment", invisible=1)

class HrEmployeeDocument(models.Model):
    _name = 'financial.document'
    _description = 'financial Documents'

    name = fields.Char(string='financial Document name')


class VendorEmployee(models.Model):
    _name = 'vendor.employee'
    _description = 'Vendor Employee'

    name = fields.Char(string='employee name')
    selection = fields.Selection(
        [('under', 'understanding'),
         ('working', 'working'),
         ('proficient', 'proficient'),
         ('proficient', 'proficient'),
         ('expert', ' Expert'),
         ], string="Knowledge Level")
    doc_attachment_id = fields.Many2many('ir.attachment', 'doc_attach_rel', 'doc_id', 'attach_id4', string="Attachment",
                                         help='You can attach the copy of your document', copy=False)
    vendor_3 = fields.Many2one('res.partner', string='vendor')


class VendorPartner(models.Model):
    _name = 'vendor.partner'
    _description = 'vendor partner'

    name = fields.Char(string='Rule name')
    doc_attachment_id = fields.Many2many('ir.attachment', 'class_ir_attachments_rel', 'class_id', 'attachment_id', 'Attachments')
    is_pass = fields.Boolean('passed')
    input_type = fields.Selection(
        [('attach', 'Attach file'),
         ('selection', 'selection'),
         ('tick', 'Tick'),
         ('number', 'number insertion'),
         ('employee', 'Man power'),
         ('financial', 'Financial statement'),
         ], string="Input Type")
    amount = fields.Float(string="Amount")
    selection = fields.Many2one('selection.field', string='selection')
    rule = fields.Many2one('vendor.document', string='rule')
    vendor = fields.Many2one('res.partner', string='vendor')
    value = fields.Float(string="value in %")


class VendorStatement(models.Model):
    _name = 'vendor.statement'
    _description = 'vendor Statement'

    name = fields.Many2one('financial.document',string='information')
    selection = fields.Selection(
        [('balance', 'Information from Balance Sheet'),
         ('income', 'Information from Income Statement')
         ], string="Information Type")
    amount = fields.Float(string="Year 1")
    amount_2 = fields.Float(string="Year 2")
    amount_3 = fields.Float(string="Last Year")
    amount_4 = fields.Float(string="Current Year")
    vendor_2 = fields.Many2one('res.partner', string='vendor')


class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    rule = fields.One2many('vendor.partner', 'vendor', string='rule')
    rule_2 = fields.One2many('vendor.statement', 'vendor_2', string='FINANCIAL DATA')
    rule_3 = fields.One2many('vendor.employee', 'vendor_3', string='Manpower DATA')
    agreement = fields.Many2one('purchase.requisition', string='Purchase agreement')
    value = fields.Float(string="Financial value in %")
    value_2 = fields.Float(string="Manpower value in %")

    @api.onchange('agreement')
    def onchange_input_type(self):
        if self.rule:
         self.rule = [(6,0,0)]
        rules = self.env['product.document'].search([('agreement', '=', self.agreement.id)])
        terms = []
        for rule in rules:
            values = {}
            values['name'] = rule.name
            values['input_type'] = rule.input_type
            values['rule'] = rule.id
            values['value'] = rule.value

            terms.append((0, 0, values))
        self.rule = terms


