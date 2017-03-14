# This file is part stock_delivery_note_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import Model, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all_ = ['Configuration', 'StockConfigurationCompany']


class Configuration:
    __metaclass__ = PoolMeta
    __name__ = 'stock.configuration'

    shipment_qty_decimal = fields.Function(fields.Boolean(
            'Shipment Qty Decimal', help='Show qty with or without decimals'),
        'get_company_config', 'set_company_config')

    @classmethod
    def get_company_config(cls, configs, names):
        pool = Pool()
        CompanyConfig = pool.get('stock.configuration.company')

        company_id = Transaction().context.get('company')
        company_configs = CompanyConfig.search([
                ('company', '=', company_id),
                ])

        res = {}
        for fname in names:
            res[fname] = {
                configs[0].id: None,
                }
            if company_configs:
                val = getattr(company_configs[0], fname)
                if isinstance(val, Model):
                    val = val.id
                res[fname][configs[0].id] = val
        return res

    @classmethod
    def set_company_config(cls, configs, name, value):
        pool = Pool()
        CompanyConfig = pool.get('stock.configuration.company')

        company_id = Transaction().context.get('company')
        company_configs = CompanyConfig.search([
                ('company', '=', company_id),
                ])
        if company_configs:
            company_config = company_configs[0]
        else:
            company_config = CompanyConfig(company=company_id)
        setattr(company_config, name, value)
        company_config.save()


class StockConfigurationCompany(ModelSQL):
    'Stock Configuration per Company'
    __name__ = 'stock.configuration.company'

    company = fields.Many2One('company.company', 'Company', required=True,
        ondelete='CASCADE', select=True)
    shipment_qty_decimal = fields.Boolean('Shipment Qty Decimal')
