#!/usr/bin/env python3
"""
Unit Tests for PEER'S Incident Response Orchestrator
Sqrock IT Solutions - Cybersecurity Internship Phase 1 (Day 14)
"""

import os
import sys
import unittest
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from ir_orchestrator import IROrchestrator


class TestIROrchestrator(unittest.TestCase):
    """Test suite for incident ingestion, automated containment, and forensic evidence preservation."""

    def setUp(self):
        self.orchestrator = IROrchestrator()
        self.orchestrator.load_incident_from_siem()

    def test_incident_ingestion(self):
        """Test that active incidents are loaded into memory with required NIST attributes."""
        self.assertGreaterEqual(len(self.orchestrator.active_incidents), 1)
        inc = self.orchestrator.active_incidents[0]
        self.assertIn("incident_id", inc)
        self.assertEqual(inc["severity"], "CRITICAL")
        self.assertEqual(inc["status"], "OPEN")

    def test_user_identity_lockout(self):
        """Test Active Directory account lockout action simulation."""
        action = self.orchestrator.lock_user_account("j.smith@sqrock-solutions.com")
        self.assertEqual(action["status"], "EXECUTED")
        self.assertEqual(action["type"], "IDENTITY_CONTAINMENT")
        self.assertIn("j.smith@sqrock-solutions.com", action["target"])

    def test_mailbox_rule_purge(self):
        """Test Exchange mailbox forwarding purge action."""
        action = self.orchestrator.purge_mailbox_forwarding("j.smith@sqrock-solutions.com", "attacker-drop@proton.me")
        self.assertEqual(action["status"], "EXECUTED")
        self.assertEqual(action["type"], "MAILBOX_CONTAINMENT")
        self.assertIn("attacker-drop@proton.me", action["details"])

    def test_perimeter_firewall_block(self):
        """Test edge firewall drop rule deployment action."""
        action = self.orchestrator.block_network_ip("198.51.100.42")
        self.assertEqual(action["status"], "EXECUTED")
        self.assertEqual(action["type"], "NETWORK_PERIMETER_BLOCK")
        self.assertEqual(action["target"], "198.51.100.42")

    def test_evidence_quarantine_and_hashing(self):
        """Test artifact sandboxing and SHA-256 chain-of-custody cryptographic hashing."""
        sample_data = "Subject: Urgent Wire Transfer\nFrom: ceo@impersonation.com"
        record = self.orchestrator.quarantine_artifact(sample_data, "test_phish.eml")
        self.assertEqual(len(record["sha256"]), 64)  # Valid SHA-256 length
        self.assertTrue(os.path.exists(record["quarantine_path"]))

    def test_full_playbook_execution_and_export(self):
        """Test automated NIST SP 800-61 end-to-end containment and JSON/TXT report export."""
        res = self.orchestrator.execute_full_playbook(0)
        self.assertEqual(res["incident"]["status"], "CONTAINED")
        self.assertEqual(len(res["actions"]), 3)

        report = self.orchestrator.export_reports()
        self.assertGreaterEqual(report["metadata"]["total_containment_actions"], 3)
        self.assertGreaterEqual(report["metadata"]["total_quarantined_artifacts"], 1)

        json_path = os.path.join(BASE_DIR, "ir_reports", "incident_report.json")
        txt_path = os.path.join(BASE_DIR, "ir_reports", "incident_summary.txt")
        self.assertTrue(os.path.exists(json_path))
        self.assertTrue(os.path.exists(txt_path))


if __name__ == "__main__":
    unittest.main()
