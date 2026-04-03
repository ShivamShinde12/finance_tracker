import urllib.request, json

base = 'http://127.0.0.1:8000'

print('Testing GET /')
try:
    with urllib.request.urlopen(base + '/') as r:
        print('Status:', r.status, 'Response:', r.read().decode())
except Exception as e:
    print('Error:', e)

print('\nTesting GET /summary (analyst role)')
req = urllib.request.Request(base + '/summary', headers={'X-User-Role': 'analyst'})
try:
    with urllib.request.urlopen(req) as r:
        print('Status:', r.status, 'Response:', r.read().decode())
except Exception as e:
    print('Error:', e)

print('\nTesting POST /transactions (admin role)')
data = json.dumps({'amount': 500.0, 'type': 'income', 'category': 'salary', 'date': '2026-04-02', 'notes': 'Monthly salary'}).encode()
req = urllib.request.Request(base + '/transactions', data=data, headers={'Content-Type': 'application/json', 'X-User-Role': 'admin'})
try:
    with urllib.request.urlopen(req) as r:
        print('Status:', r.status, 'Response:', r.read().decode())
except Exception as e:
    print('Error:', e)

print('\nTesting GET /transactions (viewer role)')
req = urllib.request.Request(base + '/transactions', headers={'X-User-Role': 'viewer'})
try:
    with urllib.request.urlopen(req) as r:
        print('Status:', r.status, 'Response:', r.read().decode())
except Exception as e:
    print('Error:', e)

print('\nTesting GET /transactions/3 (viewer role)')
req = urllib.request.Request(base + '/transactions/3', headers={'X-User-Role': 'viewer'})
try:
    with urllib.request.urlopen(req) as r:
        print('Status:', r.status, 'Response:', r.read().decode())
except Exception as e:
    print('Error:', e)