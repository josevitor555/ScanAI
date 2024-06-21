import pathlib
import textwrap
from IPython.display import Markdown
import google.generativeai as genai

GOOGLE_API_KEY = 'YOUR_API_KEY'
genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

# model = genai.GenerativeModel('gemini-1.5-flash')
# response = model.generate_content("Qual o significado da Vida?", stream=True)

model = genai.GenerativeModel('gemini-1.5-flash')

image_paths = ['images/naruto.jpeg', 'images/sakura.jpeg', 'images/sasuke.jpeg']

parts = [genai.protos.Part(text='Quem desses personagens são do clã uchiha?')]
for image_path in image_paths:
    parts.append(
        genai.protos.Part(
            inline_data=genai.protos.Blob(
                mime_type='image/jpeg',
                data=pathlib.Path(image_path).read_bytes()
            )
        )
    )

response = model.generate_content(genai.protos.Content(parts=parts), stream=True)
response.resolve()

# response = model.generate_content(
#     genai.protos.Content(
#         parts = [
#             genai.protos.Part(text='Que tipo de reação é expressada por parte da pessoa?'),
#             genai.protos.Part(
#                 inline_data=genai.protos.Blob(
#                     mime_type='image/jpg',
#                     data=pathlib.Path('images/naruto.jpeg').read_bytes()
#                 )
#             ),
#         ],
#     ),
#     stream=True)
# response.resolve()

for chunk in response:
    print(chunk.text)
    print('_' * 80)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

to_markdown(response.text)
