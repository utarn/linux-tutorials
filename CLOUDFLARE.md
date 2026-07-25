# Cloudflare Tunnel (cloudflared) — install, configure, publish HTTP

Expose an HTTP service running on a Linux host (or a Windows host) to the Internet through a Cloudflare Zero Trust tunnel. No inbound ports to open on the host — the connector dials out to Cloudflare, and Cloudflare fronts the public hostname.

**Terminology** (current Cloudflare docs): a **connector** is the `cloudflared` daemon you install and run on the origin — it is the process that dials out to Cloudflare. A **tunnel** is the persistent logical object (identified by a **tunnel UUID / tunnel ID**) that the connector connects to; one tunnel can be served by multiple connectors (called **replicas**) for redundancy. The **tunnel token** (`eyJ...`) authenticates a connector to its tunnel. The dashboard menu is still **Networking → Tunnels**; the "installation command" it shows is the connector install command, which embeds the tunnel token.

Flow: install the connector (`cloudflared`) → create a remotely-managed tunnel in the Zero Trust dashboard → copy the connector install command (it contains the **tunnel token**) → run the connector on the host → add a public-hostname route whose **Service URL** points at the local HTTP service → Cloudflare creates the DNS record automatically.

> The host only needs **outbound** access to Cloudflare on port `7844` (QUIC/HTTP-2). Verify before you start if the host sits behind a restrictive firewall.

## 1. Install the connector (cloudflared)

### Linux (Debian / Ubuntu) — Cloudflare apt repo

```bash
# Import the Cloudflare package signing key
sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg \
  | sudo tee /usr/share/keyrings/cloudflare-warp.asc >/dev/null

# Add the repo and install
echo 'deb [signed-by=/usr/share/keyrings/cloudflare-warp.asc] https://pkg.cloudflare.com/cloudflared any main' \
  | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt-get update && sudo apt-get install cloudflared

cloudflared --version
```

### Linux (RHEL / CentOS / Fedora) — rpm repo

```bash
curl -fsSL https://pkg.cloudflare.com/cloudflared.repo | sudo tee /etc/yum.repos.d/cloudflared.repo
sudo yum install cloudflared      # or: sudo dnf install cloudflared
cloudflared --version
```

### Linux — direct binary (any distro, amd64)

```bash
# Download the latest .deb from GitHub releases and install, or run the raw binary:
curl -fsSL -o cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared
sudo mv cloudflared /usr/local/bin/
cloudflared --version
```

Other Linux arches (arm64, arm, 386) and `.deb`/`.rpm` packages are on the [releases page](https://github.com/cloudflare/cloudflared/releases/latest).

### Windows

Download the [latest `cloudflared-windows-amd64.msi`](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.msi) from GitHub and run it, or install silently from PowerShell (run as Administrator):

```powershell
Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.msi" -OutFile "$env:TEMP\cloudflared.msi"
Start-Process msiexec.exe -ArgumentList '/i', "$env:TEMP\cloudflared.msi", '/quiet' -Wait
& "C:\Program Files (x86)\cloudflared\cloudflared.exe" --version
```

> `cloudflared` on Windows does **not** auto-update. Re-run the MSI to upgrade.

## 2. Create the tunnel in the Zero Trust dashboard

1. Log in to the [Cloudflare dashboard](https://dash.cloudflare.com/) → **Zero Trust** → **Networks** → **Tunnels** → **Create a tunnel**. (Direct link: <https://dash.cloudflare.com/?to=/:account/tunnels>)
2. Pick **Cloudflare Tunnel**.
3. Enter a tunnel name (e.g. `linux-edge-01`) and select **Create tunnel**.
4. Choose your OS (**Linux** or **Windows**). The dashboard shows an installation command — copy it. It looks like:

   ```bash
   cloudflared service install eyJhIjoi...long-token-string...==
   ```

   The `eyJ...` string is the **tunnel token**. Anyone who has it can run this tunnel, so treat it like a credential.

5. Run that command on the host (see step 4). The tunnel's status flips to **Healthy** once the connector connects back. Select **Continue**.

## 3. Obtain the tunnel token and tunnel ID

The **tunnel token** (`eyJ...`) authenticates the connector to its tunnel — it is all a remotely-managed tunnel needs to run. The **tunnel ID** (a UUID) identifies the tunnel itself and appears in the `cfargotunnel.com` CNAME and the API.

### From the dashboard

- **Token**: open the tunnel → **Overview** tab → **Add a replica** (or **Refresh token**) → copy the `eyJ...` string out of the connector install command.
- **Tunnel ID**: the tunnel's row in **Networks → Tunnels** shows its UUID; the detail page's **Overview** tab lists it too.

### From the API

```bash
# Account ID: dashboard → any domain → right sidebar "Account ID"
# Tunnel ID: from the dashboard (above)
# API token: My Profile → API Tokens → Create Token (permissions below)

curl "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/cfd_tunnel/$TUNNEL_ID/token" \
  --request GET \
  --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

The `result` field is the token string.

## 4. Run the connector (with the token)

You don't need a `config.yml` for a remotely-managed tunnel — the dashboard stores the config and pushes it to the connector.

### Linux — run directly (foreground, for testing)

```bash
cloudflared tunnel --token eyJhIjoi... run
```

### Linux — run the connector as a systemd service

```bash
# The connector install command from the dashboard already does this; to do it manually:
sudo cloudflared service install eyJhIjoi...long-token-string...==
sudo systemctl enable --now cloudflared
systemctl status cloudflared
```

To restart after a config change: `sudo systemctl restart cloudflared`.

### Windows — run the connector as a Windows service (Administrator CMD or PowerShell)

```powershell
# The dashboard's Windows connector install command installs the service with the token:
& "C:\Program Files (x86)\cloudflared\cloudflared.exe" service install eyJhIjoi...long-token-string...==
sc start cloudflared
sc query cloudflared
```

## 5. Publish HTTP from the Linux host

Add a **public-hostname route** to the tunnel — this maps an Internet-facing hostname to a service on the host.

1. Dashboard → **Networks → Tunnels** → your tunnel → **Public Hostname** tab → **Add a public hostname**.
2. Fill in:
   - **Subdomain**: e.g. `app`
   - **Domain**: pick your Cloudflare-managed zone, e.g. `mydomain.com`
   - **Path**: leave blank unless you want to scope to a path
   - **Service** → **Type**: `HTTP`
   - **URL**: the address of the service **on the host**. This is where you set the IP/port of the thing you are publishing. Examples:
     - `localhost:8080` — a service running on the host itself
     - `127.0.0.1:80` — same, explicit loopback
     - `10.0.0.5:8080` — a service on a private host the tunnel host can reach
     - For HTTPS origins: Type `HTTPS`, URL `10.0.0.5:443`, and toggle **TLS → No TLS Verify** if the origin uses a self-signed cert.
3. **Save**.

Cloudflare now publishes `https://app.mydomain.com` → your local `http://localhost:8080`. Cloudflare terminates TLS at the edge; the leg between `cloudflared` and your origin is HTTP on the private network.

The DNS record for `app.mydomain.com` is created automatically as a **CNAME** → `<tunnel-id>.cfargotunnel.com`. You do **not** create it by hand and it is **not** an A record (see next section).

## 6. DNS — the tunnel uses a CNAME, not an A record

For a public-hostname tunnel route, Cloudflare creates:

```
app.mydomain.com.   CNAME   <tunnel-id>.cfargotunnel.com.
```

The traffic lands on Cloudflare's edge IPs, not on the tunnel host's IP — that's the point of a tunnel. **There is no A record pointing at your host for the published hostname.** Don't create one; an A record would shadow/break the CNAME.

Where an **A record** does come in (and where the "set IP address" part of this lives):

- **Origin / Service URL** (step 5): you set the *internal* IP of the service you are publishing, e.g. `http://10.0.0.5:8080`. This is the address `cloudflared` dials on the private network — it is not a DNS record, it is the route's Service URL.
- **A real A record for a different hostname** (e.g. a non-tunnel host you point at a public IP): create it under **Websites → your domain → DNS → Records → Add record → A**, with the host name and its IPv4 address. That record needs **DNS → Edit** permission (below) and is independent of the tunnel.

If you do want `cloudflared` itself to manage DNS for the tunnel hostname via the CLI (`cloudflared tunnel route dns <tunnel> app.mydomain.com`), it still creates a **CNAME**, and the API token must have **DNS Edit** on that zone.

## 7. Required permissions

Two permission contexts: running the connector (token-based, dashboard flow) vs. managing tunnels via API/CLI (API token with the right scopes).

### To run the connector (Zero Trust tunnel, dashboard-managed)

| What | How | Who needs it |
|---|---|---|
| Run the connector (`cloudflared`) | Just the **tunnel token** (`eyJ...`) | Anyone with the token can run this tunnel — store it as a secret. |

No API token, no `cert.pem`, no zone-level role needed on the host. The token is scoped to this one tunnel.

### To create / read / rotate the tunnel token via API

An **API token** (My Profile → API Tokens → Create Token) with at least one of:

- `Cloudflare One Connectors — Write`, **or**
- `Cloudflare One Connector: cloudflared — Write`, **or**
- `Cloudflare Tunnel — Write`

(Account-level permission.)

### To create the tunnel and its DNS route via CLI / API token

Create a custom token under **My Profile → API Tokens → Create Token → Custom token** with:

| Permission | Level | Needed for |
|---|---|---|
| **Account → Cloudflare Tunnel — Edit** | Account | Create / delete / route the tunnel, `cloudflared tunnel create`, `cloudflared tunnel route dns` |
| **Zone → DNS — Edit** | Zone (the published zone) | Create the CNAME for the public hostname (auto, when adding the route in the dashboard, or via `cloudflared tunnel route dns`) |
| **Zone → Zone — Read** | Zone (the published zone) | List the zone when wiring DNS via CLI |
| *(optional)* **Account → Access — Apps and Policies — Edit** | Account | If you also put a Cloudflare Access policy in front of the published URL |

> `cloudflared tunnel login` (the legacy locally-managed flow that writes `cert.pem`) needs the same account + DNS + Load Balancer member roles, and grants account-wide tunnel management — prefer the dashboard token flow unless you specifically want a local `cert.pem`.

### Minimum for "publish HTTP from this Linux host" (dashboard flow)

You don't need any API token at all on the host. The dashboard creates the tunnel, the CNAME, and the route; you only copy the tunnel token onto the host (it installs the connector). The permissions above only matter if you are scripting tunnel creation or DNS from the CLI/API.

## Reference

- Downloads / install: <https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/>
- Create a tunnel (dashboard): <https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/create-remote-tunnel/>
- Tunnel permissions (token vs API token): <https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/configure-tunnels/remote-tunnel-permissions/>
- Run as a service — Linux: <https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/local-management/as-a-service/linux/>
- Run as a service — Windows: <https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/local-management/as-a-service/windows/>
