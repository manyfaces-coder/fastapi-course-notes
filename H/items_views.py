from typing import Annotated

from fastapi import Path, APIRouter

# from H.main import app
router = APIRouter(
    prefix="/items", tags=["Items"]
)  # (Пространство имен, чтобы не прописывать @app)


@router.get("/")
def list_items():
    return ["item1", "item2", "item3"]


@router.get("/latest/")
def get_latest_item():
    return {"item": {"id": "0", "name": "latest"}}


@router.get("/{item_id}/")
# def get_item_by_id(item_id: int):
def get_item_by_id(
    item_id: Annotated[int, Path(ge=1, lt=1_000_000)],
):  # ge - grate equal, lt - low than, underline –
    return {  # – не имеет значения в числе
        "item": {
            "id": item_id,
        }
    }
