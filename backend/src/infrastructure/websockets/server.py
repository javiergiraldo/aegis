import socketio
from fastapi import FastAPI

# Initialize the AsyncServer for ASGI, allowing cross-origin for the frontend
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

@sio.event
async def connect(sid, environ):
    """Handle client connection."""
    print(f"[Socket.IO] Client connected: {sid}")
    # Integration point: Add JWT validation / Zero-Trust auth checks here.

@sio.event
async def disconnect(sid):
    """Handle client disconnection."""
    print(f"[Socket.IO] Client disconnected: {sid}")

def get_socketio_app(fastapi_app: FastAPI) -> socketio.ASGIApp:
    """Wrap FastAPI app with Socket.IO ASGI App."""
    return socketio.ASGIApp(socketio_server=sio, other_asgi_app=fastapi_app)

async def emit_security_alert(alert_data: dict):
    """Utility to push security alerts to connected dashboard clients."""
    await sio.emit('security_alert', alert_data, namespace='/')
