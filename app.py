from flask import Flask, render_template, request
from dotenv import dotenv_values
import json
import openai

config = dotenv_values(".env")
openai.api_key = config['OPEN_AI_API_KEY']

def get_color(textPrompt):
    prompt = f"""
    You are a color generating assistant that responds to text prompts for color palettes.
    You should generate colors that fit the mood, the theme, or the instructions in the prompt below. 

    Prompt: {textPrompt}

    Output Structure: should be a JSON file with an array of hex colors string values.

    Example: ["color hex", "color hex"]

    Result:

    """
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = prompt,
        max_tokens = 100,
    )

    return json.loads(response["choices"][0]["text"])


app = Flask(__name__,
  template_folder='templates',
)

@app.route('/get-colors', methods=['POST'])
def get_colors():
  query = request.form.get('query')
  return { "colors": get_color(query) }

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)