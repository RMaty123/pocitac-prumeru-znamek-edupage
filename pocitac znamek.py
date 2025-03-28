import re

# Globální proměnná pro uložení známek a vah
saved_grades = []

def parse_grade(grade_str):
    """Zpracuje vstupní řetězec s možným mínusem, jako '1-' na 1.5."""
    if grade_str.endswith("-"):
        return float(grade_str[:-1]) + 0.5
    return float(grade_str)

def parse_weight(weight_str):
    """Zpracuje váhu a zajistí, že bude mít správný formát s dvěma desetinnými místy."""
    return round(float(weight_str), 2)

def calculate_expression(expression):
    try:
        expression = expression.replace("\u00d7", "*")
        result = eval(expression)
        return result
    except Exception as e:
        print(f"Chyba při zpracování výrazu: {e}")
        return None

def calculate_average(grades):
    total_weighted = sum(weight * grade for grade, weight in grades)
    total_weights = sum(weight for _, weight in grades)
    return total_weighted / total_weights if total_weights != 0 else 0

def show_help():
    print("Dostupné příkazy:")
    print("- SET      Nastaví výchozí průměr pomocí výpočetního vzorce")
    print("- ADD      Přidá nové známky a váhy (např. ADD 2 0.5, 3 0.25)")
    print("- SHOW:    Zobrazí aktuální známky a váhy")
    print("- CALC:    Spočítá aktuální průměr")
    print("- DEL:     Smaže všechny známky a váhy")
    print("- SAVE:    Uloží aktuální známky a váhy")
    print("- LOAD:    Načte dříve uložené známky a váhy")
    print("- DELSAVE: Smaže uložené známky a váhy")
    print("- PRINT:   Zobrazí známky a váhy ve formátu pro SET")
    print("- RM:      Smaže aktuální i uložené známky a váhy")
    print("- HELP:    Zobrazí tento seznam příkazů")
    print("- EXIT:    Ukončí aplikaci")

def save_grades():
    global saved_grades
    saved_grades = grades.copy()
    print("Známky a váhy byly uloženy.")

def load_grades():
    global grades
    if saved_grades:
        grades.clear()
        grades.extend(saved_grades)
        print("Známky a váhy byly načteny.")
    else:
        print("Žádné uložené známky nejsou k dispozici.")

def delsave_grades():
    global saved_grades
    saved_grades.clear()
    print("Uložené známky a váhy byly smazány.")

def rm_grades():
    """Smaže aktuální i uložené známky a váhy."""
    global grades, saved_grades
    grades.clear()
    saved_grades.clear()
    print("Aktuální i uložené známky a váhy byly smazány.")

def format_for_set(grades):
    """Vrátí známky a váhy ve formátu pro SET."""
    if not grades:
        return "Žádné známky nejsou zadány."
    
    weights_sum = sum(weight for _, weight in grades)
    terms = [f"{weight:.2f}\u00d7{grade}" for grade, weight in grades]
    expression = " + ".join(terms)
    return f"({expression}) / ({weights_sum:.2f})"

def process_command(command):
    global grades
    if command.startswith("SET"):
        try:
            expression = command[4:].strip()
            result = calculate_expression(expression)
            if result is not None:
                matches = re.findall(r"([\d.-]+)\s*\u00d7\s*([\d.]+)", expression)
                grades = [(parse_grade(g), parse_weight(w)) for w, g in matches]
                print(f"Výchozí známky a váhy byly nastaveny. Průměr: {result:.2f}")
        except Exception as e:
            print(f"Chyba při nastavování: {e}")
    elif command.startswith("ADD"):
        try:
            entries = command[4:].strip().split(",")
            for entry in entries:
                grade, weight = entry.strip().split()
                grade = parse_grade(grade)
                weight = parse_weight(weight)
                grades.append((grade, weight))
            print(f"Přidány známky a váhy: {', '.join(entries)}.")
        except ValueError:
            print("Chybný formát. Ověřte správnost v manuálu, správně: známka váha, známka váha")
    elif command == "SHOW":
        if grades:
            print("Známky a váhy:")
            for grade, weight in grades:
                print(f"Známka: {grade}, Váha: {weight}")
        else:
            print("Žádné známky nejsou zadány.")
    elif command == "CALC":
        average = calculate_average(grades)
        print(f"Aktuální vážený průměr je: {average:.2f}")
    elif command == "DEL":
        grades.clear()
        print("Všechny známky a váhy byly smazány.")
    elif command == "SAVE":
        save_grades()
    elif command == "LOAD":
        load_grades()
    elif command == "DELSAVE":
        delsave_grades()
    elif command == "RM":
        rm_grades()
    elif command == "PRINT":
        print(format_for_set(grades))
    elif command == "HELP":
        show_help()
    elif command == "EXIT":
        print("Ukončuji aplikaci.")
        return False
    else:
        print("Neznámý příkaz. Zadej HELP pro nápovědu.")
    return True

def main():
    global grades
    grades = []
    print("Aplikace pro výpočet průměru známek. Zadej HELP pro nápovědu.")
    
    while True:
        input_commands = input("Zadej příkaz: ").strip().upper()
        commands = input_commands.split("*")
        for command in commands:
            if not process_command(command.strip()):
                return

if __name__ == "__main__":
    main()
