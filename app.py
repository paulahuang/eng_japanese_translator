print("App.py is starting...")

from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
from openai import OpenAI
import os, json


app = Flask(__name__)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate(text):
    print("🔵 translate() called with:", text)

    try:
        prompt = f"""
        Translate the following English text into natural japanese.
        Also provide:
        - pronunciation (latin letters)
        - a grammar explanation (simple and easy)

        Return ONLY a JSON object. Do NOT add explanations, notes, or code fences.

        Example of correct output:
        {{
            "japanese": "Bonjour",
            "pronunciation": "bon-zhoor",
            "grammar": "Simple greeting. No verb. Informal or formal."
        }}

        Text: {text}
        """

        result = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        raw = result.output_text.strip()
        print("🟢 Raw model output:", raw)

        # Remove markdown code fences if they appear
        raw = raw.replace("```json", "").replace("```", "").strip()

        # Try to extract JSON if additional text appears
        json_start = raw.find("{")
        json_end = raw.rfind("}") + 1
        cleaned = raw[json_start:json_end]

        print("🟢 Cleaned JSON:", cleaned)

        data = json.loads(cleaned)

        return {
            "japanese": data.get("japanese", ""),
            "pronunciation": data.get("pronunciation", ""),
            "grammar": data.get("grammar", "")
        }

    except Exception as e:
        print("🔴 ERROR in translate():", e)
        return {
            "japanese": "",
            "pronunciation": "",
            "grammar": "",
            "error": str(e)
        }





@app.route("/")
def home():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def do_translate():
    print("🟡 /translate endpoint called")

    data = request.json
    print("🟡 Request data:", data)

    text = data.get("text", "")

    if not text:
        print("🔴 No text received")
        return jsonify({"error": "empty"}), 400

    result = translate(text)
    print("🟣 Returning:", result)

    return jsonify(result)

if __name__ == "__main__":
    print("🔥 Flask server is starting...")
    app.run(debug=True)



