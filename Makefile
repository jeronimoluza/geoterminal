setup:
    pip install -r requirements.txt

test:
    pytest tests/

clean:
    find . -name "*.pyc" -delete
