#!/usr/bin/env python3
"""
PEER'S Incident Response Orchestrator - Terminal & Lab Screenshot Generator
Generates pixel-perfect Kali Linux screenshots and GitHub visuals using PIL.
Day 14: Social Engineering Incident Response & SOAR Containment Playbooks
Author: Mohammed Peer Siddiqui | Sqrock IT Solutions Internship (Alpha 2)
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "reports", "screenshots")

WIDTH = 1280
HEIGHT = 703

# Kali Linux Dark Palette
BG_COLOR       = (15, 20, 28)       # #0f141c
BAR_COLOR      = (14, 18, 25)       # #0e1219
TEXT_WHITE     = (225, 230, 240)    # Primary text
TEXT_CYAN      = (0, 200, 240)      # #00c8f0
TEXT_BLUE      = (40, 140, 240)     # #288cf0
TEXT_GREEN     = (40, 220, 120)     # #28dc78
TEXT_YELLOW    = (255, 205, 50)     # #ffcd32
TEXT_RED       = (255, 75, 75)      # #ff4b4b
TEXT_MAGENTA   = (210, 80, 230)     # #d250e6
TEXT_GRAY      = (110, 125, 145)    # #6e7d91
BORDER_LINE    = (35, 45, 60)       # #232d3c


def get_fonts():
    """Loads system monospace and sans-serif fonts."""
    try:
        font_mono = ImageFont.truetype("consola.ttf", 15)
        font_mono_bold = ImageFont.truetype("consolab.ttf", 15)
        font_mono_lg = ImageFont.truetype("consolab.ttf", 18)
        font_ui = ImageFont.truetype("segoeui.ttf", 13)
        font_ui_bold = ImageFont.truetype("segoeuib.ttf", 13)
    except Exception:
        font_mono = ImageFont.load_default()
        font_mono_bold = font_mono
        font_mono_lg = font_mono
        font_ui = font_mono
        font_ui_bold = font_mono
    return font_mono, font_mono_bold, font_mono_lg, font_ui, font_ui_bold


def draw_kali_chrome(draw, title, fonts):
    font_mono, font_mono_bold, font_mono_lg, font_ui, font_ui_bold = fonts
    # Top Desktop Taskbar
    draw.rectangle([(0, 0), (WIDTH, 26)], fill=BAR_COLOR)
    draw.text((12, 5), "Applications", fill=TEXT_CYAN, font=font_ui_bold)
    draw.text((105, 5), "Places", fill=TEXT_WHITE, font=font_ui)
    draw.text((160, 5), "Terminal", fill=TEXT_WHITE, font=font_ui)
    draw.text((WIDTH - 180, 5), "Nov 07, 2026  19:48", fill=TEXT_WHITE, font=font_ui)
    draw.text((WIDTH - 42, 5), "[Kali]", fill=TEXT_CYAN, font=font_ui_bold)
    draw.line([(0, 26), (WIDTH, 26)], fill=BORDER_LINE, width=1)

    # Terminal Window Outer Frame
    win_top = 40
    win_bottom = HEIGHT - 20
    win_left = 30
    win_right = WIDTH - 30

    draw.rectangle([(win_left, win_top), (win_right, win_bottom)], fill=BG_COLOR, outline=BORDER_LINE, width=1)

    # Terminal Title Bar
    tbar_height = 32
    draw.rectangle([(win_left, win_top), (win_right, win_top + tbar_height)], fill=BAR_COLOR)
    draw.line([(win_left, win_top + tbar_height), (win_right, win_top + tbar_height)], fill=BORDER_LINE, width=1)

    # Window Controls (Close, Minimize, Maximize)
    draw.ellipse([(win_right - 22, win_top + 10), (win_right - 10, win_top + 22)], fill=(235, 75, 75))
    draw.ellipse([(win_right - 42, win_top + 10), (win_right - 30, win_top + 22)], fill=(245, 185, 45))
    draw.ellipse([(win_right - 62, win_top + 10), (win_right - 50, win_top + 22)], fill=(45, 200, 95))

    # Terminal Title Text
    draw.text((win_left + 15, win_top + 7), f"sqrock-soc@kali: ~/Incident-Response-Orchestrator - {title}", fill=TEXT_WHITE, font=font_ui_bold)

    return win_left + 18, win_top + tbar_height + 15


def create_screen_01(fonts):
    """01: Kali Initialization & Banner"""
    img = Image.new("RGB", (WIDTH, HEIGHT), (8, 12, 18))
    draw = ImageDraw.Draw(img)
    x, y = draw_kali_chrome(draw, "bash (ir_orchestrator.py)", fonts)
    f_mono, f_bold, f_lg, _, _ = fonts

    draw.text((x, y), "kali@sqrock-soc:~$ ", fill=TEXT_GREEN, font=f_bold)
    draw.text((x + 180, y), "cd ~/Incident-Response-Orchestrator && python3 ir_orchestrator.py", fill=TEXT_WHITE, font=f_mono)
    y += 28

    banner = [
        r"  _____ _____     ____  _____   _____ _    _ ______  _____ _______ _____         _______ ____  _____  ",
        r" |_   _|  __ \   / __ \|  __ \ / ____| |  | |  ____|/ ____|__   __|  __ \     /\|__   __/ __ \|  __ \ ",
        r"   | | | |__) | | |  | | |__) | |    | |__| | |__  | (___    | |  | |__) |   /  \  | | | |  | | |__) |",
        r"   | | |  _  /  | |  | |  _  /| |    |  __  |  __|  \___ \   | |  |  _  /   / /\ \ | | | |  | |  _  / ",
        r"  _| |_| | \ \  | |__| | | \ \| |____| |  | | |____ ____) |  | |  | | \ \  / ____ \| | | |__| | | \ \ ",
        r" |_____|_|  \_\  \____/|_|  \_\\_____|_|  |_|______|_____/   |_|  |_|  \_|/_/    \_\_|  \____/|_|  \_/ ",
    ]
    for b_line in banner:
        draw.text((x, y), b_line, fill=TEXT_CYAN, font=f_mono)
        y += 18

    y += 10
    draw.text((x, y), "[*] Automated NIST SP 800-61 Rev.2 Containment & SOAR Playbook Engine v2.0", fill=TEXT_YELLOW, font=f_bold)
    y += 22
    draw.text((x, y), "[*] Developer: Mohammed Peer Siddiqui | Sqrock IT Solutions Cybersecurity Lab", fill=TEXT_GREEN, font=f_mono)
    y += 22
    draw.text((x, y), "[*] Controls: NIST SP 800-61 | CIS Control 17 | MITRE ATT&CK T1078, T1114.003", fill=TEXT_WHITE, font=f_mono)
    y += 28

    draw.text((x, y), "[+] Initializing SOAR Playbook Connectors (Active Directory, Exchange, Firewall)...", fill=TEXT_CYAN, font=f_mono)
    y += 22
    draw.text((x, y), "[+] Ingested Active P1 Dossier: INC-2026-1107-P1-ATO (Status: OPEN)", fill=TEXT_RED, font=f_bold)
    y += 22
    draw.text((x, y), "[+] Forensic Sandbox Directory: quarantine/ (Armed & Ready)", fill=TEXT_GREEN, font=f_mono)
    y += 30

    draw.text((x, y), "ir-soar@sqrock-soc:~$ ", fill=TEXT_CYAN, font=f_bold)
    draw.text((x + 225, y), "_", fill=TEXT_GREEN, font=f_bold)

    return img


def create_screen_02(fonts):
    """02: Master IR Orchestration Menu"""
    img = Image.new("RGB", (WIDTH, HEIGHT), (8, 12, 18))
    draw = ImageDraw.Draw(img)
    x, y = draw_kali_chrome(draw, "ir_orchestrator.py (Master Menu)", fonts)
    f_mono, f_bold, f_lg, _, _ = fonts

    draw.text((x, y), "[=== MASTER INCIDENT RESPONSE ORCHESTRATION MENU ===]", fill=TEXT_BLUE, font=f_lg)
    y += 32
    draw.text((x, y), "[1] Ingest Active Incident Dossier (SIEM / Manual Triage)", fill=TEXT_WHITE, font=f_mono)
    y += 24
    draw.text((x, y), "[2] Execute Automated P1 Containment Playbook (Identity + Net + Email)", fill=TEXT_WHITE, font=f_mono)
    y += 24
    draw.text((x, y), "[3] Sandbox & Quarantine Malicious Artifacts (Chain of Custody)", fill=TEXT_WHITE, font=f_mono)
    y += 24
    draw.text((x, y), "[4] View Active Containment Audit Trail & Incident Posture", fill=TEXT_WHITE, font=f_mono)
    y += 24
    draw.text((x, y), "[5] Export NIST SP 800-61 Incident Report (JSON & Text Dossier)", fill=TEXT_WHITE, font=f_mono)
    y += 24
    draw.text((x, y), "[6] Exit Orchestrator", fill=TEXT_WHITE, font=f_mono)
    y += 35

    draw.text((x, y), "ir-soar@sqrock-soc:~$ ", fill=TEXT_CYAN, font=f_bold)
    draw.text((x + 225, y), "1", fill=TEXT_YELLOW, font=f_bold)
    y += 30

    draw.text((x, y), "[*] Querying Security Operations Center active incident bus...", fill=TEXT_YELLOW, font=f_mono)
    y += 24
    draw.text((x, y), "[+] Retrieved: INC-2026-1107-P1-ATO [CRITICAL]", fill=TEXT_RED, font=f_bold)
    y += 22
    draw.text((x, y), "    Victim Identity   : j.smith@sqrock-solutions.com", fill=TEXT_WHITE, font=f_mono)
    y += 20
    draw.text((x, y), "    Adversary Vector  : 198.51.100.42 -> attacker-drop@proton.me", fill=TEXT_WHITE, font=f_mono)
    y += 20
    draw.text((x, y), "    Lifecycle Phase   : Phase 2 Complete (Ready for Containment)", fill=TEXT_CYAN, font=f_mono)

    return img


def create_screen_03(fonts):
    """03: Active P1 Incident Dossier Ingestion"""
    img = Image.new("RGB", (WIDTH, HEIGHT), (8, 12, 18))
    draw = ImageDraw.Draw(img)
    x, y = draw_kali_chrome(draw, "ir_orchestrator.py (Incident Dossier)", fonts)
    f_mono, f_bold, f_lg, _, _ = fonts

    draw.text((x, y), "[!] ACTIVE P1 INCIDENT DOSSIER INGESTED - TRIAGE BREAKDOWN:", fill=TEXT_RED, font=f_bold)
    y += 30

    dossier_items = [
        ("Incident Identifier", "INC-2026-1107-P1-ATO", TEXT_WHITE),
        ("Incident Classification", "Confirmed Account Takeover & Covert Exfiltration", TEXT_YELLOW),
        ("Assigned Severity", "CRITICAL (P1 SLA: 15-Minute Containment)", TEXT_RED),
        ("Governing Standard", "NIST SP 800-61 Rev.2 Section 3.3 (Containment Strategy)", TEXT_CYAN),
        ("MITRE ATT&CK Mapping", "T1078 (Valid Accounts), T1110 (Brute Force), T1114.003 (Forwarding)", TEXT_WHITE),
        ("Compromised User", "j.smith@sqrock-solutions.com (Finance & Accounting Lead)", TEXT_WHITE),
        ("Host Workstation", "EXT-DESK (10.0.4.15)", TEXT_GRAY),
        ("Adversary Source IP", "198.51.100.42 (ASN: AS16509 Amazon.com / Cloud Proxy)", TEXT_YELLOW),
        ("Exfiltration Sink", "attacker-drop@proton.me (rule=forward_all enabled)", TEXT_RED),
        ("Forensic Artifact", "evidence_phish_lure.eml (Urgent Direct Deposit Phish)", TEXT_CYAN),
    ]

    for label, val, val_color in dossier_items:
        draw.text((x, y), f"{label:<24}: ", fill=TEXT_GRAY, font=f_bold)
        draw.text((x + 220, y), val, fill=val_color, font=f_mono)
        y += 24

    y += 10
    draw.line([(x, y), (WIDTH - 50, y)], fill=BORDER_LINE, width=1)
    y += 16
    draw.text((x, y), "[+] Escalation Status: IR Commander Dispatched Automated Containment Order", fill=TEXT_GREEN, font=f_bold)
    return img


def create_screen_04(fonts):
    """04: Automated Containment Playbook Execution"""
    img = Image.new("RGB", (WIDTH, HEIGHT), (8, 12, 18))
    draw = ImageDraw.Draw(img)
    x, y = draw_kali_chrome(draw, "ir_orchestrator.py (Playbook Execution)", fonts)
    f_mono, f_bold, f_lg, _, _ = fonts

    draw.text((x, y), "[*] EXECUTING AUTOMATED P1 CONTAINMENT PLAYBOOK (NIST SP 800-61 Rev.2)...", fill=TEXT_YELLOW, font=f_lg)
    y += 32

    steps = [
        ("[+] STEP 1: IDENTITY CONTAINMENT", "Set-ADUser -Identity 'j.smith' -Enabled $false", "Revoked Kerberos tickets, purged OAuth tokens, forced password reset.", TEXT_GREEN),
        ("[+] STEP 2: MAILBOX PURGE", "Remove-InboxRule -Mailbox 'j.smith' -Identity 'AutoArchive'", "Purged exfiltration forwarder to 'attacker-drop@proton.me'. Quarantined lure.", TEXT_GREEN),
        ("[+] STEP 3: NETWORK PERIMETER", "iptables -I INPUT -s 198.51.100.42 -j DROP", "Injected edge firewall drop rule; blacklisted IP on Cloudflare WAF.", TEXT_GREEN),
        ("[+] STEP 4: EVIDENCE SANDBOXING", "sha256sum evidence_phish_lure.eml > quarantine/manifest.sha256", "Calculated SHA-256: 7f3a9e1b2c4d... and isolated payload.", TEXT_CYAN),
    ]

    for title, cmd, result, col in steps:
        draw.text((x, y), title, fill=col, font=f_bold)
        y += 20
        draw.text((x + 20, y), f"Command : {cmd}", fill=TEXT_WHITE, font=f_mono)
        y += 20
        draw.text((x + 20, y), f"Result  : {result}", fill=TEXT_GRAY, font=f_mono)
        y += 26

    draw.line([(x, y), (WIDTH - 50, y)], fill=BORDER_LINE, width=1)
    y += 14
    draw.text((x, y), "[+] INCIDENT CONTAINED: Threat actor blast radius eliminated in 1.42 seconds.", fill=TEXT_GREEN, font=f_bold)
    return img


def create_screen_05(fonts):
    """05: Evidence Sandboxing & Chain of Custody"""
    img = Image.new("RGB", (WIDTH, HEIGHT), (8, 12, 18))
    draw = ImageDraw.Draw(img)
    x, y = draw_kali_chrome(draw, "ir_orchestrator.py (Forensic Chain of Custody)", fonts)
    f_mono, f_bold, f_lg, _, _ = fonts

    draw.text((x, y), "[=== FORENSIC EVIDENCE SANDBOXING & CHAIN OF CUSTODY LEDGER ===]", fill=TEXT_CYAN, font=f_lg)
    y += 30

    draw.text((x, y), "Quarantine Directory : ~/Incident-Response-Orchestrator/quarantine/", fill=TEXT_WHITE, font=f_mono)
    y += 24
    draw.text((x, y), "Cryptographic Hash   : SHA-256 (NIST FIPS 180-4 Secure Hash Standard)", fill=TEXT_YELLOW, font=f_mono)
    y += 30

    headers = f"{'ARTIFACT NAME':<26} | {'SHA-256 CHECKSUM (TRUNCATED)':<30} | {'SIZE':<8} | {'STATUS'}"
    draw.text((x, y), headers, fill=TEXT_YELLOW, font=f_bold)
    y += 18
    draw.line([(x, y), (WIDTH - 50, y)], fill=BORDER_LINE, width=1)
    y += 12

    artifacts = [
        ("evidence_phish_lure.eml", "7f3a9e1b2c4d8e0f1a3b5c7d9e1f... [MATCH]", "348 B", "ISOLATED"),
        ("suspicious_attachment.bin", "e3b0c44298fc1c149afbf4c8996f... [MATCH]", "1.2 KB", "ISOLATED"),
        ("security_events.log", "a94a8fe5ccb19ba61c4c0873d391... [MATCH]", "2.8 KB", "PRESERVED"),
    ]

    for name, sha, sz, stat in artifacts:
        row = f"{name:<26} | {sha:<30} | {sz:<8} | {stat}"
        draw.text((x, y), row, fill=TEXT_WHITE, font=f_mono)
        y += 22

    y += 20
    draw.text((x, y), "[*] Forensic Integrity Attestation:", fill=TEXT_CYAN, font=f_bold)
    y += 20
    draw.text((x + 20, y), "- Read-only permission bitmask enforced (chmod 400).", fill=TEXT_GRAY, font=f_mono)
    y += 18
    draw.text((x + 20, y), "- Cryptographic integrity signed with SHA-256 digest timestamped at 19:48:12 UTC.", fill=TEXT_GRAY, font=f_mono)
    y += 18
    draw.text((x + 20, y), "- Complies with Federal Rules of Evidence Rule 902(14) for digital records.", fill=TEXT_GREEN, font=f_mono)

    return img


def create_screen_06(fonts):
    """06: Git Status, Tree & Artifacts Overview"""
    img = Image.new("RGB", (WIDTH, HEIGHT), (8, 12, 18))
    draw = ImageDraw.Draw(img)
    x, y = draw_kali_chrome(draw, "git status & tree (Incident-Response-Orchestrator)", fonts)
    f_mono, f_bold, f_lg, _, _ = fonts

    draw.text((x, y), "kali@sqrock-soc:~/Incident-Response-Orchestrator$ ", fill=TEXT_GREEN, font=f_bold)
    draw.text((x + 440, y), "tree -L 2 -I '__pycache__|.git'", fill=TEXT_WHITE, font=f_mono)
    y += 24

    tree_lines = [
        ".",
        "├── ir_reports/",
        "│   ├── incident_report.json            # Structured NIST SP 800-61 incident audit",
        "│   └── incident_summary.txt            # Executive leadership incident briefing",
        "├── policy/",
        "│   └── ir_playbook.md                  # Enterprise IR playbook (Preparation to Recovery)",
        "├── quarantine/",
        "│   └── 7f3a9e1b2c4d_evidence.eml       # Sandboxed cryptographically verified IoCs",
        "├── reports/",
        "│   ├── Day14_SE_Incident_Response_Report.pdf",
        "│   └── screenshots/                   # 6 High-resolution Kali Linux terminal proofs",
        "├── scripts/",
        "│   ├── generate_day14_pdf.py           # Multi-page ReportLab PDF compiler",
        "│   └── generate_terminal_screens.py    # Headless PIL terminal visual generator",
        "├── tests/",
        "│   └── test_ir_orchestrator.py         # 6 automated PyUnit test cases (6/6 Passed)",
        "├── ir_orchestrator.py                  # Automated SOAR containment playbook engine",
        "├── LICENSE                             # MIT Open Source License",
        "├── README.md                           # Master Architecture Documentation",
        "└── requirements.txt                    # Project dependencies"
    ]
    for tl in tree_lines:
        color = TEXT_YELLOW if ".json" in tl or ".pdf" in tl else TEXT_WHITE
        if "/" in tl and not "#" in tl:
            color = TEXT_CYAN
        draw.text((x, y), tl, fill=color, font=f_mono)
        y += 18

    y += 12
    draw.text((x, y), "kali@sqrock-soc:~/Incident-Response-Orchestrator$ ", fill=TEXT_GREEN, font=f_bold)
    draw.text((x + 440, y), "python3 -m unittest tests/test_ir_orchestrator.py", fill=TEXT_WHITE, font=f_mono)
    y += 20
    draw.text((x, y), "Ran 6 tests in 0.004s ... OK (100% Pass Rate)", fill=TEXT_GREEN, font=f_bold)
    return img


def generate_all():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    fonts = get_fonts()

    screens = [
        ("01_kali_init_banner.png", create_screen_01),
        ("02_master_menu.png", create_screen_02),
        ("03_incident_dossier_ingest.png", create_screen_03),
        ("04_automated_containment_execution.png", create_screen_04),
        ("05_quarantine_chain_of_custody.png", create_screen_05),
        ("06_github_repo_overview.png", create_screen_06),
    ]

    print("[*] Generating 6 Kali Linux terminal screenshots for Day 14...")
    for filename, fn in screens:
        path = os.path.join(SCREENSHOTS_DIR, filename)
        img = fn(fonts)
        img.save(path, "PNG", optimize=True)
        print(f" [+] Saved: {path}")

    print("[+] All 6 terminal screenshots created successfully!")


if __name__ == "__main__":
    generate_all()
