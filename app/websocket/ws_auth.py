from fastapi import WebSocket, WebSocketException, status
from app.accounts.auth import get_current_user 

async def websocket_authenticate_user(websocket: WebSocket):
    token = websocket.query_params.get("token")

    if not token:
        auth_header = websocket.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]

    if not token:
        print("Token not found in query parameters or headers")
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Missing authentication token"
        )

    try:
        user = await get_current_user(token=token)
        print(f"Authenticated user: {user.username}")
        return user
    except Exception as e:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Authentication failed"
        )
