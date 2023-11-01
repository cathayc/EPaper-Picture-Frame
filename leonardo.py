import requests
import time
import os

base_url = "https://cloud.leonardo.ai/api/rest/v1/generations"
api_key = "c0f126f6-ef4c-4423-9c63-69322dd029ea"

def generate_image(prompt):

    # Define the headers for the API request
	headers = {
		"Authorization": f"Bearer {api_key}",
		"Content-Type": "application/json"
	}

    # Define the payload for the API request
	payload = {
		"height": 512,
		"modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
		"prompt": prompt,
		"width": 512
	}

	try:
		# Send a POST request to the Leonardo AI API to generate the image
		response = requests.post(base_url, headers=headers, json=payload)
		response.raise_for_status()  # Raise an exception if the request was not successful
		# print(response.json())

		# Extract the generation ID from response
		generation_id= response.json()['sdGenerationJob']['generationId']

		# Return the URL of the generated image
		return response.json(), generation_id

	except requests.exceptions.RequestException as e:
		# Handle any exceptions that occur during the API request
		raise ValueError(f"Failed to generate image: {e}")

def get_image(generation_id):
	# Define the headers for the API request
	headers = {
		"Authorization": f"Bearer {api_key}"
	}

	count = 0
	while True and count < 10:
		try:
			# Send a GET request to the Leonardo AI API to retrieve the image
			response = requests.get(f"{base_url}/{generation_id}", headers=headers)
			response.raise_for_status()  # Raise an exception if the request was not successful

			# Check if the response is empty
			if not response.json()["generations_by_pk"]["generated_images"]:
				count = count + 1
				# If the response is empty, introduce a delay and then retry the request
				print(f"Response is empty. Attempting retry #{count} in 2 seconds...")
				time.sleep(2)
				continue  # Retry the request

			# Return the URL of the generated image
			return response.json()

		except requests.exceptions.RequestException as e:
			# Handle any exceptions that occur during the API request
			raise ValueError(f"Failed to retrieve image: {e}")


# Example usage of the generate_image function:
def generate_ai_image(prompt):
	image_urls = []
	try:
		response_json, generation_id = generate_image(prompt)
		print(f"response_json: {response_json}")
		image_results = get_image(generation_id)['generations_by_pk']['generated_images']
		for image in image_results:
			url = image['url']
			image_urls.append(url)
			print(f"Generated image URL: {url}")
		return image_urls
	except ValueError as e:
		print(f"Error generating image: {e}")
	
def save_image(image_url, destination_name="Leo_Images"):
	# Should Default to Images as destination name
	image_name = image_url.split('/')[-1]
	print(image_name)
	imagedir = os.path.join(os.path.dirname(os.path.realpath(__file__)), destination_name)

	# Define the destination file path where you want to save the image
	destination_path = os.path.join(imagedir, image_name)

	# Send an HTTP GET request to the image URL
	response = requests.get(image_url)

	# Check if the request was successful (status code 200)
	if response.status_code == 200:
		# Open the destination file in binary write mode and write the content of the response
		with open(destination_path, "wb") as file:
			file.write(response.content)
		print(f"Image downloaded and saved to {destination_path}")
	else:
		print(f"Failed to download image. Status code: {response.status_code}")

def call_and_save(prompt, dest):
	image_urls = generate_ai_image(prompt)
	# image_urls = ['https://cdn.leonardo.ai/users/d81e277a-727d-4ba0-b196-c088406efbb5/generations/e42ddbc9-08fc-43cc-aef5-ca598bb1cfd4/Leonardo_Creative_Cathy_and_Tai_happy_0.jpg', 'https://cdn.leonardo.ai/users/d81e277a-727d-4ba0-b196-c088406efbb5/generations/e42ddbc9-08fc-43cc-aef5-ca598bb1cfd4/Leonardo_Creative_Cathy_and_Tai_happy_1.jpg', 'https://cdn.leonardo.ai/users/d81e277a-727d-4ba0-b196-c088406efbb5/generations/e42ddbc9-08fc-43cc-aef5-ca598bb1cfd4/Leonardo_Creative_Cathy_and_Tai_happy_2.jpg', 'https://cdn.leonardo.ai/users/d81e277a-727d-4ba0-b196-c088406efbb5/generations/e42ddbc9-08fc-43cc-aef5-ca598bb1cfd4/Leonardo_Creative_Cathy_and_Tai_happy_3.jpg']
	for image_url in image_urls:
		save_image(image_url, dest)

if __name__ == "__main__":
    call_and_save('Cathyssss')