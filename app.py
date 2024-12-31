from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import openai
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///templates.db'
db = SQLAlchemy(app)

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

class ScriptTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(50), nullable=False)
    theme = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/generate_script', methods=['POST'])
def generate_script():
    data = request.json
    genre = data.get('genre')
    theme = data.get('theme')
    characters = data.get('characters')

    prompt = f"Generate a movie script in the {genre} genre with the theme '{theme}' featuring the characters {', '.join(characters)}."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    script_content = response['choices'][0]['message']['content']
    
    return jsonify({"script": script_content})

@app.route('/templates', methods=['GET'])
def get_templates():
    templates = ScriptTemplate.query.all()
    return jsonify([{"id": t.id, "genre": t.genre, "theme": t.theme, "content": t.content} for t in templates])

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
