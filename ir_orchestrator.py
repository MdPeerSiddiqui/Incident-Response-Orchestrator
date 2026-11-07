#!/usr/bin/env python3
"""
PEER'S Incident Response Orchestrator - Automated SOAR Playbook Engine
Sqrock IT Solutions - Cybersecurity Internship Phase 1 (Day 14)
Author: Mohammed Peer Siddiqui
License: MIT
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

# Standard Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POLICY_DIR = os.path.join(BASE_DIR, "policy")
REPORTS_DIR = os.path.join(BASE_DIR, "ir_reports")
QUARANTINE_DIR = os.path.join(BASE_DIR, "quarantine")
DEFAULT_INCIDENT_JSON = os.path.join(REPORTS_DIR, "incident_report.json")
DEFAULT_INCIDENT_TXT = os.path.join(REPORTS_DIR, "incident_summary.txt")

os.makedirs(POLICY_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(QUARANTINE_DIR, exist_ok=True)


class IROrchestrator:
    """Enterprise Incident Response SOAR Automation Engine (NIST SP 800-61 Rev.2 compliant)."""

    def __init__(self):
        self.active_incidents = []
        self.containment_log = []
        self.quarantined_artifacts = []

    def load_incident_from_siem(self, siem_report_path=None):
        """Ingest correlated alerts from Day 13 SIEM report or instantiate baseline incidents."""
        if siem_report_path and os.path.exists(siem_report_path):
            with open(siem_report_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for alert in data.get("alerts", []):
                    inc = {
                        "incident_id": f"INC-{alert['alert_id']}",
                        "title": alert["rule_name"],
                        "severity": alert["severity"],
                        "mitre_id": alert["mitre_id"],
                        "mitre_tactic": alert["mitre_tactic"],
                        "affected_user": alert["details"].get("user") or alert["details"].get("mailbox", "unknown"),
                        "attacker_ip": alert["details"].get("attacker_ip") or alert["details"].get("src_ip", "198.51.100.42"),
                        "forward_destination": alert["details"].get("forward_destination", "N/A"),
                        "status": "OPEN",
                        "created_at": datetime.now().isoformat()
                    }
                    self.active_incidents.append(inc)
            return len(self.active_incidents)

        # Baseline standard P1 Incident
        baseline_incident = {
            "incident_id": "INC-2026-1107-P1-ATO",
            "title": "Confirmed Account Takeover & Covert Exfiltration via Auto-Forwarding",
            "severity": "CRITICAL",
            "mitre_id": "T1078 / T1110 / T1114.003",
            "mitre_tactic": "Credential Access -> Persistence -> Exfiltration",
            "affected_user": "j.smith@sqrock-solutions.com",
            "attacker_ip": "198.51.100.42",
            "forward_destination": "attacker-drop@proton.me",
            "status": "OPEN",
            "created_at": datetime.now().isoformat()
        }
        self.active_incidents = [baseline_incident]
        return len(self.active_incidents)

    def lock_user_account(self, user_identity):
        """Simulate Active Directory / Azure AD account lockout and credential revocation."""
        timestamp = datetime.now().isoformat()
        action = {
            "action_id": f"ACT-LOCK-{int(datetime.now().timestamp())}",
            "type": "IDENTITY_CONTAINMENT",
            "target": user_identity,
            "status": "EXECUTED",
            "timestamp": timestamp,
            "details": f"Revoked active Kerberos/OAuth tokens; disabled AD account {user_identity}; enforced mandatory password reset flag."
        }
        self.containment_log.append(action)
        return action

    def purge_mailbox_forwarding(self, mailbox, forward_address):
        """Simulate Exchange PowerShell cmdlet execution to purge exfiltration forwarding rules."""
        timestamp = datetime.now().isoformat()
        action = {
            "action_id": f"ACT-EXCH-{int(datetime.now().timestamp())}",
            "type": "MAILBOX_CONTAINMENT",
            "target": mailbox,
            "status": "EXECUTED",
            "timestamp": timestamp,
            "details": f"Purged forwarding rule targeting {forward_address}; quarantined inbound phishing lures; audited mailbox delegation rights."
        }
        self.containment_log.append(action)
        return action

    def block_network_ip(self, ip_address):
        """Simulate edge firewall and Cloudflare / AWS WAF drop rule deployment."""
        timestamp = datetime.now().isoformat()
        action = {
            "action_id": f"ACT-FW-{int(datetime.now().timestamp())}",
            "type": "NETWORK_PERIMETER_BLOCK",
            "target": ip_address,
            "status": "EXECUTED",
            "timestamp": timestamp,
            "details": f"Injected edge firewall drop rule: iptables -I INPUT -s {ip_address} -j DROP; blacklisted on Cloudflare WAF."
        }
        self.containment_log.append(action)
        return action

    def quarantine_artifact(self, raw_data, artifact_name="phish_lure_payload.eml"):
        """Sandbox and cryptographically hash evidence in strict accordance with chain-of-custody."""
        sha256_hash = hashlib.sha256(raw_data.encode("utf-8")).hexdigest()
        quarantine_file_path = os.path.join(QUARANTINE_DIR, f"{sha256_hash[:12]}_{artifact_name}")
        
        with open(quarantine_file_path, "w", encoding="utf-8") as f:
            f.write(raw_data)

        artifact_record = {
            "artifact_name": artifact_name,
            "sha256": sha256_hash,
            "quarantine_path": quarantine_file_path,
            "quarantined_at": datetime.now().isoformat(),
            "file_size_bytes": len(raw_data)
        }
        self.quarantined_artifacts.append(artifact_record)
        return artifact_record

    def execute_full_playbook(self, incident_index=0):
        """Execute automated NIST SP 800-61 Rev.2 containment workflow for a given incident."""
        if not self.active_incidents:
            self.load_incident_from_siem()

        inc = self.active_incidents[incident_index]
        user = inc.get("affected_user", "j.smith@sqrock-solutions.com")
        attacker_ip = inc.get("attacker_ip", "198.51.100.42")
        fwd_dest = inc.get("forward_destination", "attacker-drop@proton.me")

        # 1. Lock Account
        act_lock = self.lock_user_account(user)

        # 2. Purge Mailbox
        act_mail = self.purge_mailbox_forwarding(user, fwd_dest)

        # 3. Block IP
        act_net = self.block_network_ip(attacker_ip)

        # 4. Quarantine Artifact
        evidence_content = (
            f"From: payroll-update@sqrock-portal.com\n"
            f"To: {user}\n"
            f"Subject: Urgent: Verify Direct Deposit Details\n"
            f"X-Originating-IP: {attacker_ip}\n"
            f"X-Forward-Target: {fwd_dest}\n"
            f"Body: Action required immediately to avoid payroll cancellation.\n"
        )
        art = self.quarantine_artifact(evidence_content, "evidence_phish_lure.eml")

        inc["status"] = "CONTAINED"
        inc["containment_timestamp"] = datetime.now().isoformat()
        inc["executed_actions"] = [act_lock["action_id"], act_mail["action_id"], act_net["action_id"]]
        inc["quarantined_sha256"] = art["sha256"]

        return {
            "incident": inc,
            "actions": [act_lock, act_mail, act_net],
            "quarantined_artifact": art
        }

    def export_reports(self, json_path=DEFAULT_INCIDENT_JSON, txt_path=DEFAULT_INCIDENT_TXT):
        """Export comprehensive incident response audit dossiers."""
        report = {
            "metadata": {
                "organization": "Sqrock IT Solutions",
                "suite": "PEER'S Incident Response Orchestrator v2.0",
                "developer": "Mohammed Peer Siddiqui",
                "framework": "NIST SP 800-61 Rev.2 (Computer Security Incident Handling Guide)",
                "generated_at": datetime.now().isoformat(),
                "total_incidents": len(self.active_incidents),
                "total_containment_actions": len(self.containment_log),
                "total_quarantined_artifacts": len(self.quarantined_artifacts)
            },
            "incidents": self.active_incidents,
            "containment_audit_log": self.containment_log,
            "quarantine_ledger": self.quarantined_artifacts
        }

        # Write JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        # Write TXT
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("    SQROCK IT SOLUTIONS - NIST SP 800-61 INCIDENT RESPONSE AUDIT DOSSIER\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated At          : {report['metadata']['generated_at']}\n")
            f.write(f"Governing Standard    : {report['metadata']['framework']}\n")
            f.write(f"Total Incidents       : {report['metadata']['total_incidents']}\n")
            f.write(f"Total Actions Executed: {report['metadata']['total_containment_actions']}\n")
            f.write(f"Artifacts Sandboxed   : {report['metadata']['total_quarantined_artifacts']}\n")
            f.write("-" * 80 + "\n\n")

            f.write("--- 1. ACTIVE INCIDENTS & CURRENT POSTURE ---\n")
            for inc in self.active_incidents:
                f.write(f"[{inc['severity']}] {inc['incident_id']} - {inc['title']}\n")
                f.write(f"  Target User       : {inc['affected_user']}\n")
                f.write(f"  Attacker Vector   : IP {inc['attacker_ip']} -> Exfil {inc['forward_destination']}\n")
                f.write(f"  Current Status    : {inc['status']}\n")
                f.write(f"  MITRE Technique   : {inc['mitre_id']} ({inc['mitre_tactic']})\n\n")

            f.write("--- 2. CONTAINMENT ACTIONS CHRONOLOGY ---\n")
            for act in self.containment_log:
                f.write(f"[{act['status']}] {act['action_id']} ({act['type']})\n")
                f.write(f"  Target: {act['target']} | Timestamp: {act['timestamp']}\n")
                f.write(f"  Action Details: {act['details']}\n\n")

            f.write("--- 3. QUARANTINED FORENSIC ARTIFACTS (CHAIN OF CUSTODY) ---\n")
            for art in self.quarantined_artifacts:
                f.write(f"File Name : {art['artifact_name']}\n")
                f.write(f"SHA-256   : {art['sha256']}\n")
                f.write(f"Isolated  : {art['quarantine_path']}\n")
                f.write(f"Timestamp : {art['quarantined_at']}\n\n")

        return report


def print_banner():
    """Display terminal banner."""
    print(Fore.CYAN + Style.BRIGHT + r"""
  _____ _____     ____  _____   _____ _    _ ______  _____ _______ _____         _______ ____  _____  
 |_   _|  __ \   / __ \|  __ \ / ____| |  | |  ____|/ ____|__   __|  __ \     /\|__   __/ __ \|  __ \ 
   | | | |__) | | |  | | |__) | |    | |__| | |__  | (___    | |  | |__) |   /  \  | | | |  | | |__) |
   | | |  _  /  | |  | |  _  /| |    |  __  |  __|  \___ \   | |  |  _  /   / /\ \ | | | |  | |  _  / 
  _| |_| | \ \  | |__| | | \ \| |____| |  | | |____ ____) |  | |  | | \ \  / ____ \| | | |__| | | \ \ 
 |_____|_|  \_\  \____/|_|  \_\\_____|_|  |_|______|_____/   |_|  |_|  \_|/_/    \_\_|  \____/|_|  \_\
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + " [*] Automated NIST SP 800-61 Rev.2 Containment & SOAR Playbook Engine v2.0")
    print(Fore.GREEN + " [*] Developer: Mohammed Peer Siddiqui | Sqrock IT Solutions Cybersecurity Lab")
    print(Fore.WHITE + " [*] Controls: NIST SP 800-61 | CIS Control 17 | MITRE ATT&CK T1078, T1114.003\n")


def run_interactive_menu():
    """CLI driver loop."""
    orchestrator = IROrchestrator()
    orchestrator.load_incident_from_siem()

    while True:
        print_banner()
        print(Fore.LIGHTBLUE_EX + " [=== MASTER INCIDENT RESPONSE ORCHESTRATION MENU ===]")
        print(Fore.WHITE + " [1] Ingest Active Incident Dossier (SIEM / Manual Triage)")
        print(Fore.WHITE + " [2] Execute Automated P1 Containment Playbook (Identity + Net + Email)")
        print(Fore.WHITE + " [3] Sandbox & Quarantine Malicious Artifacts (Chain of Custody)")
        print(Fore.WHITE + " [4] View Active Containment Audit Trail & Incident Posture")
        print(Fore.WHITE + " [5] Export NIST SP 800-61 Incident Report (JSON & Text Dossier)")
        print(Fore.WHITE + " [6] Exit Orchestrator\n")

        try:
            choice = input(Fore.CYAN + " ir-soar@sqrock-soc:~$ " + Style.RESET_ALL).strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting IR Orchestrator...")
            break

        if choice == "1":
            print(Fore.YELLOW + "\n[*] Ingesting active high-severity incidents...")
            count = orchestrator.load_incident_from_siem()
            print(Fore.GREEN + f"[+] Successfully loaded {count} incident dossier(s):")
            for inc in orchestrator.active_incidents:
                print(Fore.RED + f"    [{inc['severity']}] {inc['incident_id']} - {inc['title']}")
                print(Fore.WHITE + f"         User: {inc['affected_user']} | Attacker IP: {inc['attacker_ip']} | Status: {inc['status']}\n")
            input(Fore.LIGHTBLACK_EX + "Press Enter to continue...")

        elif choice == "2":
            print(Fore.YELLOW + "\n[*] DISPATCHING AUTOMATED CONTAINMENT PLAYBOOK (NIST SP 800-61 Rev.2)...")
            res = orchestrator.execute_full_playbook(0)
            print(Fore.GREEN + "[+] Phase 1: Identity Containment -> EXECUTED (Account Locked, Sessions Revoked)")
            print(Fore.GREEN + "[+] Phase 2: Mailbox Containment  -> EXECUTED (Forwarding Rule Purged)")
            print(Fore.GREEN + "[+] Phase 3: Perimeter Firewall   -> EXECUTED (Attacker IP Blacklisted)")
            print(Fore.GREEN + f"[+] Phase 4: Artifact Sandboxing  -> EXECUTED (SHA-256: {res['quarantined_artifact']['sha256'][:16]}...)")
            print(Fore.CYAN + f"\n[+] Incident {res['incident']['incident_id']} Posture Updated: {Fore.GREEN}CONTAINED\n")
            input(Fore.LIGHTBLACK_EX + "Press Enter to continue...")

        elif choice == "3":
            print(Fore.YELLOW + "\n[*] Sandboxing suspicious email lure into isolated quarantine vault...")
            sample_payload = "MIME-Version: 1.0\nSubject: Account Verification Required\nX-Spam-Flag: YES\nMalicious lure binary payload simulated."
            art = orchestrator.quarantine_artifact(sample_payload, "suspicious_attachment.bin")
            print(Fore.GREEN + f"[+] Artifact successfully preserved in quarantine vault!")
            print(Fore.WHITE + f"    File Name   : {art['artifact_name']}")
            print(Fore.WHITE + f"    SHA-256     : {art['sha256']}")
            print(Fore.WHITE + f"    Storage Path: {art['quarantine_path']}\n")
            input(Fore.LIGHTBLACK_EX + "Press Enter to continue...")

        elif choice == "4":
            print(Fore.YELLOW + "\n[=== CURRENT INCIDENT POSTURE & AUDIT TRAIL ===]")
            for act in orchestrator.containment_log:
                print(Fore.CYAN + f"[{act['status']}] {act['action_id']} ({act['type']})")
                print(Fore.WHITE + f"   Target: {act['target']}")
                print(Fore.LIGHTBLACK_EX + f"   Details: {act['details']}\n")
            if not orchestrator.containment_log:
                print(Fore.YELLOW + "[*] No containment actions recorded yet. Run option [2] to execute.")
            input(Fore.LIGHTBLACK_EX + "Press Enter to continue...")

        elif choice == "5":
            print(Fore.YELLOW + "\n[*] Compiling formal NIST SP 800-61 Rev.2 incident response audit reports...")
            res = orchestrator.export_reports()
            print(Fore.GREEN + f"[+] JSON Report exported: {DEFAULT_INCIDENT_JSON}")
            print(Fore.GREEN + f"[+] Text Dossier exported: {DEFAULT_INCIDENT_TXT}")
            print(Fore.CYAN + f"[+] Summary: {res['metadata']['total_containment_actions']} Actions Executed | {res['metadata']['total_quarantined_artifacts']} Artifacts Sandboxed.\n")
            input(Fore.LIGHTBLACK_EX + "Press Enter to continue...")

        elif choice == "6":
            print(Fore.CYAN + "\n[*] Terminating IR Orchestrator console. Stay safe!\n")
            break
        else:
            print(Fore.RED + "\n[!] Invalid choice. Please select 1-6.\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and "--batch" in sys.argv:
        orch = IROrchestrator()
        orch.load_incident_from_siem()
        orch.execute_full_playbook(0)
        orch.export_reports()
        print("[+] Headless IR Orchestration execution completed.")
    else:
        run_interactive_menu()
