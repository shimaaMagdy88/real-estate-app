from odoo.tests.common import TransactionCase
from odoo import fields


class TestProperty(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestProperty, self).setUp()

        self.property_01_test = self.env['property'].create({
            'name': 'test_property',
            'ref': 'prt111',
            'date_availability': fields.Date.today(),
            'bedrooms': 4,
            'selling_price': 2000,
            'garden_area': 150,
            'garden_orientation': 'north'
        })

    def property_01_test_values(self):
        property_id = self.property_01_test
        expected_values = [{
            'name': 'test_property',
            'ref': 'prt112',
            'date_availability': fields.Date.today(),
            'bedrooms': 4,
            'selling_price': 2000,
            'garden_area': 150,
            'garden_orientation': 'north'
        }]

        self.assertRecordValues(property_id, expected_values)
