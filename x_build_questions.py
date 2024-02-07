import re

def read_questions(questions_file):
    with open(questions_file, 'r') as file:
        return [line.strip() for line in file.readlines()]

def read_definitions(defs_file):
    # Read the definitions from defs.txt and store them in a dictionary
    defs = {}
    with open(defs_file, 'r') as file:
        content = file.read().split('\n\n')  # Split by double newline to separate each definition
        for block in content:
            lines = block.strip().split('\n')
            key = lines[0].split()[0]  # The key is the first word of the first line
            defs[key] = block
    return defs

def find_definition(defs, key, elements):
    # Find and return the definition corresponding to the key with replaced elements
    if key in defs:
        definition = defs[key]
        return definition
    else:
        return None

def extract_properties(definition, questions, elements):
    lines = definition.split('\n')
    unique_properties = set()

    # Placeholder substitution adjustment
    # Dynamically create the element map based on the placeholders found in the definition and elements provided
    placeholder_pattern = re.compile(r'\b(x|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|y|z)\b')
    all_placeholders = placeholder_pattern.findall(definition)
    unique_placeholders = sorted(set(all_placeholders), key=all_placeholders.index)  # Preserve order

    element_map = {ph: elements[i] for i, ph in enumerate(unique_placeholders) if i < len(elements)}

    for line in lines:
        for question in questions:
            if re.search(r'\b' + re.escape(question) + r'\b', line):
                substituted_line = line
                # Substitute placeholders with actual elements
                for placeholder, actual in element_map.items():
                    substituted_line = substituted_line.replace(placeholder, actual)

                # Extract and format questions correctly
                properties = re.findall(r'\b' + re.escape(question) + r'\b[^,]*', substituted_line)
                for property in properties:
                    clean_property = property.strip()
                    # Ensure the entire question is formulated correctly
                    formatted_property = clean_property.replace("x", elements[0])  # Replace 'x' if it's used differently
                    unique_properties.add(formatted_property)

    # Return a list of unique questions
    return list(unique_properties)


def process_tester(tester_file, defs, questions):
    shapes_questions_elements = {}
    with open(tester_file, 'r') as file, open('x_tester.txt', 'w') as outfile:
        for line in file:
            formulas = line.strip().split('; ')
            line_questions = []  # Store questions for the current line
            for formula in formulas:
                elements_str, key_and_elements = formula.split(' = ')
                key_parts = key_and_elements.split()
                key = key_parts[0]
                elements = key_parts[1:]
                print(f"\n\nkey: {key},\n elements_str: {elements_str},\n elements: {elements},\n definition: {defs[key]}\n\n")
                
                definition = find_definition(defs, key, elements)
                if definition:
                    if key not in shapes_questions_elements:
                        shapes_questions_elements[key] = {"elements": set(), "properties": set()}
                    shapes_questions_elements[key]["elements"].update(elements)
                    properties = extract_properties(definition, questions, elements)
                    for property in properties:
                        shapes_questions_elements[key]["properties"].add(property)
                        line_questions.append(property)

            # Write the current line with each question appended to tester2.txt
            for question in line_questions:
                outfile.write(f'{line.strip()} ? {question}\n')

    for key, data in shapes_questions_elements.items():
        data["elements"] = list(data["elements"])
        data["properties"] = list(data["properties"])
    return shapes_questions_elements


# Main script
defs = read_definitions('defs.txt')
questions = read_questions('list_of_questions.txt')
properties_dict = process_tester('tester3_full.txt', defs, questions)

for key, data in properties_dict.items():
    print(f"{key}:")
    print("  Elements:", ", ".join(data["elements"]))
    for property in data["properties"]:
        print(f"  - Question: {property}")