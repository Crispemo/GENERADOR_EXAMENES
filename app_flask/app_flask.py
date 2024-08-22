import json
import random
from flask import Flask, render_template, request, send_file
from responses import record_failed_question
from failed_exam_generator import generate_exam_from_failed_questions
import pandas as pd
import os
from fpdf import FPDF

app = Flask(__name__)

EXCEL_PATH = "/Users/cris/exam_generator/answers.xlsx"
QUESTIONS_DIR = "/Users/cris/exam_generator/exam_txt"
JSON_PATH = "/Users/cris/EXAM_GENERATOR/questions.json"
YEARS = list(range(1993, 1999)) + list(range(2010, 2023))

df_answers = pd.read_excel(EXCEL_PATH)

def load_questions(year):
    questions_file = os.path.join(QUESTIONS_DIR, f"{year}_ex_ocr.txt")
    with open(questions_file, "r") as file:
        questions = file.read().split("\n\n")  
    return questions

def parse_question(question_text, year, question_number):
    # Opciones de respuesta disponibles como enteros
    options = [1, 2, 3, 4, 5]

    # Obtener la respuesta correcta del archivo Excel
    correct_answer = df_answers[(df_answers['Year'] == year) & 
                                (df_answers['Question Number'] == question_number)]['Correct Answer'].values[0]

    # Asegurarse de que la respuesta correcta sea un entero
    correct_answer = int(correct_answer)

    # Imprimir para depuración
    print(f"Year: {year}, Question Number: {question_number}")
    print("Options:", options)
    print("Correct Answer:", correct_answer)

    # Verificar si la respuesta correcta está en las opciones
    if correct_answer not in options:
        print(f"ERROR: Correct answer {correct_answer} not in options {options}")
        return None  # Devuelve None o maneja este caso como prefieras

    correct_answer_index = options.index(correct_answer)

    return {
        "question": question_text,
        "options": options,
        "answer": correct_answer_index,
        "topic": None,
        "chapter": None
    }




    return question

def generate_questions_json():
    questions = []

    for year in YEARS:
        raw_questions = load_questions(year)
        for i, question_text in enumerate(raw_questions, start=1):
            question = parse_question(question_text, year, i)
            questions.append(question)
    
    with open(JSON_PATH, 'w') as f:
        json.dump(questions, f, indent=4)

    print(f"Saved {len(questions)} questions to {JSON_PATH}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_exam', methods=['POST'])
def generate_exam_route():
    num_questions = int(request.form['num_questions'])

    with open(JSON_PATH, 'r') as f:
        all_questions = json.load(f)
    
    selected_questions = random.sample(all_questions, num_questions)
    questions_text = [f"{i+1}. {q['question']}" for i, q in enumerate(selected_questions)]
    correct_answers = [f"{i+1}. {q['options'][q['answer']]}" for i, q in enumerate(selected_questions)]

    pdf_filename = "Simulated_EIR.pdf"
    generate_pdf(questions_text, correct_answers, pdf_filename)
    
    return send_file(pdf_filename, as_attachment=True)

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

if __name__ == "__main__":
    generate_questions_json()
    app.run(debug=True)






