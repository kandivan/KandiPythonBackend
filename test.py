from database import Database, User
from ai_generation import AIGenerationService, ImageCaptionGenerator
from PIL import Image

# db = Database()
# session = db.get_session()
# # Insert data
# # new_user = User(name='John Doe', email='john@example.com', password='securepassword')
# # session.add(new_user)
# # session.commit()

# # Query data
# users = session.query(User).filter(User.name == 'John Doe').all()
# for user in users:
#     print(user.email)
#     session.delete(user)
# session.commit()

# generator = AIGenerationService()
# image_description = generator.image_caption_generator.predict_step(['shoe.jpg'])
# prompt = "An image for a marketing campaign on facebook ads, centered around " + image_description[0]
# generator.generate_image(prompt)

import requests
import torch
from PIL import Image
from io import BytesIO

from diffusers import StableDiffusionImg2ImgPipeline

device = "cuda"
model_id_or_path = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
pipe = pipe.to(device)

image_path = "shoe.jpg"
init_image = Image.open(image_path)
init_image = init_image.resize((768, 512))

prompt = "Marketing campaign for a shoe company."

images = pipe(prompt=prompt, image=init_image, strength=0.75, guidance_scale=7.5).images
images[0].save("shoe.png")