import argparse

from dotenv import load_dotenv



load_dotenv()

from etl.extract import extract
from etl.transform import transform
from etl.load import load


if __name__ == "__main__":

    TASK_CHOICES = ['extract','transform','load']
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=str, choices=TASK_CHOICES, help="Elige la etapa a ejecutar: extract, transform o load")

    args = parser.parse_args()

    if args.stage is None:
        extract()
        transform()
        load()
    else:
        if args.stage == 'extract':
            extract()
        elif args.stage == 'transform':
            transform()
        elif args.stage == 'load':
            load()