import json
from typing import Any

METADATA_FIELDS = frozenset({"_id", "Data"})


# fmt: off

class HemoesParser:
    def parse(self, raw_json: str) -> dict[str, list[dict[str, Any]]]:
        payload = json.loads(raw_json)
        records = self._remove_metadata(self._extract_records(payload))

        return {
            "blood_types": self._format_blood_stock(records),
        }

    def _extract_records(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        try:
            return payload["result"]["records"]
        except KeyError as error:
            raise KeyError(f"{self.__class__.__name__}: {error}") from error

    def _remove_metadata(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                field_name: status
                for field_name, status in record.items() if field_name not in METADATA_FIELDS
            } for record in records
        ]

    def _format_blood_stock(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                "name": blood_type,
                "status": status
            } for record in records for blood_type, status in record.items()
        ]
