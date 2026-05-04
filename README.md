# vault-setup

Vault HA Cluster on GCP (2-Node with Auto-Unseal)
📌 Overview

This project demonstrates setting up a 2-node HA Vault cluster using:

HashiCorp Vault
Google Cloud Platform
Terraform (for infra)
Raft storage (integrated storage)
GCP KMS (auto-unseal)
Internal + External TCP Load Balancer
🏗 Architecture
Client
   ↓
External TCP Load Balancer (Public IP:8200)
   ↓
Internal TCP Load Balancer
   ↓
Vault Node 1 (Active)
Vault Node 2 (Standby)
⚙️ Prerequisites
GCP project
gcloud CLI configured
Terraform installed
SSH access to VM
🚀 Step 1: Infrastructure Setup (Terraform)

Create:

VPC
Subnet
Firewall rules
2 VM instances

Example:

resource "google_compute_instance" "vault" {
  count        = 2
  name         = "vault-instance-${count.index}"
  machine_type = "e2-medium"
}
🔐 Step 2: Install Vault
sudo apt update
sudo apt install vault -y

Verify:

vault version
🔑 Step 3: Create TLS Certificates
openssl req -x509 -nodes -days 365 \
-newkey rsa:2048 \
-keyout vault-key.pem \
-out vault-cert.pem

Move to:

/opt/vault/tls/
🔒 Step 4: Configure Vault

/etc/vault.d/vault.hcl

disable_mlock = true
ui = true

storage "raft" {
  path    = "/opt/vault/data"
  node_id = "node-1"
}

listener "tcp" {
  address         = "0.0.0.0:8200"
  cluster_address = "0.0.0.0:8201"

  tls_cert_file = "/opt/vault/tls/vault-cert.pem"
  tls_key_file  = "/opt/vault/tls/vault-key.pem"
}

seal "gcpckms" {
  project     = "PROJECT_ID"
  region      = "global"
  key_ring    = "vault-keyring"
  crypto_key  = "vault-key"
  credentials = "/opt/vault/creds/gcp.json"
}
🔑 Step 5: Setup GCP KMS Auto-Unseal
Create key ring
Create crypto key
Create service account
Download JSON key

Place:

/opt/vault/creds/gcp.json
▶️ Step 6: Start Vault
sudo systemctl start vault
sudo systemctl enable vault
🔐 Step 7: Initialize Vault
export VAULT_ADDR=https://127.0.0.1:8200
export VAULT_SKIP_VERIFY=true

vault operator init
🔗 Step 8: Join Node 2
vault operator raft join https://NODE1_IP:8200
⚖️ Step 9: Load Balancer Setup
❗ Important

Use TCP Load Balancer (Layer 4)

Internal LB
Type: Internal TCP
Port: 8200
External LB
Type: External TCP
Port: 8200
🌐 Step 10: Access Vault UI
https://<EXTERNAL_LB_IP>:8200/ui/
🧪 Health Check
curl -k https://<LB_IP>:8200/v1/sys/health
⚠️ Key Learnings
Vault requires TCP Load Balancer
HTTP LB breaks Vault due to TLS termination
Internal LB is not publicly accessible
TLS SAN is critical for browser access
Auto-unseal still requires initial vault operator init
