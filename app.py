# app.py

from flask import Flask, request, jsonify, render_template
import openai
import PyPDF2

app = Flask(__name__)
openai.api_key = "sk-proj-n68N3o6F5CQ31qYpxn82T3BlbkFJfKbMmoet0gKelGtZLZpO"

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    cv_file = request.files["cv_file"]
    job_description_file = request.files["job_description_file"]
    
    cv_text = extract_text_from_pdf(cv_file)
    job_description_text = extract_text_from_pdf(job_description_file)
    
    prompt = f"""
    As an AI recruiting assistant, evaluate the candidate's suitability for the role based on their CV and the job requirements.
    
    CV: {cv_text}
    
    Job Description: {job_description_text}
    
    Provide a score from 1 to 10 (10 being the best fit) and a 2-4 sentence explanation of your score. Consider factors such as relevant skills, experience, qualifications, and overall fit for the role. Mention both pros and cons in your explanation.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )

    analysis = response.choices[0].message.content.strip()
    
    # Extract score and explanation from the response
    lines = analysis.split("\n")
    score = lines[0].split(":")[1].strip()
    explanation = " ".join(lines[1:])

    return jsonify({"score": score, "explanation": explanation})


if __name__ == "__main__":
    app.run(debug=True)