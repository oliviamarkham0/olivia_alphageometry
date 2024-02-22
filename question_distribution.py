question_counts = {}

with open('full_problems2.txt', 'r') as file:
    for line in file:
        if '?' in line:
            question_part = line.split('?')[-1].strip()
            question_type = question_part.split()[0]
            if question_type in question_counts:
                question_counts[question_type] += 1
            else:
                question_counts[question_type] = 1

total_questions = sum(question_counts.values())

question_percentages = {q: round((count / total_questions * 100), 2) for q, count in question_counts.items()}

# Sort the question percentages dictionary by value in descending order
sorted_question_percentages = dict(sorted(question_percentages.items(), key=lambda item: item[1], reverse=True))

for question, percentage in sorted_question_percentages.items():
    print(f"{question}: {percentage}%")
