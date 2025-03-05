import re

def parse_grade(grade_str):
    """Zpracuje vstupní řetězec s možným mínusem, jako '1-' na 1.5."""
    if grade_str.endswith("-"):
        # Přidáme 0.5 k hodnotě, pokud končí znakem '-'
        return float(grade_str[:-1]) + 0.5
    return float(grade_str)

def parse_weight(weight_str):
    """Zpracuje váhu a zajistí, že bude mít správný formát s dvěma desetinnými místy."""
    return round(float(weight_str), 2)

def calculate_expression(expression):
    try:
        # Nahradíme symboly "×" za "*", aby Python zvládl výpočet
        expression = expression.replace("×", "*")
        # Vypočítáme výsledek zadaného výrazu
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
    print(" ")
    print("- SET    (0.5×1 + 0.25×2) / (0.5 + 0.25): Nastaví výchozí průměr")
    print("- ADD    grade weight: Přidá novou známku a váhu (např. ADD 2 0.5)")
    print("- SHOW:  Zobrazí aktuální známky a váhy")
    print("- CALC:  Spočítá aktuální průměr")
    print("- DEL:   Smaže všechny známky a váhy")
    print("- HELP:  Zobrazí tento seznam příkazů")
    print("- EXIT:  Ukončí aplikaci")
    print(" ")

def main():
    grades = []
    print("Aplikace pro výpočet průměru známek. Zadej HELP pro nápovědu.")
    
    while True:
        command = input("Zadej příkaz: ").strip().upper()
        if command.startswith("SET"):
            try:
                expression = command[4:].strip()  # Získá výraz po "SET"
                result = calculate_expression(expression)
                if result is not None:
                    # Extrahujeme jednotlivé známky a váhy z výrazu
                    matches = re.findall(r"([\d.-]+)\s*×\s*([\d.]+)", expression)
                    grades = [(parse_grade(g), parse_weight(w)) for g, w in matches]
                    print(f"Výchozí známky a váhy byly nastaveny. Průměr: {result:.2f}")
            except Exception as e:
                print(f"Chyba při nastavování: {e}")
        elif command.startswith("ADD"):
            try:
                _, grade, weight = command.split()
                grade = parse_grade(grade)  # Zpracujeme známku se znaménkem
                weight = parse_weight(weight)  # Zpracujeme váhu s dvěma desetinnými místy
                grades.append((grade, weight))
                print(f"Přidána známka {grade} s váhou {weight}.")
            except ValueError:
                print("Chybný formát. Použij: ADD grade weight")
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
        elif command == "HELP":
            show_help()
        elif command == "EXIT":
            print("Ukončuji aplikaci.")
            break
        else:
            print("Neznámý příkaz. Zadej HELP pro nápovědu.")

if __name__ == "__main__":
    main()
