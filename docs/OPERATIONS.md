# Operations playbook — docs.rousseau-agent.com

Recovery runbook for the docs site when something is on fire. Kept
short and specific so a call at 3 a.m. isn't the wrong time to learn
how the pipeline works.

## Live health check

```bash
# Should return HTTP 200 from a GitHub Pages IP (185.199.108–111.153).
curl -sI https://rousseau-agent.com/ | head -3

# Should return HTTP 200 and content-type: text/css.
curl -sI https://rousseau-agent.com/_csp/52e1d65d13dabc2f.css | head -3
```

If either returns 4xx/5xx, jump to the matching section below.

## The DNS + TLS chain

```
rousseau-agent.com (A record)
        ↓
185.199.{108-111}.153   ← GitHub Pages static IPs
        ↓
GitHub Pages serves the site with a Let's Encrypt cert issued to
rousseau-agent.com AND www.rousseau-agent.com.
```

The GitHub Pages cert state is queryable:

```bash
gh api repos/sebastienrousseau/rousseau-agent.github.io/pages \
  --jq '{cname, https_certificate, https_enforced}'
```

`https_certificate.state` must be `"approved"` and `expires_at` at
least 30 days out.

## Symptom → likely cause map

| Symptom | Likely cause | First-line fix |
| :--- | :--- | :--- |
| `HTTP 526` (Cloudflare origin SSL) | Cloudflare proxy is on and cert is missing on origin | Grey-cloud (DNS-only) the `A` records for rousseau-agent.com; wait 60 s. |
| `HTTP 404` on `/` | GH Pages CNAME lost | Re-run the `deploy` workflow; the `public/CNAME` step re-writes the file every build. |
| `HTTP 404` on CSS/JS but 200 on HTML | `BASE_PATH` env accidentally set at build time | Confirm `.github/workflows/deploy.yml` build step has **no** `BASE_PATH` env — the apply-base-path pass no-ops on empty. |
| Site loads but only landing page — every other route 404 | GH Pages fell back to root only | Check the artefact upload step succeeded; look at the `deploy` action's Pages summary. |
| Custom domain de-configured in Pages settings | Auto-reconfigure on domain change | Re-run deploy; the `public/CNAME` write restores the binding. |

## Recovery: HTTP 526

The failure mode is Cloudflare-to-origin TLS handshake. Two ways out:

1. **Grey-cloud the DNS records** (safest — no cert dance):
   In Cloudflare → DNS → `rousseau-agent.com` → click the orange
   cloud on the `A` records to turn it grey. Traffic now goes
   directly to GH Pages IPs; the GH Pages Let's Encrypt cert is
   used end-to-end.

2. **Full (strict) SSL on Cloudflare**:
   If the proxy must stay orange (e.g. to keep a Worker in the
   path), Cloudflare → SSL/TLS → Overview must be **Full (strict)**.
   That way CF's origin fetch validates the GH Pages cert.

## Recovery: CSS / assets 404

Root cause is almost always a stale `BASE_PATH` prefix. Verify:

```bash
curl -s https://rousseau-agent.com/ | grep -oE 'href="[^"]*\.css"' | head
```

Every path must start with `/`, not `/rousseau-agent.github.io/`.
If the prefix is present, someone put `BASE_PATH` back in
`.github/workflows/deploy.yml`. Remove it, push, wait ~2 min.

## Recovery: CNAME lost

If the custom domain gets un-set in GH Pages (Settings → Pages), the
CI-side fix ensures it's set on the next deploy:

```yaml
- name: Write CNAME for the custom domain
  run: echo 'rousseau-agent.com' > public/CNAME
```

Runs on every push to `main`. To force it now, push an empty commit:

```bash
git commit --allow-empty -m "chore: re-trigger deploy for CNAME"
git push origin main
```

## Cert renewal

Let's Encrypt certs issued to GH Pages custom domains are
auto-renewed. You'll see it flip in the API response's
`https_certificate.expires_at`. Nothing to do until it stops
happening.

## Escalation

If nothing above helps:

1. Check <https://www.githubstatus.com> — the Pages service can go
   down.
2. Roll back to the last-known-good commit on `main` and force a
   deploy: `git revert <bad-commit> && git push origin main`.
3. As a last resort, temporarily grey-cloud in Cloudflare so
   Cloudflare drops out of the path entirely — the site will still
   resolve at rousseau-agent.com via the direct GH Pages A records.
