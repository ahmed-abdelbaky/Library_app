from odoo import models, fields
from odoo.exceptions import  ValidationError

class Book(models.Model):
    _name = 'library.book'
    _description = 'book'
    name = fields.Char('Title', required=True)
    isbn = fields.Char('ISBN')
    active = fields.Boolean('Active?', required=True)
    date_published = fields.Date()
    image = fields.Binary('Cover')
    published_id = fields.Many2one('res.partner', string='Published')
    author_ids = fields.Many2many('res.partner', string='Authors')

    def _check_isbn(self):
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderation = [1, 3] * 6
            terms = [a * b for a, b in zip(digits[:12], ponderation)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check

    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise ValidationError(f"Please Enter Serial Number for {book.name}")
            if book.isbn and not book._check_isbn():
                raise ValidationError(f"please Serial Number is Invalid for {book.name}")