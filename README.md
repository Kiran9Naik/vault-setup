🔐 Vault + CI/CD Integration (AppRole + GitHub Actions)

This project demonstrates a production-aligned secret delivery workflow using HashiCorp Vault integrated with a CI/CD pipeline.

The focus is not just running Vault, but securely consuming secrets inside pipelines without exposing credentials.

🚀 Architecture Overview
Vault (Raft + TLS enabled)
KV Secret Engine (v1)
AppRole Authentication
Python (hvac) client
GitHub Actions pipeline

👉 Secrets are fetched dynamically at runtime, not stored in code or pipeline.

⚙️ Prerequisites
Vault installed and running
TLS configured (self-signed or CA-based)
Python 3.x
GitHub repository
🏗️ Step 1: Vault Configuration
Enable AppRole
vault auth enable approle
Create Policy
# policy.hcl
path "kv/secrets" {
  capabilities = ["read"]
}

path "kv/secrets/*" {
  capabilities = ["read"]
}

Apply:

vault policy write myapp-policy policy.hcl
Create AppRole
vault write auth/approle/role/myapp-role \
    token_policies="myapp-policy" \
    token_ttl=1h \
    token_max_ttl=4h
Get Role ID & Secret ID
vault read auth/approle/role/myapp-role/role-id

vault write -f auth/approle/role/myapp-role/secret-id

👉 Save:

ROLE_ID
SECRET_ID
🔐 Step 2: Store Secret (KV v1)
vault kv put kv/secrets user="kiran" password="naik"

Verify:

vault kv get kv/secrets
🐍 Step 3: Python Application

Install dependency:

pip install hvac
python.py
import hvac
import os

VAULT_ADDR = os.getenv("VAULT_ADDR")
ROLE_ID = os.getenv("ROLE_ID")
SECRET_ID = os.getenv("SECRET_ID")

client = hvac.Client(
    url=VAULT_ADDR,
    verify=False  # For self-signed cert (PoC)
)

# Authenticate using AppRole
client.auth.approle.login(
    role_id=ROLE_ID,
    secret_id=SECRET_ID
)

if not client.is_authenticated():
    raise Exception("Vault authentication failed")

print("Authenticated successfully!")

# Read secret from KV v1
secret = client.secrets.kv.v1.read_secret(
    path="secrets",
    mount_point="kv"
)

data = secret["data"]

print("User:", data["user"])
print("Password:", data["password"])
⚙️ Step 4: GitHub Actions Pipeline
Add Secrets in GitHub

Go to:
Repo → Settings → Secrets

Add:

VAULT_ADDR
ROLE_ID
SECRET_ID
Workflow File

.github/workflows/vault.yml

name: Vault Integration

on:
  push:
    branches: [ "main" ]

jobs:
  vault-job:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: pip install hvac

    - name: Run Python script
      env:
        VAULT_ADDR: ${{ secrets.VAULT_ADDR }}
        ROLE_ID: ${{ secrets.ROLE_ID }}
        SECRET_ID: ${{ secrets.SECRET_ID }}
      run: python python.py
⚠️ Common Issues & Fixes
❌ Using /ui in VAULT_ADDR
https://IP:8200/ui   ❌
https://IP:8200      ✅
❌ SSL Certificate Error
SSLCertVerificationError

✔ Fix:

verify=False  # for testing

✔ Production:

Use CA cert or trusted certificate
❌ AppRole Login Failure
permission denied

✔ Fix:

Regenerate SECRET_ID
Ensure policy attached
Verify role exists
❌ KV v1 vs v2 mismatch
Engine	API Path
KV v1	kv/secrets
KV v2	kv/data/secrets
🔍 Debugging Approach

Always validate in order:

Vault CLI
vault write auth/approle/login ...
API
curl -k https://IP:8200/v1/...
Python
CI Pipeline
📈 Production Considerations
Replace verify=False with CA validation
Rotate SECRET_ID regularly
Use short TTL tokens
Restrict policies to least privilege
🚀 Future Improvements
AppRole → OIDC (GitHub → Vault)
KV v1 → KV v2 (versioning support)
Direct API → Vault Agent / Injector (Kubernetes)
💡 Key Takeaway

Vault setup is just the beginning.

👉 The real value lies in:

Secure authentication
Runtime secret retrieval
CI/CD integration without exposure
🧑‍💻 Author

KiranNaik Bukke
Devops Engineer Engineer | DevOps | Cloud | Security