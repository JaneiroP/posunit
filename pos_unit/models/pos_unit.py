import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PosUnit(models.Model):

    _name = 'pos.unit'
