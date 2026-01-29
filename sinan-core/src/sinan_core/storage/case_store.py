# sinan-core/src/sinan_core/storage/case_store.py
"""本地用例存储"""
import json
from pathlib import Path
from typing import Optional
from ..models.case import TestCase


class LocalCaseStore:
    """本地 JSON 文件存储"""

    def __init__(self, storage_dir: str = "./cases"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save(self, case: TestCase) -> str:
        """保存用例"""
        file_path = self.storage_dir / f"{case.case_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(case.to_json())
        return str(file_path)

    def load(self, case_id: str) -> Optional[TestCase]:
        """加载用例"""
        file_path = self.storage_dir / f"{case_id}.json"
        if not file_path.exists():
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            return TestCase.from_json(f.read())

    def list_all(self) -> list[dict]:
        """列出所有用例"""
        cases = []
        for file_path in self.storage_dir.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cases.append({
                        "case_id": data["case_id"],
                        "case_name": data["case_name"],
                        "status": data.get("status", "pending"),
                    })
            except Exception:
                continue
        return cases

    def delete(self, case_id: str) -> bool:
        """删除用例"""
        file_path = self.storage_dir / f"{case_id}.json"
        if file_path.exists():
            file_path.unlink()
            return True
        return False
