import os
import json
import random
from fpdf import FPDF

def generate_exam_from_failed_questions(user_id):
    failed_questions_file = f"failed_questions_{user_id}.json"
    
    if os.path.exists(failed_questions_file):
        with open(failed_questions_file, "r") as file:
            failed_questions = json.load(file)
    else:
        return None

    selected_questions = random.sample(failed_questions, min(len(failed_questions), 10))
    questions_text = [f"{i+1}. {q['question']}" for i, q in enumerate(selected_questions)]
    correct_answers = [f"{i+1}. {q['options'][q['answer']]}" for i, q in enumerate(selected_questions)]
    
    pdf_filename = f"Failed_Questions_Exam_{user_id}.pdf"
    generate_pdf(questions_text, correct_answers, pdf_filename)
    
    return pdf_filename

def generate_pdf(questions, answers, filename="new_exam.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(0, 10, "Generated Exam", ln=True, align="C")
    pdf.ln(10)

    for i, question in enumerate(questions, start=1):
        pdf.multi_cell(0, 10, f"{question}")
        pdf.ln(3) 

    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Correct Answers", ln=True, align="C")
    pdf.ln(10)

    for i, answer in enumerate(answers, start=1):
        pdf.multi_cell(0, 10, f"Question {i}: Correct Answer: {answer}")
        pdf.ln(5)

    pdf.output(filename)