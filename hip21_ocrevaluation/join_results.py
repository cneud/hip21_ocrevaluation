from contextlib import contextmanager
from csv import DictReader, DictWriter

from xlsxwriter import Workbook
from click import command, argument, option

FIELDS = [
    'prima_ID', 'language', 'OCR_conf',
    'dingle_CER', 'ocreval_CER', 'evalUA_CER', 'prima_CER',
    'dingle_WER', 'ocreval_WER', 'evalUA_WER', 'prima_WER',
    'evalUA_BoW', 'prima_BoW',
    'prima_layout1', 'prima_layout2', 'prima_layout3', 'prima_layout4',
    'prima_FCER',
]

FIELD_MAPPINGS = {
    'csv/dinglehopper.csv':         {'language': 'language', 'prima_id': 'prima_ID', 'CER': 'dingle_CER', 'WER': 'dingle_WER'},
    'csv/ocrconf-enp.csv':          {'language': 'language', 'prima_id': 'prima_ID', 'conf': 'OCR_conf'},
    'csv/ocrconf-impact.csv':       {'language': 'language', 'prima_id': 'prima_ID', 'conf': 'OCR_conf'},
    'csv/ocreval-enp-cer.csv':      {'language': 'language', 'prima_id': 'prima_ID', 'CER': 'ocreval_CER'},
    'csv/ocreval-enp-wer.csv':      {'language': 'language', 'prima_id': 'prima_ID', 'WER': 'ocreval_WER'},
    'csv/ocreval-impact-cer.csv':   {'language': 'language', 'prima_id': 'prima_ID', 'CER': 'ocreval_CER'},
    'csv/ocreval-impact-wer.csv':   {'language': 'language', 'prima_id': 'prima_ID', 'WER': 'ocreval_WER'},
    'csv/ocrevaluation-enp.csv':    {'language': 'language', 'prima_id': 'prima_ID', 'CER': 'evalUA_CER', 'WER': 'evalUA_WER', 'BOW': 'evalUA_BoW'},
    'csv/ocrevaluation-impact.csv': {'language': 'language', 'prima_id': 'prima_ID', 'CER': 'evalUA_CER', 'WER': 'evalUA_WER', 'BOW': 'evalUA_BoW'},
    'csv/layouteval-impact.csv':    {'prima_id': 'prima_ID', 'prima_layout1': 'prima_layout1', 'prima_layout2': 'prima_layout2', 'prima_layout3': 'prima_layout3', 'prima_layout4': 'prima_layout4'},
    'csv/layouteval-enp.csv':    {'prima_id': 'prima_ID', 'prima_layout1': 'prima_layout1', 'prima_layout2': 'prima_layout2', 'prima_layout3': 'prima_layout3', 'prima_layout4': 'prima_layout4'},
    'csv/texteval-impact-cer.csv':  {'prima_id': 'prima_ID', 'CER': 'prima_CER'},
    'csv/texteval-impact-fcer.csv': {'prima_id': 'prima_ID', 'CER': 'prima_FCER'},
    'csv/texteval-impact-wer.csv':  {'prima_id': 'prima_ID', 'WER': 'prima_WER'},
    'csv/texteval-impact-bow.csv':  {'prima_id': 'prima_ID', 'BOW': 'prima_BoW'},
    'csv/texteval-enp-cer.csv':  {'prima_id': 'prima_ID', 'CER': 'prima_CER'},
    # 'csv/texteval-enp-fcer.csv': {'prima_id': 'prima_ID', 'CER': 'prima_FCER'},
    'csv/texteval-enp-wer.csv':  {'prima_id': 'prima_ID', 'WER': 'prima_WER'},
    'csv/texteval-enp-bow.csv':  {'prima_id': 'prima_ID', 'BOW': 'prima_BoW'},
}

@contextmanager
def get_csv_reader(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        reader = DictReader(f)
        yield reader

class EvalDB():

    def __init__(self):
        self._db = {}

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


@command()
@option('--csv/--excel', default=False, help='Output one CSV per dataset instead of excel')
@argument('fname')
def merge_csv(csv, fname):
    evaldb = EvalDB()
    evaldb.populate()
    getattr(evaldb, 'to_csv' if csv else 'to_excel')(fname)

if __name__ == "__main__":
    merge_csv()
