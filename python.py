import hvac
import os

VAULT_ADDR = os.getenv("VAULT_ADDR")
ROLE_ID = os.getenv("ROLE_ID")
SECRET_ID = os.getenv("SECRET_ID")

client = hvac.Client(url=VAULT_ADDR)

# Authenticate using AppRole
auth_response = client.auth.approle.login(
    role_id=ROLE_ID,
    secret_id=SECRET_ID
)

if not client.is_authenticated():
    raise Exception("Vault authentication failed")

print("Authenticated successfully!")

# Read secret
secret = client.secrets.kv.v2.read_secret_version(
    path="myapp"
)

data = secret["data"]["data"]

print("Username:", data["username"])
print("Password:", data["password"])