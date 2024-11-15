# Project Report: Serverless Image Generation System Using AWS Lambda, Diffusion Model in Bedrock, API Gateway, and Amazon S3

## 1. Introduction

In this project, I developed a serverless architecture for generating images based on user-provided prompts. The system leverages **AWS Lambda**, **AWS Bedrock’s diffusion model ("stability.stable-diffusion-xl-v1")**, **Amazon API Gateway**, and **Amazon S3** to create, process, and store images. The diffusion model produces high-quality images by iteratively refining random noise to match the user’s prompt. Users can interact with the system by sending HTTP POST requests with image prompts, and the generated images are automatically stored in S3, making them accessible for further usage or sharing.

## 2. Designing the AWS Lambda Function

The AWS Lambda function serves as the core processing unit of my image generation workflow. This function handles tasks such as parsing user-provided prompts, interacting with the Bedrock diffusion model, and storing the resulting image in S3.

### Key Components of the Lambda Function

1. **Parsing User Input**: The Lambda function parses incoming requests from API Gateway, including the user’s image prompt. The request body contains a JSON object with a "message" field specifying the prompt, such as “A cat running a marathon.”

2. **Interfacing with Bedrock’s Diffusion Model**: I configured the function to initialize the Bedrock runtime client with extended read timeouts and retry configurations. The diffusion model "stability.stable-diffusion-xl-v1" generates detailed images based on textual prompts.

   - I sent a payload to the diffusion model with parameters such as:
     - **text_prompts**: The prompt text provided by the user.
     - **cfg_scale**: Determines how closely the generated image adheres to the prompt.
     - **seed**: Ensures reproducibility of the generated image.
     - **steps**: Specifies the number of steps for image generation, affecting quality and detail.

3. **Handling Model Output**: The model responds with a base64-encoded image, which I decoded into binary format. This decoded image is then saved as a standard PNG file, making it accessible for various applications.

4. **Storing the Image in S3**: I configured the function to save the image in an S3 bucket with a unique filename based on a timestamp, ensuring efficient organization and retrieval.

### Lambda Code Flow

The Lambda function’s code execution flow includes:
- Parsing the input prompt from the API Gateway request.
- Configuring Bedrock client settings.
- Sending the prompt and parameters to Bedrock’s diffusion model.
- Decoding the base64 image data from the model response.
- Saving the decoded image to an S3 bucket with a unique name.

![Alt text](<https://github.com/RhythmAhir/bedrock_image_generation/blob/main/Screenshots/1.%20Lambda%20Function.png>)

The complete code for this Lambda function can be found in the **"Bedrock_image_generation.py"** file.

## 3. Configuring the S3 Bucket for Image Storage

I created an S3 bucket named **bedrock-image-generation-test** to store generated images. Within this bucket, I added a folder named **output-images/** to organize the images. Each generated image file is named with a unique timestamp, ensuring it can be easily identified and retrieved without conflicts.

![Alt text](<https://github.com/RhythmAhir/bedrock_image_generation/blob/main/Screenshots/2.%20S3%20Bucket%20Created.png>)

## 4. Setting Up API Gateway to Interface with Lambda

Amazon API Gateway serves as the entry point for user interactions. I configured an HTTP POST route to enable users to send prompts directly to the Lambda function, which processes the requests and generates images based on the prompts.

### Route Configuration

I set up an API Gateway route, `/image-generation,` to accept POST requests. This route is linked to the Lambda function, allowing it to be triggered by incoming HTTP requests containing JSON payloads with image prompts.

![Alt text](<https://github.com/RhythmAhir/bedrock_image_generation/blob/main/Screenshots/4.%20API%20Route.png>)

### Lambda Integration with API Gateway

API Gateway is integrated with the Lambda function through an HTTP endpoint, enabling external access. This integration manages the flow of data between users and the backend function.

![Alt text](<https://github.com/RhythmAhir/bedrock_image_generation/blob/main/Screenshots/3.%20API%20Gateway%20Integration%20with%20Lambda.png>)

## 5. Testing the API with Postman

To test the system, I used **Postman** to send a POST request with a sample prompt, such as **"A cat running a marathon."**

### Steps for Testing:
1. **Sending the Request**: In Postman, I constructed a JSON request:
   ```json
   {
       "message": "A cat running a marathon"
   }
   ```
2. **Receiving the Response**: The API returned a success message: **"Image Saved to S3"**, confirming that the image was generated and saved.

![Alt text](<https://github.com/RhythmAhir/bedrock_image_generation/blob/main/Screenshots/5.%20POSTMAN%20POST.png>)

## 6. Validating the Image in S3

After testing, I verified that the generated image was correctly stored in the specified S3 bucket under the **output-images/** folder.

![Alt text](<https://github.com/RhythmAhir/bedrock_image_generation/blob/main/Screenshots/6.%20Output%20saved%20in%20S3.png>)

## 7. Generated Image

Below is the sample image generated by Bedrock’s diffusion model based on the prompt "A cat running a marathon." The image was saved in S3 for further use.

![Alt text](<https://github.com/RhythmAhir/bedrock_image_generation/blob/main/Image-Output/062141.png>)

## Conclusion

This project demonstrates my ability to integrate multiple AWS services to build a serverless image generation pipeline. I created a scalable and flexible system for generating images based on user prompts by combining **AWS Lambda**, **API Gateway**, by combining **AWS Lambda**, **Bedrock’s diffusion model**, **API Gateway**, and **Amazon S3**.

### Key Takeaways
- **Scalability**: The serverless architecture can handle numerous requests without manual intervention.
- **Generative AI Integration**: Using Bedrock’s diffusion model allows for high-quality image generation, expanding creative possibilities.
- **Practical Applications**: The setup can be extended to use cases like e-commerce, social media, or custom artwork production.

In summary, I successfully showcased the power of serverless architectures combined with advanced AI models to deliver an efficient and flexible image generation solution.
