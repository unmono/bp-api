import pytest
from decimal import Decimal
from pydantic import ValidationError

from parsebp import models


class TestPriceList:
    entry = models.PriceList(
        part_no='1234567890',
        title_ua='Title UA',
        title_en='Title EN',
        section='1. Section',
        subsection='1.1. Sub Section',
        group='1.1.1. Group',
        uktzed=1234567890,
        min_order=1,
        quantity=1,
        price=Decimal('100.99'),
        truck=True,
    )
    validators_test_data_set = {
        'part_no': {
            'good': [
                '1418502203',
                'F00VC99002',
                'F00HN37002',
                '2437010080',
            ],
            'bad': [
                '14185022031',
                '23670-3902',
                'F00HN3700',
                'F00vc99002',
            ]
        },
        'title_ua': {
            'good': [
                'ТРИМАЧ ПРУЖИНИ ФОРСУН ',
                'ЩІТКА СКЛООЧИСНИКА TWIN ВАНТАЖ [N 77]. 7',
                'РЕМІНЬ ЗУБЧАТИЙ Z=116',
                'К-Т ЗУБЧАТИХ РЕМЕНІВ+ РОЛИКИ',
                'К-Т ЗУБЧАТИХ РЕМЕНІВ/ ВОД. НАСОС',
            ],
            'bad': [
                ':;ASDF',
                '',
                '   ',
                '{}|',
            ]
        },
        'title_en': {
            'good': [
                'Toothed Belt/Pump Set',
                'Tensioning Roller ',
                'Wear Sensor F.Brake Pad',
            ],
            'bad': [
                ':;ASDF',
                '',
                '   ',
                '{}|',
            ]
        },
        'section': {
            'good': [
                '1. Section',
                '2. Section  ',
                '3. section + - a/as',
            ],
            'bad': [
                '1.1. Section',
                '2 Section  ',
                'section + - a/as',
            ]
        },
        'subsection': {
            'good': [
                '1.1. Section',
                '2.2. Section  ',
                '3.3. section + - a/as',
            ],
            'bad': [
                '1.1.1. Section',
                '2.2 Section  ',
                '2 Section  ',
                'section + - a/as',
            ]
        },
        'group': {
            'good': [
                '1.1.1. Section',
                '2.2.2. Section  ',
                '3.2.2. section + - a/as',
            ],
            'bad': [
                '1.1.1 Section',
                '1.1. Section',
                '2. Section  ',
                'section + - a/as',
            ]
        },
    }

    def test_validators(self):
        for field, data_set in self.validators_test_data_set.items():
            for v in data_set['good']:
                setattr(self.entry, field, v)
                assert getattr(self.entry, field) == v.strip()

            for v in data_set['bad']:
                with pytest.raises(ValidationError):
                    setattr(self.entry, field, v)

    @pytest.mark.parametrize('value', [Decimal('101.991'), '101.99', 101.99])
    def test_price(self, value):
        self.entry.price = value
        assert self.entry.price == Decimal('101.99')
