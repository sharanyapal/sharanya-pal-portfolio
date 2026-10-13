"""Replayable event-time login detector with watermarks, deduplication and sliding windows.

Python standard library; no network connection or sensitive data collection.
"""
from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timezone
import argparse
import csv
import json

@dataclass(frozen=True)
class Event:
    event_id: str
    timestamp: float
    identity: str
    ip: str
    outcome: str

    @staticmethod
    def from_dict(row: dict) -> 'Event':
        stamp = str(row['timestamp']).replace('Z', '+00:00')
        return Event(str(row['event_id']), datetime.fromisoformat(stamp).timestamp(),
                     str(row['identity']), str(row['ip']), str(row['outcome']).upper())

class Detector:
    """Event-time bounded sliding-window detector; tolerates delayed arrivals."""
    def __init__(self, window_seconds=120, allowed_lateness=20, threshold=5):
        if window_seconds <= 0 or allowed_lateness < 0 or threshold <= 0:
            raise ValueError('Invalid window / lateness / threshold')
        self.window = window_seconds
        self.lateness = allowed_lateness
        self.threshold = threshold
        self.max_seen = float('-inf')
        self.seen: set[str] = set()
        self.pending: list[Event] = []
        self.failed: dict[str, deque[Event]] = defaultdict(deque)
        self.last_alert_at: dict[str, float] = {}
        self.alerts: list[dict] = []
        self.late_dropped = 0
        self.duplicates = 0

    def ingest(self, e: Event) -> None:
        if e.event_id in self.seen:
            self.duplicates += 1
            return
        self.seen.add(e.event_id)
        old_watermark = self.max_seen - self.lateness
        if e.timestamp < old_watermark:
            self.late_dropped += 1
            return
        self.max_seen = max(self.max_seen, e.timestamp)
        self.pending.append(e)
        self._flush(self.max_seen - self.lateness)

    def _flush(self, watermark: float) -> None:
        ready = sorted((e for e in self.pending if e.timestamp <= watermark),
                       key=lambda e: (e.timestamp, e.event_id))
        self.pending = [e for e in self.pending if e.timestamp > watermark]
        for e in ready:
            dq = self.failed[e.ip]
            while dq and e.timestamp - dq[0].timestamp > self.window:
                dq.popleft()
            if e.outcome == 'FAILURE':
                dq.append(e)
                if len(dq) >= self.threshold and e.timestamp - self.last_alert_at.get(e.ip, float('-inf')) >= self.window:
                    self.last_alert_at[e.ip] = e.timestamp
                    self.alerts.append({'type': 'BRUTE_FORCE', 'ip': e.ip,
                       'timestamp': datetime.fromtimestamp(e.timestamp, timezone.utc).isoformat(),
                       'failed_count': len(dq), 'unique_users': len({a.identity for a in dq})})
            elif e.outcome == 'SUCCESS' and len(dq) >= self.threshold - 1:
                self.alerts.append({'type': 'SUCCESS_AFTER_FAILURES', 'ip': e.ip,
                   'timestamp': datetime.fromtimestamp(e.timestamp, timezone.utc).isoformat(),
                   'failed_count': len(dq), 'identity': e.identity})

    def finish(self) -> list[dict]:
        self._flush(float('inf'))
        return list(self.alerts)

def run(path: str, threshold: int) -> dict:
    detector = Detector(threshold=threshold)
    with open(path, newline='', encoding='utf8') as fp:
        for row in csv.DictReader(fp):
            detector.ingest(Event.from_dict(row))
    return {'alerts': detector.finish(), 'duplicates': detector.duplicates,
            'dropped_late': detector.late_dropped}

if __name__ == '__main__':
    ap=argparse.ArgumentParser(description='Event-time login event analytics')
    ap.add_argument('csv_file');ap.add_argument('--threshold',type=int,default=5)
    args=ap.parse_args()
    print(json.dumps(run(args.csv_file,args.threshold),indent=2))
