"""Liveness and readiness health check routes."""

from fastapi import APIRouter, HTTPException, Request, status

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/live", status_code=status.HTTP_200_OK)
def liveness() -> dict[str, str]:
    """Return 200 OK when the application process is running."""
    return {"status": "alive"}


@router.get("/ready", status_code=status.HTTP_200_OK)
def readiness(request: Request) -> dict[str, str]:
    """Return 200 when dependencies are ready, 503 otherwise."""
    if getattr(request.app.state, "user_service", None) is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User service unavailable.",
        )

    return {"status": "ready", "persistence": "in-memory"}
