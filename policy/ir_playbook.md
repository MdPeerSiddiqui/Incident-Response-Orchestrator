# Enterprise Social Engineering Incident Response Playbook
**Framework:** NIST SP 800-61 Rev. 2 (Computer Security Incident Handling Guide)  
**Standard:** ISO/IEC 27035 / CIS Controls v8 (Control 17 - Incident Response Management)  
**Organization:** Sqrock IT Solutions  
**Author:** Mohammed Peer Siddiqui  

---

## 1. Phase 1: Preparation
- **Tooling:** Automated SOAR incident orchestrator (`ir_orchestrator.py`).
- **Telemetry Sources:** SIEM alerts, Secure Email Gateway (SEG), EDR agents, Active Directory logs.
- **Access Controls:** Least privilege API tokens for AD account manipulation, firewall API access, and M365 security cmdlets.

---

## 2. Phase 2: Detection & Analysis
- **Trigger Events:**
  - Severity P1: Active Credential Compromise / Account Takeover (ATO) with external exfiltration rule.
  - Severity P2: Targeted Spear Phishing lure with confirmed payload execution or credential entry.
  - Severity P3: Reconnaissance probes / unsuccessful password spraying.
- **Triage Protocol:**
  - Extract Indicators of Compromise (IoCs): Sender domain, external forward address, source IP, attachment hashes.
  - Determine blast radius: Identify all recipients, impacted endpoints, and active tokens.

---

## 3. Phase 3: Containment, Eradication & Recovery
- **Step 3.1: Identity Isolation**
  - Revoke all active Kerberos, OAuth 2.0, and SAML refresh tokens.
  - Apply immediate administrative account lockout (`Set-ADUser -Enabled $false`).
- **Step 3.2: Messaging & Data Exfiltration Containment**
  - Scan and purge all inbox auto-forwarding rules (`Remove-InboxRule`).
  - Quarantine malicious email message IDs across all mailboxes organization-wide.
- **Step 3.3: Network Perimeter Containment**
  - Push drop rules for attacker IP addresses to edge firewalls.
  - Blacklist adversarial domains and C2 URLs on DNS resolvers and Secure Web Gateways (SWG).
- **Step 3.4: Evidence Preservation & Sandboxing**
  - Export raw email headers, message bodies, and telemetry logs into encrypted forensic storage (`quarantine/`).
  - Compute SHA-256 cryptographic hashes for chain of custody.

---

## 4. Phase 4: Post-Incident Activity
- Conduct Lessons Learned debrief within 72 hours.
- Incorporate novel lure vectors into employee awareness training simulation banks (Day 11 suite).
- Generate executive compliance audit and export to SIEM archival storage.
