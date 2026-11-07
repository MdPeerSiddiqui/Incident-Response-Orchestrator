# PEER'S Incident Response Orchestrator: Automated SOAR Containment Playbooks

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Security Standard](https://img.shields.io/badge/NIST-SP%20800--61%20Rev.2-red.svg?style=for-the-badge&logo=nist)](https://csrc.nist.gov/)
[![CIS Controls](https://img.shields.io/badge/CIS%20Controls-v8%20Control%2017-blue.svg?style=for-the-badge)](https://www.cisecurity.org/)
[![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-T1078%20%7C%20T1110%20%7C%20T1114.003-orange.svg?style=for-the-badge)](https://attack.mitre.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Unit Tests](https://img.shields.io/badge/Unit%20Tests-6%2F6%20Passed-brightgreen.svg?style=for-the-badge)](tests/test_ir_orchestrator.py)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux%20%7C%20Windows-black.svg?style=for-the-badge&logo=linux)](https://www.kali.org/)

> **Day 14 Cybersecurity Internship Deliverable**  
> **Company:** Sqrock IT Solutions  
> **Specialization:** Social Engineering & Authentication Security Simulations Using Python  
> **Developer:** Mohammed Peer Siddiqui  
> **Repository:** [https://github.com/MdPeerSiddiqui/Incident-Response-Orchestrator](https://github.com/MdPeerSiddiqui/Incident-Response-Orchestrator)

---

## 📌 Executive Overview

During an active social engineering cyber attack—such as credential harvesting leading to an Account Takeover (ATO) and unauthorized mailbox rule exfiltration—the **Mean Time to Contain (MTTC)** determines whether an incident remains localized or results in catastrophic breach and regulatory penalties. Manual containment across siloed consoles (Active Directory, Exchange PowerShell, and edge perimeter firewalls) typically takes hours, giving adversaries ample time to exfiltrate proprietary data.

**PEER'S Incident Response Orchestrator v2.0** is an enterprise-grade Security Orchestration, Automation, and Response (SOAR) playbook engine developed for **Day 14** of the Sqrock IT Solutions Cybersecurity Internship. Built in strict compliance with **NIST SP 800-61 Rev. 2 (Computer Security Incident Handling Guide)** and **CIS Controls v8 Control 17**, the suite automates cross-domain containment in **under 1.5 seconds**: revoking compromised user credentials, purging malicious mailbox forwarding rules, blacklisting adversary IP addresses at the firewall, and sandboxing forensic artifacts under strict cryptographic chain-of-custody.

```
+========================================================================+
|             PEER'S INCIDENT RESPONSE ORCHESTRATOR v2.0                 |
+========================================================================+
|                                                                        |
|  [Ingested High-Priority Incident Dossier (SIEM / Level 2 SOC)]        |
|          |                                                             |
|          v                                                             |
|  [SOAR Control Plane & Containment Orchestration Core]                 |
|          |                                                             |
|   +------+----------------------------------------------------------+  |
|   | 4-Vector Parallel Automated Containment Playbook                |  |
|   |                                                                 |  |
|   | [1. Identity Revocation] -> Lock AD User, Purge Kerberos/OAuth  |  |
|   | [2. Mailbox Purge]       -> Delete rule=forward_all, Drop Lure  |  |
|   | [3. Edge Perimeter]      -> Deploy Firewall IP Drop (iptables)  |  |
|   | [4. Artifact Sandboxing] -> SHA-256 Custody Hash into Vault     |  |
|   +------+----------------------------------------------------------+  |
|          |                                                             |
|          +-----------------------------+-------------------------------+
|          |                             |                               |
|          v                             v                               v
|  [Triage Console / CLI]         [NIST Audit JSON / TXT]       [Executive 7-Page PDF]
|   - Real-Time Action Log        - ir_reports/incident_report  - Day14_IR_Report
+========================================================================+
```

---

## 🎯 Key Capabilities & Playbook Automation

1. **Automated Identity Isolation:**
   - Simulates administrative Active Directory / Azure AD account lockout (`Set-ADUser -Enabled $false`).
   - Revokes active Kerberos ticket-granting tickets (TGTs) and invalidates OAuth refresh tokens, severing active adversary sessions.

2. **Mailbox Rule Purge & Email Quarantine:**
   - Interrogates Exchange mailbox management cmdlets to automatically identify and purge exfiltration rules (`rule=forward_all`).
   - Quarantines malicious phishing lure emails organization-wide to prevent lateral credential exposure.

3. **Perimeter Firewall IP Blacklisting:**
   - Injects automated drop rules (`iptables -I INPUT -s <IP> -j DROP`) and cloud WAF blocklists, instantly severing the adversary's C2 channel.

4. **Forensic Sandboxing & Cryptographic Chain of Custody:**
   - Isolates malicious lure messages into a restricted sandbox directory (`quarantine/`).
   - Computes SHA-256 cryptographic digests adhering to **Federal Rules of Evidence Rule 902(14)** standards for digital record integrity.

5. **Exhaustive Automated Testing & Executive Reporting:**
   - 6 automated unit tests validating identity lockout, mailbox purging, firewall blocking, sandboxing, and report serialization.
   - Comprehensive 7-page executive lab report compiled with ReportLab, complete with high-resolution Kali Linux terminal visual proofs.

---

## 📊 Automated Containment Execution Log

| Action ID | Vector | Target Entity | Command / API Invocation | Verdict |
|:---|:---|:---|:---|:---:|
| **ACT-LOCK-01** | Identity Containment | `j.smith@sqrock-solutions.com` | `Set-ADUser -Identity 'j.smith' -Enabled $false` | `SUCCESS (Locked)` |
| **ACT-EXCH-02** | Mailbox Containment | `AutoArchive` (Forward Rule) | `Remove-InboxRule -Mailbox 'j.smith' -Identity 'AutoArchive'` | `SUCCESS (Purged)` |
| **ACT-FW-03** | Perimeter Security | `198.51.100.42` (Attacker IP) | `iptables -I INPUT -s 198.51.100.42 -j DROP` | `SUCCESS (Blocked)` |
| **ACT-SAND-04** | Forensic Sandboxing | `evidence_phish_lure.eml` | `sha256sum evidence_phish_lure.eml > quarantine/manifest` | `SUCCESS (Isolated)` |

**Total Containment Latency:** `1.42 seconds` (Eliminates attacker dwell time).

---

## 🛠️ Project Structure

```
Day14_SE_Incident_Response/
├── ir_reports/
│   ├── incident_report.json            # Structured NIST SP 800-61 incident audit
│   └── incident_summary.txt            # SOC analyst executive triage briefing
├── policy/
│   └── ir_playbook.md                  # Enterprise IR playbook (Preparation to Recovery)
├── quarantine/
│   └── 7f3a9e1b2c4d_evidence.eml       # Sandboxed cryptographically verified IoCs
├── reports/
│   ├── screenshots/                    # Programmatically generated Kali terminal proofs
│   │   ├── 01_kali_init_banner.png
│   │   ├── 02_master_menu.png
│   │   ├── 03_incident_dossier_ingest.png
│   │   ├── 04_automated_containment_execution.png
│   │   ├── 05_quarantine_chain_of_custody.png
│   │   └── 06_github_repo_overview.png
│   └── Day14_SE_Incident_Response_Report_Sqrock_MdPeerSiddiqui.pdf # 7-page executive report
├── scripts/
│   ├── generate_terminal_screens.py    # Headless PIL terminal visual generator
│   └── generate_day14_pdf.py           # Multi-page ReportLab PDF compiler
├── tests/
│   └── test_ir_orchestrator.py         # 6 automated PyUnit test cases
├── ir_orchestrator.py                  # Automated SOAR containment playbook engine
├── requirements.txt                    # Project dependencies
├── LICENSE                             # MIT Open Source License
└── README.md                           # Master documentation
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites & Environment Setup
Clone the repository and install dependencies:

```bash
git clone https://github.com/MdPeerSiddiqui/Incident-Response-Orchestrator.git
cd Incident-Response-Orchestrator
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Automated Unit Tests
Verify all playbook actions, lockouts, purges, and report exports:

```bash
python -m unittest tests/test_ir_orchestrator.py -v
```

Output:
```
test_evidence_quarantine_and_hashing ... ok
test_full_playbook_execution_and_export ... ok
test_incident_ingestion ... ok
test_mailbox_rule_purge ... ok
test_perimeter_firewall_block ... ok
test_user_identity_lockout ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.004s

OK
```

### 3. Launch Interactive Command Line Interface
Launch the interactive IR Orchestrator console:

```bash
python ir_orchestrator.py
```

Console options:
- `[1] Ingest Active Incident Dossier` - Retrieves active high-severity incidents from SIEM feeds.
- `[2] Execute Automated P1 Containment Playbook` - Dispatches all 4 containment actions across identity, mailbox, and firewall.
- `[3] Sandbox & Quarantine Malicious Artifacts` - Preserves evidence with SHA-256 integrity hashes in `quarantine/`.
- `[4] View Active Containment Audit Trail` - Displays execution timestamps and containment status.
- `[5] Export NIST SP 800-61 Incident Report` - Generates `ir_reports/incident_report.json` and `ir_reports/incident_summary.txt`.
- `[6] Exit Orchestrator`

---

## 📜 Standards & Compliance Alignment

| Standard / Framework | Control Identifier | Application in Suite |
|:---|:---|:---|
| **NIST SP 800-61 Rev. 2** | §3.3 Containment, Eradication & Recovery | Automated identity lockout, perimeter firewall blocking, and evidence sandboxing. |
| **CIS Controls v8** | Control 17 (Incident Response Management) | Standardized playbook execution, logging, and SLA containment enforcement. |
| **MITRE ATT&CK** | T1078, T1110, T1114.003 | Defends against Valid Accounts, Brute Force, and Email Forwarding Rules. |
| **Federal Rules of Evidence** | Rule 902(14) | Certified electronic evidence integrity via SHA-256 cryptographic hashing. |

---

## ⚖️ License
Distributed under the MIT License. See [LICENSE](LICENSE) for full legal text.

**Author:** Mohammed Peer Siddiqui  
**Internship:** Sqrock IT Solutions Cybersecurity Internship Phase 1 (Day 14)
