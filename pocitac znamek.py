import re
import tkinter as tk
from tkinter import ttk, messagebox
import random

# Globální proměnné pro uložení známek a vah
saved_grades = []
grades = []

def parse_grade(grade_str):
    """Zpracuje vstupní řetězec s možným mínusem, jako '1-' na 1.5."""
    if grade_str.endswith("-"):
        return float(grade_str[:-1]) + 0.5
    try:
        return float(grade_str)
    except ValueError:
        return None

def parse_weight(weight_str):
    """Zpracuje váhu a zajistí, že bude mít správný formát s dvěma desetinnými místy."""
    try:
        return round(float(weight_str), 2)
    except ValueError:
        return None

def calculate_expression(expression):
    try:
        expression = expression.replace("\u00d7", "*")
        result = eval(expression)
        return result
    except Exception as e:
        print(f"Chyba při zpracování výrazu: {e}")
        return None

def calculate_average(grades):
    if not grades:
        return 0
    total_weighted = sum(weight * grade for grade, weight in grades)
    total_weights = sum(weight for _, weight in grades)
    return total_weighted / total_weights if total_weights != 0 else 0

def format_for_set(grades):
    """Vrátí známky a váhy ve formátu pro SET."""
    if not grades:
        return "Žádné známky nejsou zadány."
    
    weights_sum = sum(weight for _, weight in grades)
    terms = [f"{weight:.2f}\u00d7{grade}" for grade, weight in grades]
    expression = " + ".join(terms)
    return f"({expression}) / ({weights_sum:.2f})"

# Funkce pro zpracování příkazů z konzole
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
        global saved_grades
        saved_grades = grades.copy()
        print("Známky a váhy byly uloženy.")
    elif command == "LOAD":
        if saved_grades:
            grades.clear()
            grades.extend(saved_grades)
            print("Známky a váhy byly načteny.")
        else:
            print("Žádné uložené známky nejsou k dispozici.")
    elif command == "DELSAVE":
        saved_grades.clear()
        print("Uložené známky a váhy byly smazány.")
    elif command == "RM":
        grades.clear()
        saved_grades.clear()
        print("Aktuální i uložené známky a váhy byly smazány.")
    elif command == "PRINT":
        print(format_for_set(grades))
    elif command == "HELP":
        show_help()
    elif command == "SEE":
        open_gui()
        return True
    elif command == "EXIT":
        print("Ukončuji aplikaci.")
        return False
    else:
        print("Neznámý příkaz. Zadej HELP pro nápovědu.")
    return True

def show_help():
    print("Dostupné příkazy:")
    print("- SET      Nastaví výchozí průměr pomocí výpočetního vzorce")
    print("- ADD      Přidání nové známky a váhy (např. ADD 2 0.5, 3 0.25)")
    print("- SHOW:    Zobrazí aktuální známky a váhy")
    print("- CALC:    Spočítá aktuální průměr")
    print("- DEL:     Smaže všechny známky a váhy")
    print("- SAVE:    Uloží aktuální známky a váhy")
    print("- LOAD:    Načte dříve uložené známky a váhy")
    print("- DELSAVE: Smaže uložené známky a váhy")
    print("- PRINT:   Zobrazí známky a váhy ve formátu pro SET")
    print("- RM:      Smaže aktuální i uložené známky a váhy")
    print("- SEE:     Otevře grafické uživatelské rozhraní")
    print("- HELP:    Zobrazí tento seznam příkazů")
    print("- EXIT:    Ukončí aplikaci")

# GUI funkce
class GradeCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kalkulátor známek")
        self.geometry("800x600")
        self.configure(bg="#f5f5f5")
        
        # Proměnné pro ukládání uživatelského vstupu
        self.grade_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.expression_var = tk.StringVar()
        self.result_var = tk.StringVar(value="Průměr: 0.00")
        
        self.create_widgets()
        self.update_grade_list()
        self.calculate_average()
        
        # Nastavení ikon a stylů
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 10), padding=5)
        self.style.configure("TLabel", font=("Segoe UI", 11), background="#f5f5f5")
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), background="#f5f5f5")
        self.style.configure("Result.TLabel", font=("Segoe UI", 16, "bold"), background="#f5f5f5", foreground="#2c3e50")
        
        # Animace při spuštění
        self.after(100, self.animate_start)
        
    def animate_start(self):
        """Jednoduchá animace při spuštění aplikace"""
        for widget in self.winfo_children():
            widget.place_forget()
        
        for i, widget in enumerate(self.winfo_children()):
            self.after(i * 50, lambda w=widget: w.place(w.place_info()))
    
    def create_widgets(self):
        # Hlavní rámce
        self.header_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=10)
        self.header_frame.pack(fill="x")
        
        self.main_frame = tk.Frame(self, bg="#f5f5f5")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.left_frame = tk.Frame(self.main_frame, bg="#f5f5f5", width=350)
        self.left_frame.pack(side="left", fill="both", padx=(0, 10))
        
        self.right_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        self.right_frame.pack(side="right", fill="both", expand=True)
        
        # Nadpis
        self.title_label = ttk.Label(self.header_frame, text="Kalkulátor známek", style="Header.TLabel")
        self.title_label.pack(pady=10)
        
        # Sekce pro přidání známky
        self.input_frame = tk.LabelFrame(self.left_frame, text="Přidat známku", bg="#f5f5f5", font=("Segoe UI", 11), padx=10, pady=10)
        self.input_frame.pack(fill="x", pady=10)
        
        # Vstupní pole pro známku
        self.grade_label = ttk.Label(self.input_frame, text="Známka:", style="TLabel")
        self.grade_label.grid(row=0, column=0, sticky="w", pady=5)
        
        self.grade_entry = ttk.Entry(self.input_frame, textvariable=self.grade_var, width=10)
        self.grade_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Vstupní pole pro váhu
        self.weight_label = ttk.Label(self.input_frame, text="Váha:", style="TLabel")
        self.weight_label.grid(row=1, column=0, sticky="w", pady=5)
        
        self.weight_entry = ttk.Entry(self.input_frame, textvariable=self.weight_var, width=10)
        self.weight_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Tlačítko pro přidání známky
        self.add_button = ttk.Button(self.input_frame, text="Přidat", command=self.add_grade)
        self.add_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        
        # Sekce pro nastavení pomocí výrazu
        self.expression_frame = tk.LabelFrame(self.left_frame, text="Nastavit pomocí výrazu", bg="#f5f5f5", font=("Segoe UI", 11), padx=10, pady=10)
        self.expression_frame.pack(fill="x", pady=10)
        
        self.expression_label = ttk.Label(self.expression_frame, text="Výraz:", style="TLabel")
        self.expression_label.grid(row=0, column=0, sticky="w", pady=5)
        
        self.expression_entry = ttk.Entry(self.expression_frame, textvariable=self.expression_var, width=30)
        self.expression_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.set_button = ttk.Button(self.expression_frame, text="Nastavit", command=self.set_expression)
        self.set_button.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        
        # Akční tlačítka
        self.actions_frame = tk.LabelFrame(self.left_frame, text="Akce", bg="#f5f5f5", font=("Segoe UI", 11), padx=10, pady=10)
        self.actions_frame.pack(fill="x", pady=10)
        
        self.calc_button = ttk.Button(self.actions_frame, text="Spočítat průměr", command=self.calculate_average)
        self.calc_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        self.save_button = ttk.Button(self.actions_frame, text="Uložit známky", command=self.save_grades)
        self.save_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        self.load_button = ttk.Button(self.actions_frame, text="Načíst známky", command=self.load_grades)
        self.load_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        self.del_button = ttk.Button(self.actions_frame, text="Smazat známky", command=self.del_grades)
        self.del_button.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        self.delsave_button = ttk.Button(self.actions_frame, text="Smazat uložené", command=self.delsave_grades)
        self.delsave_button.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        self.rm_button = ttk.Button(self.actions_frame, text="Smazat vše", command=self.rm_grades)
        self.rm_button.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        
        # Výsledek
        self.result_frame = tk.Frame(self.left_frame, bg="#f5f5f5", padx=10, pady=10)
        self.result_frame.pack(fill="x", pady=10)
        
        self.result_label = ttk.Label(self.result_frame, textvariable=self.result_var, style="Result.TLabel")
        self.result_label.pack(pady=10)
        
        # Seznam známek
        self.grades_frame = tk.LabelFrame(self.right_frame, text="Seznam známek", bg="#f5f5f5", font=("Segoe UI", 11), padx=10, pady=10)
        self.grades_frame.pack(fill="both", expand=True, pady=10)
        
        # Tabulka známek
        columns = ("grade", "weight")
        self.grades_tree = ttk.Treeview(self.grades_frame, columns=columns, show="headings", selectmode="browse")
        
        self.grades_tree.heading("grade", text="Známka")
        self.grades_tree.heading("weight", text="Váha")
        
        self.grades_tree.column("grade", width=100, anchor="center")
        self.grades_tree.column("weight", width=100, anchor="center")
        
        self.grades_tree.pack(fill="both", expand=True, pady=10)
        
        # Scrollbar pro tabulku
        self.scrollbar = ttk.Scrollbar(self.grades_tree, orient="vertical", command=self.grades_tree.yview)
        self.grades_tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        
        # Tlačítko pro odstranění vybrané známky
        self.remove_button = ttk.Button(self.grades_frame, text="Odstranit vybranou známku", command=self.remove_selected_grade)
        self.remove_button.pack(fill="x", pady=5)
        
        # Tooltips
        self.create_tooltips()
    
    def create_tooltips(self):
        self.add_tooltip(self.grade_entry, "Zadejte známku (např. 1, 2, 3, 1-, 2-)")
        self.add_tooltip(self.weight_entry, "Zadejte váhu známky (např. 0.5, 1, 2)")
        self.add_tooltip(self.add_button, "Přidat novou známku do seznamu")
        self.add_tooltip(self.expression_entry, "Zadejte výraz ve formátu (0.5×1 + 1×2) / (1.5)")
        self.add_tooltip(self.set_button, "Nastavit známky podle zadaného výrazu")
        self.add_tooltip(self.calc_button, "Spočítat vážený průměr známek")
        self.add_tooltip(self.save_button, "Uložit aktuální seznam známek")
        self.add_tooltip(self.load_button, "Načíst dříve uložené známky")
        self.add_tooltip(self.del_button, "Smazat všechny známky v seznamu")
        self.add_tooltip(self.delsave_button, "Smazat uložené známky")
        self.add_tooltip(self.rm_button, "Smazat aktuální i uložené známky")
        self.add_tooltip(self.remove_button, "Odebrat vybranou známku ze seznamu")
    
    def add_tooltip(self, widget, text):
        tooltip = ToolTip(widget, text)
    
    def add_grade(self):
        grade_str = self.grade_var.get().strip()
        weight_str = self.weight_var.get().strip()
        
        grade = parse_grade(grade_str)
        weight = parse_weight(weight_str)
        
        if grade is None or weight is None:
            messagebox.showerror("Chyba", "Neplatná známka nebo váha. Zkontrolujte vstupní hodnoty.")
            return
        
        global grades
        grades.append((grade, weight))
        
        self.grade_var.set("")
        self.weight_var.set("")
        
        self.update_grade_list()
        self.calculate_average()
        self.flash_feedback("Známka přidána")
    
    def set_expression(self):
        expression = self.expression_var.get().strip()
        if not expression:
            messagebox.showwarning("Upozornění", "Zadejte platný výraz.")
            return
        
        try:
            result = calculate_expression(expression)
            if result is not None:
                matches = re.findall(r"([\d.-]+)\s*\u00d7\s*([\d.]+)", expression)
                
                global grades
                grades = [(parse_grade(g), parse_weight(w)) for w, g in matches]
                
                self.update_grade_list()
                self.calculate_average()
                self.flash_feedback(f"Výchozí známky nastaveny, průměr: {result:.2f}")
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba při zpracování výrazu: {e}")
    
    def update_grade_list(self):
        # Vyčistit tabulku
        for item in self.grades_tree.get_children():
            self.grades_tree.delete(item)
        
        # Naplnit tabulku
        for i, (grade, weight) in enumerate(grades):
            self.grades_tree.insert("", "end", values=(grade, weight), tags=(f"row{i % 2}",))
        
        # Nastavit styly řádků pro lepší čitelnost
        self.grades_tree.tag_configure("row0", background="#f9f9f9")
        self.grades_tree.tag_configure("row1", background="#efefef")
    
    def calculate_average(self):
        global grades
        average = calculate_average(grades)
        self.result_var.set(f"Průměr: {average:.2f}")
        
        # Změna barvy podle průměru
        if average <= 1.5:
            self.result_label.configure(foreground="#27ae60")  # zelená
        elif average <= 2.5:
            self.result_label.configure(foreground="#2980b9")  # modrá
        elif average <= 3.5:
            self.result_label.configure(foreground="#f39c12")  # oranžová
        else:
            self.result_label.configure(foreground="#c0392b")  # červená
    
    def save_grades(self):
        global saved_grades, grades
        saved_grades = grades.copy()
        self.flash_feedback("Známky uloženy")
    
    def load_grades(self):
        global saved_grades, grades
        if saved_grades:
            grades = saved_grades.copy()
            self.update_grade_list()
            self.calculate_average()
            self.flash_feedback("Známky načteny")
        else:
            messagebox.showinfo("Info", "Žádné uložené známky nejsou k dispozici.")
    
    def del_grades(self):
        global grades
        if messagebox.askyesno("Potvrzení", "Opravdu chcete smazat všechny známky?"):
            grades.clear()
            self.update_grade_list()
            self.calculate_average()
            self.flash_feedback("Známky smazány")
    
    def delsave_grades(self):
        global saved_grades
        if messagebox.askyesno("Potvrzení", "Opravdu chcete smazat uložené známky?"):
            saved_grades.clear()
            self.flash_feedback("Uložené známky smazány")
    
    def rm_grades(self):
        global grades, saved_grades
        if messagebox.askyesno("Potvrzení", "Opravdu chcete smazat všechny aktuální i uložené známky?"):
            grades.clear()
            saved_grades.clear()
            self.update_grade_list()
            self.calculate_average()
            self.flash_feedback("Všechny známky smazány")
    
    def remove_selected_grade(self):
        global grades
        selected_item = self.grades_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Vyberte známku, kterou chcete odstranit.")
            return
        
        item_index = self.grades_tree.index(selected_item[0])
        if 0 <= item_index < len(grades):
            del grades[item_index]
            self.update_grade_list()
            self.calculate_average()
            self.flash_feedback("Známka odstraněna")
    
    def flash_feedback(self, message):
        """Zobrazí krátkou zpětnou vazbu na obrazovce"""
        feedback = tk.Label(self, text=message, font=("Segoe UI", 12), 
                           bg="#333333", fg="white", padx=15, pady=8)
        feedback.place(relx=0.5, rely=0.9, anchor="center")
        
        # Zaoblené rohy pomocí border-radius
        feedback.configure(relief="flat", borderwidth=0)
        
        # Postupné mizení
        self.after(2000, lambda: feedback.destroy())

# Třída pro vytvoření tooltipu
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        # Vytvoření tooltip okna
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", 
                         relief="solid", borderwidth=1, font=("Segoe UI", 9))
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def open_gui():
    app = GradeCalculator()
    app.mainloop()

def main():
    print("Aplikace pro výpočet průměru známek. Zadej HELP pro nápovědu.")
    
    while True:
        input_commands = input("Zadej příkaz: ").strip().upper()
        commands = input_commands.split("*")
        for command in commands:
            if not process_command(command.strip()):
                return

if __name__ == "__main__":
    main()