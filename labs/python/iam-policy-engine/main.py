"""Least-privilege IAM audit engine; demonstrative synthetic identity records."""
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path

# Never treat a title as permission: roles must map to explicit resources/actions.
POLICY = {
    "viewer": {"reports": ["read"]},
    "analyst": {"reports": ["read", "write"], "incidents": ["read", "write"]},
    "admin": {"reports": ["read", "write", "delete"], "incidents": ["read", "write", "approve"]},
    "auditor": {"reports": ["read"], "audit": ["read"]},
}
# Separation of duties: the same identity shouldn't request and approve a payout.
CONFLICTS = {frozenset(("requester", "approver")), frozenset(("admin", "auditor"))}

@dataclass(frozen=True)
class Identity:
    username: str
    roles: tuple[str, ...]
    active: bool = True


def authorize(identity: Identity, resource: str, action: str) -> dict:
    if not identity.active:
        return {"allow": False, "reason": "inactive identity"}
    for role in identity.roles:
        if action in POLICY.get(role, {}).get(resource, ()):
            return {"allow": True, "reason": f"explicit {role} permission"}
    return {"allow": False, "reason": "default deny"}


def audit(identities: list[Identity]) -> dict:
    findings = []
    for identity in identities:
        if not identity.active and identity.roles:
            findings.append({"user": identity.username, "severity": "high", "issue": "inactive account retains roles"})
        for conflict in CONFLICTS:
            if conflict.issubset(identity.roles):
                findings.append({"user": identity.username, "severity": "high", "issue": "separation-of-duties conflict: " + "/".join(sorted(conflict))})
        invalid = sorted(set(identity.roles) - POLICY.keys() - {"requester", "approver"})
        if invalid:
            findings.append({"user": identity.username, "severity": "medium", "issue": "unmapped roles: " + ", ".join(invalid)})
    return {"identities_checked": len(identities), "findings": findings, "passed": len(findings) == 0}


def main():
    parser = argparse.ArgumentParser(description="Offline IAM role access audit")
    parser.add_argument("--identities", type=Path, default=Path(__file__).with_name("sample.json"))
    parser.add_argument("--check", nargs=3, metavar=("USERNAME", "RESOURCE", "ACTION"))
    args = parser.parse_args()
    data = json.loads(args.identities.read_text(encoding="utf8"))
    identities = [Identity(x["username"], tuple(x.get("roles", [])), bool(x.get("active", True))) for x in data]
    if args.check:
        username, resource, action = args.check
        target = next((x for x in identities if x.username == username), None)
        print(json.dumps(authorize(target, resource, action) if target else {"allow": False, "reason": "unknown identity"}, indent=2))
    else:
        print(json.dumps(audit(identities), indent=2))

if __name__ == "__main__": main()
