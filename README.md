Zane.TI - Deploy-ready Flask package for Render

How to use (quick):
1. Create a GitHub repo and push all files from this package's root.
2. On Render, create a new Web Service and connect the repo.
   Render will use render.yaml -> pip install -r requirements.txt and start gunicorn.
3. Configure environment variables in Render dashboard (Settings > Environment).
   - OPENAI_API_KEY : for OpenAI Chat/Image (optional)
   - DEEPL_KEY : for DeepL translation (optional)

Local test:
  python -m venv venv
  source venv/bin/activate     # Windows: venv\Scripts\activate
  pip install -r requirements.txt
  python app.py
  Open http://localhost:10000

Notes:
- All real API calls are commented inside app.py. If you want real integration,
  set the environment variables in Render and uncomment the request() blocks.
- No Node.js files (package.json) are included, so Render will detect Python runtime.
