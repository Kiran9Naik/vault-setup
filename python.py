import hvac
import os

VAULT_ADDR = os.getenv("VAULT_ADDR")
ROLE_ID = os.getenv("ROLE_ID")
SECRET_ID = os.getenv("SECRET_ID")

client = hvac.Client(
    url=VAULT_ADDR,
    verify=False   # for self-signed cert
)

# ✅ Just call login (no need to capture response)
client.auth.approle.login(
    role_id=ROLE_ID,
    secret_id=SECRET_ID
)

# ✅ Validate auth
if not client.is_authenticated():
    raise Exception("Vault authentication failed")

print("Authenticated successfully!")

# ✅ Read secret
secret = client.secrets.kv.v1.read_secret_version(
    path="kv/secrets"
)

data = secret["data"]["data"]

print("Username:", data["user"])
print("Password:", data["password"])