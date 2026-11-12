from fastapi import Query


def pagination_params(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    return {
        "limit": limit,
        "offset": offset
    }


def sorting_params(
    sort_by: str = Query(default="id"),
    order: str = Query(default="asc", pattern="^(asc|desc)$")
):
    return {
        "sort_by": sort_by,
        "order": order
    }



def get_current_user():
    return {
        "id": 1,
        "username": "test_user"
    }
