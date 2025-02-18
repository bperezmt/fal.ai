import requests
from PIL import Image
from io import BytesIO
import fal_client

def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])

def generate_image(model, prompt):
    result = fal_client.subscribe(
        model,
        arguments={"prompt": prompt},
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    image_url = result['images'][0]['url']
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    image.show()

def main():
    models = {
        "1": "fal-ai/flux-pro/v1.1",
        "2": "fal-ai/flux/dev",
        "3": "fal-ai/flux/schnell"
    }
    
    while True:
        print("\nSelect an image generation model:")
        print("1. fal-ai/flux-pro/v1.1")
        print("2. fal-ai/flux/dev")
        print("3. fal-ai/flux/schnell")
        print("4. Exit")
        
        choice = input("Enter the number of your choice: ")
        
        if choice == "4":
            print("Exiting the program…")
            break
        
        if choice in models:
            prompt = input("Enter your prompt for image generation: ")
            generate_image(models[choice], prompt)
        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()
