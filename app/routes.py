import os
from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
import pandas as pd
from fpdf import FPDF

from app.cv_parser import extract_cv_text
from app.jd_parser import extract_jd_text
from app.matcher import get_match_score, get_match_score_and_reason

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

results_data = []  # Stores the results across routes

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    global results_data
    results_data = []

    if request.method == "POST":
        jd_file = request.files.get("job_description")
        cv_files = request.files.getlist("cvs")

        # Save and extract JD
        if jd_file and allowed_file(jd_file.filename):
            jd_path = os.path.join(UPLOAD_FOLDER, "jds", secure_filename(jd_file.filename))
            os.makedirs(os.path.dirname(jd_path), exist_ok=True)
            jd_file.save(jd_path)
            jd_text = extract_jd_text(jd_path)

            for cv in cv_files:
                if cv and allowed_file(cv.filename):
                    cv_path = os.path.join(UPLOAD_FOLDER, "cvs", secure_filename(cv.filename))
                    os.makedirs(os.path.dirname(cv_path), exist_ok=True)
                    cv.save(cv_path)

                    try:
                        cv_text = extract_cv_text(cv_path)
                        score, reason = get_match_score_and_reason(cv_text, jd_text)

                        results_data.append({
                            "file": cv.filename,
                            "score": float(score),
                            "reason": reason
                        })

                    except Exception as e:
                        results_data.append({
                            "file": cv.filename,
                            "score": "Error",
                            "reason": f"Failed to process: {str(e)}"
                        })

            # Sort by score descending (skip entries with 'Error')
            results_data.sort(
                key=lambda r: r["score"] if isinstance(r["score"], (int, float)) else 0,
                reverse=True
            )

            return redirect("/results")

    return render_template("index.html")

@app.route("/results")
def results():
    return render_template("results.html", results=results_data)

@app.route("/download/excel")
def download_excel():
    df = pd.DataFrame(results_data, columns=["file", "score", "reason"])
    file_path = os.path.join(UPLOAD_FOLDER, "match_results.xlsx")
    df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True)

@app.route("/download/pdf")
def download_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Candidate Match Results", ln=True, align='C')

    for r in results_data:
        pdf.multi_cell(0, 10, txt=f"{r['file']} - {r['score']}%\n{r['reason']}\n", border=0)

    file_path = os.path.join(UPLOAD_FOLDER, "match_results.pdf")
    pdf.output(file_path)
    return send_file(file_path, as_attachment=True)

