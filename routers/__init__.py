from fastapi import APIRouter

from routers import (
    auth, 
    accounts, 
    debug, 
    generate, 
    logs,
    forms,
    documents,
)
router = APIRouter()

router.include_router(auth.router, prefix="/auth")
router.include_router(accounts.router, prefix="/accounts")
router.include_router(debug.router, prefix="/debug")
router.include_router(generate.router, prefix="/generate")
router.include_router(logs.router, prefix="/logs")
router.include_router(forms.router, prefix="/forms")
router.include_router(documents.router, prefix="/documents")
