DATASETS = ['enp', 'impact']

ENGINES = ['dinglehopper', 'ocrevalCER', 'ocrevalUAtion', 'ocrevalWER', 'primaWER', 'primaCER', 'primaBoW']

LANGUAGES = ['deu', 'eng', 'fra', 'est', 'fin', 'lav', 'nld', 'pol', 'swe']

# TODO
ENP_IDS = ''
# with open('enp_ids_triple_checked_and_valid.txt', 'r', encoding='utf-8') as f:
    # ENP_IDS = f.read()

# TODO
ENP_DEU_IDS = ''
# with open('enp_deu.ids', 'r', encoding='utf-8') as f:
#     ENP_DEU_IDS = f.read()

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


TEMP_FIELDNAMES = [
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
