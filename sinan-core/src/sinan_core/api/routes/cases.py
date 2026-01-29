# sinan-core/src/sinan_core/api/routes/cases.py
"""用例管理 API"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sinan_core.storage.case_store import LocalCaseStore
from sinan_core.models.case import TestCase, TestStep

router = APIRouter(tags=["cases"])
case_store = LocalCaseStore()


class CreateCaseRequest(BaseModel):
    case_name: str
    steps: list[dict] = []


@router.get("/cases")
async def list_cases():
    """获取所有用例"""
    return case_store.list_all()


@router.get("/cases/{case_id}")
async def get_case(case_id: str):
    """获取单个用例"""
    case = case_store.load(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="用例不存在")
    return case.to_dict()


@router.post("/cases")
async def create_case(request: CreateCaseRequest):
    """创建用例"""
    import uuid
    case_id = f"tc_{uuid.uuid4().hex[:8]}"

    case = TestCase(case_id=case_id, case_name=request.case_name)
    for i, step_data in enumerate(request.steps):
        step = TestStep(
            step_id=i + 1,
            action=step_data.get("action", "tap"),
            target_desc=step_data.get("target_desc", ""),
            coordinates=step_data.get("coordinates", [0, 0]),
        )
        case.add_step(step)

    case_store.save(case)
    return {"case_id": case_id, "message": "用例创建成功"}


@router.delete("/cases/{case_id}")
async def delete_case(case_id: str):
    """删除用例"""
    if case_store.delete(case_id):
        return {"message": "用例已删除"}
    raise HTTPException(status_code=404, detail="用例不存在")
