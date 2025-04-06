"""
Main initialization file for routes package
"""

from app.backend.routes.email_routes import router as email_router
from app.backend.routes.client_routes import router as client_router
from app.backend.routes.routing_rules_routes import router as routing_rules_router
from app.backend.routes.system_routes import router as system_router

__all__ = [
    'email_router',
    'client_router',
    'routing_rules_router',
    'system_router'
]
