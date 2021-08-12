from pathlib import Path
from json import load
from re import search

from click import argument, group, option

from .constants import ENGINES, DATASETS, ENP_IDS
from .utils import get_csv_reader, get_csv_writer, classify_filename
from .evaldb import EvalDB


@group()
def cli():
    pass

@cli.group('parse')
def cli_parse():
    """
    Parse the evaluation results into consistent CSV
    """

@cli_parse.command('ocrevalCER')
@argument('out_filename')
@argument('report_filenames', nargs=-1)
def parse_ocreval_cer(out_filename, report_filenames):
    """
    Parse all the CER REPORT_FILENAMES and output a row each in OUT_FILENAME
    """
    with get_csv_writer(out_filename) as writer:
        for report_filename in report_filenames:
            row = classify_filename(report_filename)
            if not row:
                continue
            with open(report_filename, 'r', encoding='utf-8') as f_in:
                lines = [x.strip() for x in f_in.readlines()]
                row['chars_total'] = int(lines[2].split(' ')[0])
                row['chars_wrong'] = int(lines[3].split(' ')[0])
                row['CER'] = row['chars_wrong'] / max(row['chars_total'], 1)
                writer.writerow(row)

@cli_parse.command('ocrevalWER')
@argument('out_filename')
@argument('report_filenames', nargs=-1)
def parse_ocreval_wer(out_filename, report_filenames):
    """
    Parse all the WER REPORT_FILENAMES and output a row each in OUT_FILENAME
    """
    with get_csv_writer(out_filename) as writer:
        for report_filename in report_filenames:
            row = classify_filename(report_filename)
            if not row:
                continue
            with open(report_filename, 'r', encoding='utf-8') as f_in:
                lines = [x.strip() for x in f_in.readlines()]
                row['words_total'] = int(lines[2].split(' ')[0])
                row['words_wrong'] = int(lines[3].split(' ')[0])
                row['WER'] = row['words_wrong'] / max(row['words_total'], 1)
                writer.writerow(row)

@cli_parse.command('dinglehopper')
@argument('out_filename')
@argument('report_filenames', nargs=-1)
def parse_dinglehopper_json(out_filename, report_filenames):
    """
    Parse all the WER REPORT_FILENAMES and output a row each in OUT_FILENAME
    """
    with get_csv_writer(out_filename) as writer:
        for report_filename in report_filenames:
            row = classify_filename(report_filename)
            if not row:
                continue
            with open(report_filename, 'r') as f:
                report = load(f)
                row['CER'] = report['cer']
                row['WER'] = report['wer']
                row['words_total'] = report['n_words']
                row['chars_total'] = report['n_characters']
                writer.writerow(row)

@cli_parse.command('ocrevalUAtion')
@argument('out_filename')
@argument('report_filenames', nargs=-1)
def parse_ocrevalUAtion(out_filename, report_filenames):
    with get_csv_writer(out_filename) as writer:
        for _, report_filename in enumerate(report_filenames):
            row = classify_filename(report_filename)
            if not row:
                continue
            with open(report_filename, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    if '<td>WER</td>' in line:
                        row['WER'] = float(line[16:-6].replace(',', '.')) / 100
                    elif '<td>CER</td>' in line:
                        row['CER'] = float(line[16:-6].replace(',', '.')) / 100
                    elif '<td>WER (order independent)</td>' in line:
                        row['BOW'] = float(line[36:-6].replace(',', '.')) / 100
                writer.writerow(row)

@cli_parse.command('conf')
@argument('out_filename')
@argument('report_filenames', nargs=-1)
def parse_ocrconf(out_filename, report_filenames):
    with get_csv_writer(out_filename) as writer:
        for report_filename in report_filenames:
            row = classify_filename(report_filename)
            if not row:
                continue
            with open(report_filename, 'r', encoding='utf-8') as f:
                text = f.read()
                row['conf'] = 1 - (float(text[text.rindex(' '):]) / 100)
                writer.writerow(row)

@cli_parse.command('LayoutEval')
@argument('out_filename')
@argument('report_filenames', nargs=-1)
def parse_layouteval(out_filename, report_filenames):
    row_in_column = 'overallWeightedAreaSuccessRate'
    with get_csv_writer(out_filename) as writer:
        for report_filename in report_filenames:
            enp_or_impact = 'enp' if 'enp' in report_filename.lower() else 'impact'
            with get_csv_reader(report_filename) as reader:
                for row_in in reader:
                    if not row_in['Ground-Truth'] or 'Error' in row_in['Ground-Truth'] or 'not found' in row_in['Ground-Truth']:
                        if row_in['Ground-Truth']:
                            print(row_in['Ground-Truth'])
                        continue
                    if row_in[row_in_column] == '0':
                        print("Suspiciously, successRate is zero, skipping %s" % row_in['Ground-Truth'])
                        continue
                    row_out_column = 'prima_layout1' if row_in['Profile'] == 'OCRScenario.evx' else \
                                     'prima_layout2' if row_in['Profile'] == 'PageAnalysis.evx' else \
                                     'prima_layout3' if row_in['Profile'] == 'Segmentation.evx' else \
                                     'prima_layout4'
                    row_out = {
                        'prima_id': search(r'\d+', row_in['Ground-Truth']).group(0),
                        'dataset': '%s-%s' % (enp_or_impact, 'gt4hist' if row_in['Method'] == 'gt4hist' else 'lang'),
                        row_out_column: 1 - float(row_in[row_in_column])
                    }
                    if row_out['dataset'] == 'enp-lang' and row_out['prima_id'] not in ENP_IDS:
                        print("Prima ID not in enp_map: %s" % row_out)
                        continue
                    writer.writerow(row_out)

@cli_parse.command('texteval')
@argument('out_filename')
@option('--first-only', is_flag=True, default=False)
@option('--dataset-prefix', default='impact')
@argument('measure')
@argument('report_filenames', nargs=-1)
def parse_texteval(out_filename, first_only, dataset_prefix, measure, report_filenames):
    row_measure = 'wordAccuracy' if measure == 'WER' else \
                  'characterAccuracy' if measure == 'CER' else \
                  'wordIndexMissErrorRate'
    with get_csv_writer(out_filename) as writer:
        for report_filename in report_filenames:
            with get_csv_reader(report_filename) as reader:
                for row_in in reader:
                    row_out = {
                        'prima_id': search(r'\d{3,}', row_in['groundTruth']).group(0),
                        'dataset': '%s-%s' % (dataset_prefix, 'gt4hist' if 'gt4hist' in row_in['result'] else 'lang'),
                        measure: float(row_in[row_measure] or 1)
                    }
                    if row_out['dataset'] == 'enp-lang' and row_out['prima_id'] not in ENP_IDS:
                        print("Prima ID not in enp_map: %s" % row_out)
                        break
                    if measure != 'BOW':
                        row_out[measure] = 1 - row_out[measure]
                    writer.writerow(row_out)
                    if first_only:
                        break

@cli.command('list')
@argument('dataset')
@argument('engine')
def cli_list(dataset, engine):
    """
    List results from ENGINE in DATASET
    """
    if dataset not in DATASETS:
        raise ValueError("Dataset ust be one of %s" % DATASETS)
    if engine not in ENGINES:
        raise ValueError('ENGINE must be one of %s' % ENGINES)

    with get_csv_reader('primaID.csv') as reader:
        ids = [r['primaID'] for r in reader if r['dataset'] == dataset]
        for f in Path('data').iterdir():
            id_, rest = f.name.split('.', 1)
            if id_ not in ids:
                continue
            if '.%s.' % engine not in rest:
                continue
            print(f)

@cli.command('join')
@option('--csv/--excel', default=False, help='Output one CSV per dataset instead of excel')
@argument('fname')
def merge_csv(csv, fname):
    evaldb = EvalDB()
    evaldb.populate()
    getattr(evaldb, 'to_csv' if csv else 'to_excel')(fname)


if __name__ == "__main__":
    cli()
