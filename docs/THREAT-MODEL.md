# Threat Model: Child Content Guardian

## 1. Introduction
The Child Content Guardian is a local AI-powered filtering system designed to protect children from harmful online content. Because it operates on the user's local machine and handles sensitive browsing data, security and privacy are paramount.

## 2. Attacker Profiles
- **The Tech-Savvy Child**: Attempts to bypass the filter using proxies, VPNs, Incognito mode, or editing local configuration files.
- **Malicious Website**: Attempts to bypass the AI classifiers using adversarial perturbations (e.g., invisible characters, skewed images) or "cloaking" content from the extension.
- **Malicious Software**: Tries to compromise the local database or modify the allowlist to grant access to harmful sites.

## 3. Abuse Scenarios
- **Filter Bypass via DNS/VPN**: The child uses a VPN to bypass network-level filters, though this system operates at the browser/API level, mitigating some network bypasses.
- **Adversarial AI Attacks**: Using "jailbreak" prompts or specifically crafted images that confuse the model but remain harmful to humans.
- **Database Tampering**: Direct manipulation of guardian.db to delete event logs or add harmful domains to the allowlist.

## 4. Privacy Risks
- **Data Leakage**: If the local database is not encrypted, other users of the machine can see the child's browsing history.
- **Over-Collection**: Collecting too much metadata from the browser can create a privacy risk if the machine is compromised.

## 5. Mitigations
- **Local-Only Processing**: No content data ever leaves the local machine.
- **Encrypted Storage**: Use SQLCipher for the SQLite database (Phase 1).
- **Robust Decision Engine**: Use ensemble voting (multiple models) to reduce the success rate of single-model adversarial attacks.
- **Integrity Checks**: Periodically verify the integrity of the threshold configuration.
