from csv import DictReader, DictWriter
from contextlib import contextmanager

fieldnames = [
    'prima_id',
    'dataset',
    'language',
    'CER',
    'FCER',
    'WER',
    'BOW',
    'conf',
    'words_total',
    'words_wrong',
    'chars_total',
    'chars_wrong',
    'prima_layout1',
    'prima_layout2',
    'prima_layout3',
    'prima_layout4',
]


@contextmanager
def get_csv_writer(out_filename):
    with open(out_filename, 'w', encoding='utf-8') as f_out:
        writer = DictWriter(f_out, fieldnames=fieldnames)
        writer.writerow({x: x for x in fieldnames})
        yield writer

@contextmanager
def get_csv_reader(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        reader = DictReader(f)
        yield reader

