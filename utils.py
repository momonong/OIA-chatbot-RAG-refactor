import httpx
import base64
import json


async def send_async_request(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            return response.text if response.status_code == 200 else None
        except Exception as e:
            return None


def clear_token(session):
    if "oauth_token" in session:
        del session["oauth_token"]


def decode_token(access_token):
    try:
        jwt_parts = access_token.split(".")
        if len(jwt_parts) != 3:
            raise ValueError("Invalid token format")
        payload_encoded = jwt_parts[1]
        payload_encoded += "=" * (4 - len(payload_encoded) % 4)
        payload_decoded = base64.urlsafe_b64decode(payload_encoded)
        return json.loads(payload_decoded)
    except Exception as e:
        print(f"\n\nError decoding token: {str(e)}\n\n")
        return {}


def normalize_name(display_name, student_en_name):
    if student_en_name.lower() not in display_name.lower():
        return f"{display_name} {student_en_name}"
    return display_name