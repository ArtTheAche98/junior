import argparse
import csv
from typing import List, Dict, Any, Callable, Optional
from tabulate import tabulate
import sys


def parse_args():
    parser = argparse.ArgumentParser(description='Process CSV with filter and aggregation.')
    parser.add_argument('file', help='Path to CSV file')
    parser.add_argument('--where', help='Filter condition, e.g. price>100')
    parser.add_argument('--aggregate', help='Aggregation, e.g. price=avg')
    return parser.parse_args()


def read_csv(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def parse_where(where: str):
    if '>=' in where:
        col, val = where.split('>=', 1)
        return col.strip(), '>=', val.strip()
    elif '<=' in where:
        col, val = where.split('<=', 1)
        return col.strip(), '<=', val.strip()
    elif '>' in where:
        col, val = where.split('>', 1)
        return col.strip(), '>', val.strip()
    elif '<' in where:
        col, val = where.split('<', 1)
        return col.strip(), '<', val.strip()
    elif '=' in where:
        col, val = where.split('=', 1)
        return col.strip(), '=', val.strip()
    else:
        raise ValueError('Invalid where condition')


def filter_rows(rows: List[Dict[str, Any]], where: Optional[str]) -> List[Dict[str, Any]]:
    if not where:
        return rows
    col, op, val = parse_where(where)
    def match(row):
        cell = row[col]
        try:
            cell_val = float(cell)
            val_num = float(val)
        except ValueError:
            cell_val = cell
            val_num = val
        if op == '>':
            return cell_val > val_num
        elif op == '<':
            return cell_val < val_num
        elif op == '=':
            return cell_val == val_num
        elif op == '>=':
            return cell_val >= val_num
        elif op == '<=':
            return cell_val <= val_num
        else:
            return False
    return [row for row in rows if match(row)]


def parse_aggregate(aggregate: str):
    if not aggregate or '=' not in aggregate:
        raise ValueError('Invalid aggregate format')
    col, func = aggregate.split('=', 1)
    return col.strip(), func.strip().lower()


def aggregate_column(rows: List[Dict[str, Any]], aggregate: Optional[str]):
    if not aggregate:
        return None
    col, func = parse_aggregate(aggregate)
    values = [float(row[col]) for row in rows]
    if func == 'avg':
        return ('avg', col, sum(values) / len(values) if values else None)
    elif func == 'min':
        return ('min', col, min(values) if values else None)
    elif func == 'max':
        return ('max', col, max(values) if values else None)
    else:
        raise ValueError('Unknown aggregate function')


def main():
    args = parse_args()
    try:
        rows = read_csv(args.file)
    except Exception as e:
        print(f'Error reading file: {e}', file=sys.stderr)
        sys.exit(1)
    rows = filter_rows(rows, args.where)
    if args.aggregate:
        try:
            result = aggregate_column(rows, args.aggregate)
            if result:
                func, col, value = result
                print(f'{func}({col}) = {value}')
        except Exception as e:
            print(f'Error in aggregation: {e}', file=sys.stderr)
            sys.exit(1)
    else:
        print(tabulate(rows, headers='keys', tablefmt='grid'))

if __name__ == '__main__':
    main()

