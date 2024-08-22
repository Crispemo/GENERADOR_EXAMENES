import os
import json

def record_failed_question(user_id, question):
    failed_questions_file = f"failed_questions_{user_id}.json"
    
    if os.path.exists(failed_questions_file):
        with open(failed_questions_file, "r") as file:
            failed_questions = json.load(file)
    else:
        failed_questions = []

    failed_questions.append(question)
    
    with open(failed_questions_file, "w") as file:
        json.dump(failed_questions, file, indent=4)

