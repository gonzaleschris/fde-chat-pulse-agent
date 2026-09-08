"""State management, async compaction, and history persistence."""
import asyncio
import json
import os
from typing import Any, Dict, List
from agent.observability import logger, scrub_pii

MEMORY_FILE = "agent_memory.json"


class PersistentAgentMemory:
    """Manages cross-session state with automated compaction."""
    def __init__(self, storage_path: str = MEMORY_FILE):
        self.storage_path = storage_path
        self._data: Dict[str, Any] = {"sessions": {}, "compacted_history": []}
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load memory file: {e}")

    def save(self) -> None:
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    def store_session_report(self, session_id: str, report: Dict[str, Any]) -> None:
        clean_report_str = scrub_pii(json.dumps(report))
        self._data["sessions"][session_id] = json.loads(clean_report_str)
        self.save()

    async def async_compact_history(self, max_items: int = 5) -> None:
        """Asynchronously summarizes and truncates older session states."""
        await asyncio.sleep(0.01)  # Non-blocking async yield
        session_keys = list(self._data["sessions"].keys())
        if len(session_keys) > max_items:
            overflow = session_keys[:-max_items]
            for old_key in overflow:
                summary = f"Archived week {old_key} with {len(self._data['sessions'][old_key].get('hot_topics', []))} topics."
                self._data["compacted_history"].append(summary)
                del self._data["sessions"][old_key]
            self.save()
            logger.info("Memory compaction completed successfully.", extra={"intent": "compact_memory", "outcome": "pruned_overflow"})
