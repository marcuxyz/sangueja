import json

from app.crawlers.hemoes.parser import HemoesParser


def test_extract_records_without_metadata(hemoes_fixture):
    parser = HemoesParser()
    stock_data = json.loads(hemoes_fixture)
    records = parser._remove_metadata(parser._extract_records(stock_data))

    assert records == [
        {
            "A-": "Crítico",
            "A+": "Estável",
            "B-": "Crítico",
            "B+": "Crítico",
            "AB-": "Alerta",
            "AB+": "Alerta",
            "O-": "Alerta",
            "O+": "Estável",
        }
    ]


def test_collected_at_blood_stock(hemoes_fixture):
    parser = HemoesParser()
    stock_blood_data = json.loads(hemoes_fixture)
    excracted_records = parser._extract_records(stock_blood_data)
    collected_data = parser._collected_at(excracted_records)

    assert collected_data == "05/08/2026"


def test_format_blood_stock(hemoes_fixture):
    parser = HemoesParser()
    stock_blood_data = json.loads(hemoes_fixture)
    records = parser._extract_records(stock_blood_data)
    stock_blood = parser._remove_metadata(records)
    blood_stock = parser._format_blood_stock(stock_blood)

    assert blood_stock == [
        {"name": "A-", "status": "Crítico"},
        {"name": "A+", "status": "Estável"},
        {"name": "B-", "status": "Crítico"},
        {"name": "B+", "status": "Crítico"},
        {"name": "AB-", "status": "Alerta"},
        {"name": "AB+", "status": "Alerta"},
        {"name": "O-", "status": "Alerta"},
        {"name": "O+", "status": "Estável"},
    ]
