from .routes import router
from .database import app  # Import the app with lifespan + DB setup

# API metadata 
app.title = "Employee API"
app.version = "1.0"

# Include all routes
app.include_router(router)
