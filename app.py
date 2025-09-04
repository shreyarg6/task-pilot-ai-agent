from flask import Flask, render_template, request, jsonify
from config import DEBUG
from utils.parser import parse_tasks
from utils.scheduler import prioritize
from services.llm import chat_reply
import html

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json(force=True) or {}
    items = data.get('items')

    if items:
        # parse each item separately to get due time and defaults
        parsed = []
        for it in items:
            title = (it.get('title') or '').strip()
            if not title:
                continue
            # reuse parser on a single sentence
            p = parse_tasks(title)
            if not p:
                continue
            t = p[0]
            # override with UI selections, if provided
            if it.get('minutes') is not None:
                t['estimated_minutes'] = int(it['minutes'])
            if it.get('importance'):
                t['importance'] = it['importance']
            parsed.append(t)
        ranked = prioritize(parsed)
        prompt = (
            "You are TaskPilot. Given these tasks (already parsed), produce a concise plan for today, "
            "in time order, with at most 6 actionable steps and at most 3 brief tips.\n\n"
            f"{ranked}"
        )
    else:
        # fallback: old path where the user pasted a blob of text
        user_input = (data.get('user_input') or '').strip()
        ranked = prioritize(parse_tasks(user_input))
        prompt = (
            "Tasks: " + user_input + "\nParsed: " + str(ranked) +
            "\nCreate a concise plan in time order."
        )

    try:
        reply = chat_reply(prompt)
    except Exception:
        reply = "(LLM unavailable) Here is the prioritized list."

    reply_html = '<br>'.join(html.escape(line) for line in reply.split('\n'))
    return jsonify({"reply_html": reply_html, "tasks": ranked})

if __name__ == '__main__':
    app.run(debug=DEBUG, use_reloader=False)
