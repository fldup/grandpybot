import os

if os.environ.get('GOOGLE_KEY') is None:
    key_value = ''
else:
    key_value = os.environ['GOOGLE_KEY']
