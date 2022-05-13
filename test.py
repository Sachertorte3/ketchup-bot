with open('questions.txt', encoding="utf-8") as f:
        lines = f.readlines()
        questions = {}
        for line in lines:
            questions[line.split(',')[0]] = line.split(',')[1]
        print([{"type": "postback", "data": f"Q:{question_Q}\nA:{question_A}", "label": question_Q}
                         for question_Q, question_A in questions.items()])
print(lines)