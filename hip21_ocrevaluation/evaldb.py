from csv import DictWriter
from xlsxwriter import Workbook
from pathlib import Path

from .constants import FIELDS, FIELD_MAPPINGS
from .utils import get_csv_reader

class EvalDB():

    def __init__(self, path_to_csv):
        self._db = {}
        self.path_to_csv = Path(path_to_csv)

    def get(self, dataset, prima_id):
        if dataset not in self._db:
            self._db[dataset] = {}
        if prima_id not in self._db[dataset]:
            self._db[dataset][prima_id] = {}
        return self._db[dataset][prima_id]

    def set(self, dataset, prima_id, field, val):
        if val in (None, ''):
            return
        if field not in FIELDS:
            raise ValueError(f"Invalid field {field}")
        if ('CER' in field or 'WER' in field or 'BoW' in field) and float(val) > 1:
            print("%s/%s: invalid %s value %s > 1, setting to 1" % (dataset, prima_id, field, val))
            val = 1
        self.get(dataset, prima_id)[field] = val

    def populate(self):
        for fname, mapping in FIELD_MAPPINGS.items():
            with get_csv_reader(fname) as reader:
                for row in reader:
                    for src, dst in mapping.items():
                        self.set(row['dataset'], row['prima_id'], dst, row[src])

    def to_csv(self, fname):
        for dataset, rows in self._db.items():
            csv_fname = f'{fname}-{dataset}.csv'
            with open(csv_fname, 'w', encoding='utf-8') as f:
                writer = DictWriter(f, fieldnames=FIELDS)
                writer.writerow({x: x for x in FIELDS})
                for row_idx, row in enumerate(rows.values()):
                    writer.writerow(row)


    def to_excel(self, fname):
        wb = Workbook(fname)
        for dataset, rows in self._db.items():
            sheet = wb.add_worksheet(dataset)
            for field_idx, field in enumerate(FIELDS):
                sheet.write(0, field_idx, field)
            for row_idx, row in enumerate(rows.values()):
                for field_idx, field in enumerate(FIELDS):
                    if field in row:
                        sheet.write(row_idx + 1, field_idx, row[field])
        wb.close()

