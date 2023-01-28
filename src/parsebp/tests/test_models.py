import pytest
from decimal import Decimal
from pydantic import ValidationError

from parsebp import models


class ValidatorsCaseMixin:

    def test_validators(self, data_set, entry):
        for field, data_set in data_set.items():
            for v in data_set['good']:
                v, e = v if type(v) is tuple else (v, v.strip())
                setattr(entry, field, v)
                assert getattr(entry, field) == e

            for v in data_set.get('bad', []):
                v, _ = v if type(v) is tuple else (v, None)
                with pytest.raises(ValidationError):
                    setattr(entry, field, v)


class TestPriceList(ValidatorsCaseMixin):
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
        price='100.99',
        truck='x',
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
        'price': {
            'good': [
                '1.1',
                '0.123',
                '0,123',
                '123',
            ],
            'bad': [
                '1.1.',
                '.1',
                '2e',
            ]
        },
        'truck': {
            'good': [
                ('x', True),
                ('X', True),
                ('X ', True),
                ('Вантажний асортимент', True),
                ('', False),
                (' ', False),
            ]
        }
    }

    def test_validators(self):
        super().test_validators(self.validators_test_data_set, self.entry)


class TestMasterData(ValidatorsCaseMixin):
    entry = models.MasterData(
        part_no='1234567890',
        ean='3165142935904',
        gross='3.318',
        net='3.084',
        weight_unit='KG',
        length='288',
        width='167',
        height='120',
        measure_unit='MM',
        volume='5.772',
        volume_unit='L',
    )
    validators_data_set = {
        'weight_unit': {
            'good': [
                'KG',
                'KG ',
                'Kg',
                'kg',
            ],
            'bad': [
                'KGxasdf',
                ' ',
                '',
            ],
        },
        'measure_unit': {
            'good': [
                'MM',
                'MM ',
                'mm',
                'Mm',
            ],
            'bad': [
                'Mmx',
                ' ',
                '',
            ],
        },
        'volume_unit': {
            'good': [
                'L',
                'L ',
                'l',
            ],
            'bad': [
                'Lx',
                ' ',
                '',
            ],
        },
    }

    def test_validators(self):
        super().test_validators(self.validators_data_set, self.entry)
