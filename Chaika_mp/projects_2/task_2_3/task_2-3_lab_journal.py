
researcher_name = input("ФИО исследователя: ")
experiment_date = input("Дата эксперимента (ДД.ММ.ГГГГ): ")
experiment_title = input("Название эксперимента: ")
conclusion = input("Вывод:\n")

frame_width = 50
header = "+-" + "-" * (frame_width - 2) + "-+\n"
line_template = "| {:<" + str(frame_width - 2) + "}|\n"
separator = header


with open('journal.txt', 'w', encoding="utf-8") as file:
    file.write(header)
    file.write(line_template.format("Электронный лабораторный журнал"))
    file.write(separator)
    
    file.write(line_template.format(f"ФИО исследователя : {researcher_name}"))
    file.write(line_template.format(f"Дата             : {experiment_date}"))
    file.write(line_template.format(f"Эксперимент      : {experiment_title}"))
    file.write(separator)

    file.write(line_template.format("Вывод:"))
    for line in conclusion.split("\n"):
        wrapped_lines = []
        while len(line) > frame_width - 2:
            idx = line[:frame_width - 2].rfind(" ") if " " in line else frame_width - 2
            wrapped_lines.append(line[:idx])
            line = line[idx + 1:]
        
        wrapped_lines.append(line)
        for wrapped_line in wrapped_lines:
            file.write(line_template.format(wrapped_line.strip()))
            
    file.write(separator)