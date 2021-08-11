from csv import DictReader
from click import argument, command
from contextlib import contextmanager
from pathlib import Path

DATASETS = ['enp', 'impact']
ENGINES = ['dinglehopper', 'ocrevalCER', 'ocrevalUAtion', 'ocrevalWER', 'primaWER', 'primaCER', 'primaBoW']

@contextmanager
def get_csv_reader(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        reader = DictReader(f)
        yield reader

@command()
@argument('dataset')
@argument('engine')
def cli(dataset, engine):
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

if __name__ == "__main__":
    cli()
