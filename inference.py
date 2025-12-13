from runware import Runware
import asyncio
import requests
from google import genai
from google.genai import types
from io import BytesIO


# Initialize the Runware client with your API Key
# Replace 'YOUR_RUNWARE_API_KEY' with your actual key
runware = Runware(api_key="YOUR_RUNWARE_API_KEY")

async def generate_qwen_edit():
    # 1. Define your prompt and input images
    # You can use public URLs or base64-encoded strings
    prompt = "Place the person from image 1 into the scenic beach background of image 2"
    image_1_url = "https://example.com/person.png"
    image_2_url = "https://example.com/beach_background.png"

    # 2. Configure the inference request
    # Note: Qwen-Image-Edit-2509 is referenced via its AIR (AI Resource) identifier
    # For multi-image, we pass a list to the 'input_image' parameter
    request_config = {
        "model": "runware:1@qwen-image-edit-2509", # Use the specific AIR for this model
        "positivePrompt": prompt,
        "inputImage": [image_1_url, image_2_url], # Array of 2 images
        "numberResults": 1,
        "outputType": "URL",  # Can be "URL" or "base64Data"
        "steps": 40,          # Standard for high quality; use 4-8 if using a 'Lightning' version
        "CFGScale": 4.0       # Qwen-2509 performs well at a lower CFG (around 4.0)
    }

    # 3. Perform inference
    images = await runware.imageInference(**request_config)

    # 4. Output the result
    for img in images:
        print(f"Generated Image URL: {img.imageURL}")



client = genai.Client(api_key="YOUR_API_KEY")

def process_cloudinary_images(url1, url2, prompt):
    # 1. Download images into memory from Cloudinary
    # This is better than saving to disk
    img1_data = requests.get(url1).content
    img2_data = requests.get(url2).content

    # 2. Wrap them for the Gemini API
    # We use types.Part.from_bytes to tell Gemini these are image tokens
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[
            prompt,
            types.Part.from_bytes(data=img1_data, mime_type="image/png"),
            types.Part.from_bytes(data=img2_data, mime_type="image/png")
        ],
        config=types.GenerateContentConfig(response_modalities=["IMAGE"])
    )
    
    return response.candidates[0].content.parts[0].as_image()

if __name__ == "__main__":
    asyncio.run(generate_qwen_edit())