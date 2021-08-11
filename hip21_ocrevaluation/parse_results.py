from json import load
from re import search
from click import argument, group, option
from .utils import get_csv_reader, get_csv_writer

languages = ['deu', 'eng', 'fra', 'est', 'fin', 'lav', 'nld', 'pol', 'swe']

with open('enp_ids_triple_checked_and_valid.txt', 'r', encoding='utf-8') as f:
    ENP_IDS = f.read()

with open('enp_deu.ids', 'r', encoding='utf-8') as f:
    ENP_DEU_IDS = f.read()

def classify_filename(fname):
    ret = {}
    ret['prima_id'] = search(r'([0-9]{8})', fname).group(1)
    is_gt4hist = 'gt4hist' in fname or 'g4hist' in fname
    if not is_gt4hist:
        try:
            lang = next(lang for lang in languages if f'.{lang}' in fname)
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

@group()
def cli():
    pass

@cli.command('ocreval-cer')
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

@cli.command('ocreval-wer')
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

@cli.command('dinglehopper')
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

@cli.command('ocrevaluation')
@argument('out_filename')
@argument('report_filenames', nargs=-1)
def parse_ocrevalUAtion(out_filename, report_filenames):
    with get_csv_writer(out_filename) as writer:
        for n, report_filename in enumerate(report_filenames):
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

@cli.command('ocrconf')
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

@cli.command('layouteval')
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
                    # TODO choose the right values
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

@cli.command('texteval')
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

if __name__ == "__main__":
    cli()
