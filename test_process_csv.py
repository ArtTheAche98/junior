import os
import tempfile
import subprocess
import pytest

CSV_CONTENT = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4
"""

def run_script(args, input_file):
    cmd = ['python3', 'process_csv.py', input_file] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

@pytest.fixture
def csv_file():
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.csv') as f:
        f.write(CSV_CONTENT)
        f.flush()
        yield f.name
    os.remove(f.name)

def test_no_filter(csv_file):
    result = run_script([], csv_file)
    assert 'iphone 15 pro' in result.stdout
    assert 'galaxy s23 ultra' in result.stdout
    assert result.returncode == 0

def test_filter_price_gt(csv_file):
    result = run_script(['--where', 'price>1000'], csv_file)
    assert 'galaxy s23 ultra' in result.stdout
    assert 'iphone 15 pro' not in result.stdout
    assert result.returncode == 0

def test_filter_brand_eq(csv_file):
    result = run_script(['--where', 'brand=xiaomi'], csv_file)
    assert 'redmi note 12' in result.stdout
    assert 'poco x5 pro' in result.stdout
    assert 'iphone 15 pro' not in result.stdout
    assert result.returncode == 0

def test_aggregate_avg(csv_file):
    result = run_script(['--aggregate', 'price=avg'], csv_file)
    assert 'avg(price)' in result.stdout
    assert result.returncode == 0

def test_aggregate_min(csv_file):
    result = run_script(['--aggregate', 'price=min'], csv_file)
    assert 'min(price)' in result.stdout
    assert result.returncode == 0

def test_aggregate_max(csv_file):
    result = run_script(['--aggregate', 'price=max'], csv_file)
    assert 'max(price)' in result.stdout
    assert result.returncode == 0

def test_aggregate_with_filter(csv_file):
    result = run_script(['--where', 'brand=xiaomi', '--aggregate', 'price=max'], csv_file)
    assert 'max(price)' in result.stdout
    assert result.returncode == 0

def test_invalid_file():
    result = run_script([], 'no_such_file.csv')
    assert result.returncode != 0
    assert 'Error reading file' in result.stderr

def test_invalid_aggregate(csv_file):
    result = run_script(['--aggregate', 'price=median'], csv_file)
    assert result.returncode != 0
    assert 'Unknown aggregate function' in result.stderr

