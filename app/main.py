from .routes import router
from .database import app  # Import the app with lifespan + DB setup

# Add metadata if you want (title, version already set in database.py)
app.title = "Employee API"
app.version = "1.0"

# Include routes
app.include_router(router)
