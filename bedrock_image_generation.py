import json
import boto3
import botocore
from datetime import datetime
import base64

def lambda_handler(event, context):
    # Parse the incoming event to extract the image generation prompt
    event = json.loads(event['body'])
    message = event['message']  # The text prompt for generating the image

    # Initialize the Bedrock runtime client with extended read timeout and retry configuration
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name="us-east-1",
        config=botocore.config.Config(read_timeout=300, retries={'max_attempts': 3})
    )

    # Initialize the S3 client for storing the generated image
    s3 = boto3.client('s3')

    # Define the payload for the diffusion model with text prompt and generation parameters
    payload = {
        "text_prompts": [{"text": message}],  # Text input for generating the image
        "cfg_scale": 10,  # Strength of guidance (how closely image follows the prompt)
        "seed": 0,  # Seed for reproducibility
        "steps": 100  # Number of steps for image generation
    }

    # Invoke the diffusion model in Bedrock with the payload
    response = bedrock.invoke_model(
        body=json.dumps(payload),
        modelId='stability.stable-diffusion-xl-v1',
        contentType="application/json",
        accept="application/json"
    )

    # Decode the response from the model to extract the base64-encoded image
    response_body = json.loads(response.get("body").read())
    base_64_img_str = response_body["artifacts"][0].get("base64")
    image_content = base64.decodebytes(bytes(base_64_img_str, "utf-8"))  # Decode base64 to binary image content

    # Define S3 bucket name and file path for storing the generated image
    bucket_name = 'bedrock-image-generation-test'
    current_time = datetime.now().strftime('%H%M%S')  # Generate a unique timestamp for the image file
    s3_key = f"output-images/{current_time}.png"  # S3 key (path) for storing the image

    # Upload the image to the specified S3 bucket with proper content type
    s3.put_object(
        Bucket=bucket_name,
        Key=s3_key,
        Body=image_content,
        ContentType='image/png'
    )

    # Return a success response indicating the image was saved to S3
    return {
        'statusCode': 200,
        'body': json.dumps('Image Saved to S3')
    }
