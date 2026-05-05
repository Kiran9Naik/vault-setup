import hvac
import os

VAULT_ADDR = os.getenv("VAULT_ADDR")
ROLE_ID = os.getenv("ROLE_ID")
SECRET_ID = os.getenv("SECRET_ID")

# 👇 Disable SSL verification (temporary)
client = hvac.Client(
    url=VAULT_ADDR,
    verify=False
)

client.auth.approle.login(
    role_id=ROLE_ID,
    secret_id=SECRET_ID
)

print("Authenticated:", client.is_authenticated())

secret = client.secrets.kv.v2.read_secret_version(
    path="kv/secrets"
)

print(secret["data"]["data"])