import psycopg2
try:
    conn = psycopg2.connect("postgresql://postgres.ivajdrrrjktuarovumbd:ryoiki_tenkai__nehan_no_roka@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres")
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")