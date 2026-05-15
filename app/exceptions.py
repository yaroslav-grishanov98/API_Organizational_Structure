from fastapi import HTTPException


def not_found(entity: str = "Resource"):
    return HTTPException(status_code=404, detail=f"{entity} not found")

def conflict(detail: str = "Conflict"):
    return HTTPException(status_code=409, detail=detail)

def bad_request(detail: str = "Bad request"):
    return HTTPException(status_code=400, detail=detail)
