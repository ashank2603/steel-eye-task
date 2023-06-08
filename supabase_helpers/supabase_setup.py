from dotenv import dotenv_values
from supabase import create_client, Client

config = dotenv_values(".env")

url: str = config["SUPABASE_URL"]
key: str = config["SUPABASE_KEY"]
supabase: Client = create_client(url,key)