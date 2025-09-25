"""Zane.TI - Flask app (deploy-ready for Render)

Notes:
- requirements.txt is at repo root so Render detects Python runtime.
- render.yaml forces Python runtime and tells Render how to start the app.
- To use real APIs, set the environment variables in Render (Settings -> Environment):
    OPENAI_API_KEY, DEEPL_KEY, etc.
- Example calls to external APIs are commented. If the corresponding ENV var exists
  the app will attempt a real call; otherwise it returns a mocked response for testing.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Frontend routes (templates) ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/imagens')
def imagens_page():
    return render_template('imagens.html')

@app.route('/traducao')
def traducao_page():
    return render_template('traducao.html')

@app.route('/servicos')
def servicos_page():
    return render_template('servicos.html')

@app.route('/contato')
def contato_page():
    return render_template('contato.html')

# --- API endpoints ---

@app.route('/api/chatbot', methods=['POST'])
def api_chatbot():
    data = request.get_json(force=True)
    message = data.get('message', '')

    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    if OPENAI_API_KEY:
        # Example of real call to OpenAI (uncomment to use):
        # headers = {'Authorization': f'Bearer {OPENAI_API_KEY}', 'Content-Type': 'application/json'}
        # payload = {'model':'gpt-3.5-turbo', 'messages':[{'role':'user','content':message}]}
        # resp = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload, timeout=30)
        # if resp.status_code == 200:
        #     j = resp.json()
        #     reply = j['choices'][0]['message']['content']
        #     return jsonify({'reply': reply})
        # else:
        #     return jsonify({'error': 'OpenAI error', 'detail': resp.text}), 502

        # For safety in this template we return a note telling user to enable real calls.
        return jsonify({'reply': f'[MOCKED - OpenAI key detected but real call is commented] You said: {message}'})
    else:
        # Mock response for local testing without keys
        return jsonify({'reply': f'Mock reply — you said: {message}'})

@app.route('/api/imagem', methods=['POST'])
def api_imagem():
    data = request.get_json(force=True)
    prompt = data.get('prompt', '')

    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    if OPENAI_API_KEY:
        # Example: generate image with OpenAI Images API (uncomment to use)
        # headers = {'Authorization': f'Bearer {OPENAI_API_KEY}', 'Content-Type':'application/json'}
        # payload = {'model':'gpt-image-1','prompt':prompt,'size':'1024x1024'}
        # resp = requests.post('https://api.openai.com/v1/images/generations', headers=headers, json=payload, timeout=30)
        # if resp.status_code == 200:
        #     j = resp.json()
        #     url = j['data'][0]['url']
        #     return jsonify({'url': url})
        # else:
        #     return jsonify({'error':'Image API error','detail':resp.text}), 502

        return jsonify({'url': f'[MOCKED - image call commented] https://via.placeholder.com/1024?text={prompt[:40]}'})

    # Fallback: return placeholder image
    return jsonify({'url': 'https://via.placeholder.com/1024?text=' + requests.utils.requote_uri(prompt[:60])})

@app.route('/api/traduzir', methods=['POST'])
def api_traduzir():
    data = request.get_json(force=True)
    text = data.get('text', '')
    target = data.get('targetLang', 'EN')

    DEEPL_KEY = os.environ.get('DEEPL_KEY')
    if DEEPL_KEY:
        # Example using DeepL (uncomment to use):
        # payload = {'auth_key': DEEPL_KEY, 'text': text, 'target_lang': target}
        # resp = requests.post('https://api-free.deepl.com/v2/translate', data=payload, timeout=30)
        # if resp.status_code == 200:
        #     j = resp.json()
        #     return jsonify({'translated': j['translations'][0]['text']})
        # else:
        #     return jsonify({'error':'DeepL error','detail':resp.text}), 502

        return jsonify({'translated': f'[MOCKED - DeepL key present, real call commented] ({target}) ' + text})

    # Mock fallback
    return jsonify({'translated': f'[{target}] ' + text})

# Simple in-memory CRUD for "projects" (example of sistemas personalizados)
PROJECTS = []
NEXT_ID = 1

@app.route('/api/projects', methods=['GET','POST'])
def api_projects():
    global NEXT_ID
    if request.method == 'POST':
        payload = request.get_json(force=True)
        name = payload.get('name','Untitled')
        desc = payload.get('desc','')
        project = {'id': NEXT_ID, 'name': name, 'desc': desc}
        NEXT_ID += 1
        PROJECTS.append(project)
        return jsonify(project), 201
    else:
        return jsonify(PROJECTS)

@app.route('/api/projects/<int:pid>', methods=['DELETE'])
def api_project_delete(pid):
    global PROJECTS
    PROJECTS = [p for p in PROJECTS if p['id'] != pid]
    return jsonify({'ok': True})

# Contact endpoint (simulated)
@app.route('/api/contact', methods=['POST'])
def api_contact():
    payload = request.get_json(force=True)
    name = payload.get('name')
    email = payload.get('email')
    message = payload.get('message')
    # In production replace by real email sending (SMTP/SendGrid) using env vars
    print(f'[CONTACT] {name} <{email}>: {message}')
    return jsonify({'ok': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
