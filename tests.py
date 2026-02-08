'''import psycopg2
try:
    conn = psycopg2.connect("postgresql://postgres.ivajdrrrjktuarovumbd:ryoiki_tenkai__nehan_wa_roka@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres")
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")'''

import secrets, string
prefix = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(7))
secret = secrets.token_urlsafe(32)
full_key = f"vera_{prefix}_{secret}"
print(full_key)