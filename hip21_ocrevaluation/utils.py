from csv import DictReader, DictWriter
from re import search
from contextlib import contextmanager

from .constants import TEMP_FIELDNAMES, LANGUAGES, ENP_IDS, ENP_DEU_IDS

@contextmanager
def get_csv_writer(out_filename):
    with open(out_filename, 'w', encoding='utf-8') as f_out:
        writer = DictWriter(f_out, fieldnames=TEMP_FIELDNAMES)
        writer.writerow({x: x for x in TEMP_FIELDNAMES})
        yield writer

@contextmanager
def get_csv_reader(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        reader = DictReader(f)
        yield reader

def classify_filename(fname):
    ret = {}
    ret['prima_id'] = search(r'([0-9]{8})', fname).group(1)
    is_gt4hist = 'gt4hist' in fname or 'g4hist' in fname
    if not is_gt4hist:
        try:
            lang = next(lang for lang in LANGUAGES if f'.{lang}' in fname)
        except Exception as e:
            print(fname)
            raise e
        ret['language'] = lang
    ret['dataset'] = 'impact' if 'impact' in fname else 'enp'
    if ret['dataset'] == 'enp' and not is_gt4hist and ret['prima_id'] not in ENP_IDS:
        print("Prima ID not in enp_map: %s" % ret)
        return
    elif ret['dataset'] == 'enp' and 'language' in ret and ret['language'] == 'deu' and ret['prima_id'] not in ENP_DEU_IDS:
        print("Prima ID not in enp_deu.ids: %s" % ret)
        return
    ret['dataset'] += '-'
    ret['dataset'] += 'gt4hist' if is_gt4hist else 'lang'
    return ret

