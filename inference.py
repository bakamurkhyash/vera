from runware import Runware
import asyncio
import requests
from google import genai
from google.genai import types
from io import BytesIO



runware = Runware(api_key="YOUR_RUNWARE_API_KEY")

async def generate_qwen_edit():

    prompt = "Place the person from image 1 into the scenic beach background of image 2"
    image_1_url = "https://example.com/person.png"
    image_2_url = "https://example.com/beach_background.png"

    # 2. Configure the inference request

    request_config = {
        "model": "runware:1@qwen-image-edit-2509", 
        "positivePrompt": prompt,
        "inputImage": [image_1_url, image_2_url], 
        "numberResults": 1,
        "outputType": "URL",  
        "steps": 40,          
        "CFGScale": 4.0       
    }

    # 3. Perform inference
    images = await runware.imageInference(**request_config)

    # 4. Output the result
    for img in images:
        print(f"Generated Image URL: {img.imageURL}")



client = genai.Client(api_key="YOUR_API_KEY")

def process_cloudinary_images(url1, url2, prompt):
    # 1. Download images into memory from Cloudinary
    img1_data = requests.get(url1).content
    img2_data = requests.get(url2).content

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
