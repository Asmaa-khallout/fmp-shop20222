import logging
import pprint
import re
import unicodedata
from datetime import datetime

import psycopg2
from dateutil import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import consteq, format_amount, ustr
from odoo.tools.misc import hmac as hmac_tool

from odoo.addons.payment import utils as payment_utils

_logger = logging.getLogger(__name__)


class PaymentTransactionn(models.Model):
    _inherit = 'payment.transaction'

  
    def _cron_finalize_post_processing(self):
        """ Finalize the post-processing of recently done transactions not handled by the client.
        :return: None
        """
        txs_to_post_process = self
        if not txs_to_post_process:
            # Let the client post-process transactions so that they remain available in the portal
            client_handling_limit_date = datetime.now() - relativedelta.relativedelta(minutes=1)
            # Don't try forever to post-process a transaction that doesn't go through. Set the limit
            # to 4 days because some providers (PayPal) need that much for the payment verification.
            retry_limit_date = datetime.now() - relativedelta.relativedelta(days=4)
            # Retrieve all transactions matching the criteria for post-processing
            txs_to_post_process = self.search([
                ('state', '=', 'done'),
                ('is_post_processed', '=', False),
                '|', ('last_state_change', '<=', client_handling_limit_date),
                     ('operation', '=', 'refund'),
                ('last_state_change', '>=', retry_limit_date),
            ])
        for tx in txs_to_post_process:
            try:
                tx._finalize_post_processing()
                self.env.cr.commit()
            except psycopg2.OperationalError:  # A collision of accounting sequences occurred
                self.env.cr.rollback()  # Rollback and try later
            except Exception as e:
                _logger.exception(
                    "encountered an error while post-processing transaction with id %s:\n%s",
                    tx.id, e
                )
                self.env.cr.rollback()