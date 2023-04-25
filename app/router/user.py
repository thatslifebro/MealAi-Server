from fastapi import APIRouter

router = APIRouter(
    prefix="/api/users",
)


@router.get("/")
def f1():
    a1 = 1
    a2 = 2
    a3 = 3
    res = {"a1": a1, "a2": a2, "a3": a3}

    return res


@router.post("/")
def f2(c: int):
    a1 = 1
    a2 = 2
    a3 = 3
    res = {"a1": a1, "a2": a2, "a3": c}

    return res
