from mcp.server.fastmcp import FastMCP
import httpx
import base64
import os
import mimetypes

# Initialize FastMCP server
mcp = FastMCP("cluster-vision-mcp")

# Environment variables
# README example suggests API_URL might be the base URL (e.g. http://192.168.10.106:1234)
# We will ensure we construct the correct chat completion endpoint
BASE_URL = os.environ.get("API_URL", "http://localhost:1234").rstrip("/")
MODEL_NAME = os.environ.get("MODEL_NAME", "gemma-3n-e4b-it-mlx")

@mcp.tool()
async def analyze_image(image_path: str) -> str:
    """
    指定した画像を解析して、オブジェクト位置や名前などを解析した結果を取得します。
    
    Args:
        image_path: 解析する画像の絶対パス
    """
    if not os.path.exists(image_path):
        return f"Error: File not found at {image_path}"

    # Determine mime type
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/jpeg" # Default fallback

    try:
        # Read and encode image
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        image_url = f"data:{mime_type};base64,{encoded_string}"

        headers = {
            "Content-Type": "application/json"
        }
        
        # Construct endpoint URL
        # If the user provided a full path in API_URL, usage might be tricky if we append, 
        # but matching README example, we expect a base URL.
        # We'll check if it already looks like a completion URL to be safe, though simple append is safer for the target use case.
        if "/v1/chat/completions" in BASE_URL:
             api_endpoint = BASE_URL
        else:
             api_endpoint = f"{BASE_URL}/v1/chat/completions"
        
        payload = {
            "model": MODEL_NAME,
            "messages": [

                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "画像を分析してください。\n映っている主要なオブジェクトを列挙し、それぞれのオブジェクトが画像のどのあたりにあるか（位置情報）を詳しく説明してください。"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1000
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(api_endpoint, json=payload, headers=headers, timeout=60.0)
            response.raise_for_status()
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            return content

    except httpx.RequestError as e:
        return f"Network error communicating with LM Studio: {str(e)}"
    except httpx.HTTPStatusError as e:
        return f"API error from LM Studio: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

if __name__ == "__main__":
    mcp.run()
