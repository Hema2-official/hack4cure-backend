from fastapi import APIRouter

from routers import auth, accounts, appointments, resources, demands, debug, generate, sss, upcoming, logs, rooms, maintenances, statistics, user, mi

router = APIRouter()

router.include_router(auth.router, prefix="/auth")
router.include_router(accounts.router, prefix="/accounts")
router.include_router(debug.router, prefix="/debug")
router.include_router(generate.router, prefix="/generate")
router.include_router(logs.router, prefix="/logs")
router.include_router(rooms.router, prefix="/rooms")
router.include_router(maintenances.router, prefix="/maintenances")
router.include_router(statistics.router, prefix="/statistics")
router.include_router(rooms.router, prefix="/rooms")
router.include_router(user.router, prefix="/user")
router.include_router(mi.router, prefix="/mi")
