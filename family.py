import tkinter as tk
from tkinter import messagebox
import csv

class ExpenseCategory:
    def __init__(self, name, limit=0, value=0):
        self.name = name  # Название категории
        self.limit = limit  # Лимит расходов
        self.value = value  # Значение расходов

class FamilyBudgetExpertSystem:
    def __init__(self):
        self.income = 0
        self.expenses = {
            'жилищные расходы': ExpenseCategory('жилищные расходы'),
            'еда': ExpenseCategory('еда'),
            'транспорт': ExpenseCategory('транспорт'),
            'развлечения': ExpenseCategory('развлечения'),
            'сбережения': ExpenseCategory('сбережения'),
            'долги': ExpenseCategory('долги')
        }
        self.savings_goal = 0
        self.monthly_savings = 0

    def set_income(self, income):
        self.income = income

    def set_expenses(self, category, amount):
        if category in self.expenses:
            self.expenses[category].value = amount

    def set_savings_goal(self, goal):
        self.savings_goal = goal

    def set_monthly_savings(self, savings):
        self.monthly_savings = savings

    def set_category_limit(self, category, limit):
        if category in self.expenses:
            self.expenses[category].limit = limit

    def calculate_balance(self):
        total_expenses = sum(cat.value for cat in self.expenses.values())
        balance = self.income - total_expenses
        return balance

    def recommend_budget(self):
        balance = self.calculate_balance()
        recommendations = []

        if self.monthly_savings < self.savings_goal:
            recommendations.append("Рекомендуется увеличить сбережения на минимум 10% от дохода.")
        
        for cat_name, cat in self.expenses.items():
            if cat.value > self.income * 0.3:
                recommendations.append(f"Сократите расходы на '{cat_name}'.")

            if cat.value > cat.limit:
                recommendations.append(f"Расходы на '{cat_name}' превышают установленный лимит!")

        if balance < 0:
            recommendations.append("Ваши расходы превышают доходы. Необходимо сократить затраты.")
        elif balance < self.income * 0.1:
            recommendations.append("Ваш баланс близок к нулю. Попробуйте откладывать больше.")

        return recommendations

    def get_over_limit_expenses(self):
        over_limit = [cat.name for cat in self.expenses.values() if cat.value > cat.limit]
        return over_limit if over_limit else ["Нет категорий с превышением лимитов."]

    def get_expense_distribution(self):
        total_expenses = sum(cat.value for cat in self.expenses.values())
        if total_expenses == 0:
            return "Нет расходов для распределения."
        distribution = {cat.name: (cat.value / total_expenses) * 100 for cat in self.expenses.values()}
        return distribution

    def save_to_csv(self, filename="budget_data.csv"):
        data = {
            "Доход": self.income,
            **{cat.name: cat.value for cat in self.expenses.values()},
            "Цель по сбережениям": self.savings_goal,
            "Месячные сбережения": self.monthly_savings,
            **{f"Лимит на {cat.name}": cat.limit for cat in self.expenses.values()}
        }
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for key, value in data.items():
                writer.writerow([key, value])
        return filename

class BudgetApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Интеллектуальная экспертная система для семейного бюджета")
        self.master.geometry("600x350")
        self.expert_system = FamilyBudgetExpertSystem()

        self.income_var = tk.DoubleVar()
        self.expense_vars = {category: tk.DoubleVar() for category in self.expert_system.expenses}
        self.savings_goal_var = tk.DoubleVar()
        self.monthly_savings_var = tk.DoubleVar()
        self.category_limit_vars = {category: tk.DoubleVar() for category in self.expert_system.expenses}

        self.title_label = tk.Label(master, text="Формирование семейного бюджета", font=("Helvetica", 16))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.income_label = tk.Label(master, text="Доход семьи (руб.):")
        self.income_label.grid(row=1, column=0, padx=10, pady=5)
        self.income_entry = tk.Entry(master, textvariable=self.income_var)
        self.income_entry.grid(row=1, column=1, padx=10, pady=5)

        row_index = 2
        for category in self.expert_system.expenses:
            label = tk.Label(master, text=f"{category.capitalize()} (руб.):")
            label.grid(row=row_index, column=0, padx=10, pady=5)
            entry = tk.Entry(master, textvariable=self.expense_vars[category])
            entry.grid(row=row_index, column=1, padx=10, pady=5)
            row_index += 1

        self.savings_goal_label = tk.Label(master, text="Цель по сбережениям (руб.):")
        self.savings_goal_label.grid(row=row_index, column=0, padx=10, pady=5)
        self.savings_goal_entry = tk.Entry(master, textvariable=self.savings_goal_var)
        self.savings_goal_entry.grid(row=row_index, column=1, padx=10, pady=5)
        row_index += 1

        self.monthly_savings_label = tk.Label(master, text="Месячные сбережения (руб.):")
        self.monthly_savings_label.grid(row=row_index, column=0, padx=10, pady=5)
        self.monthly_savings_entry = tk.Entry(master, textvariable=self.monthly_savings_var)
        self.monthly_savings_entry.grid(row=row_index, column=1, padx=10, pady=5)
        row_index += 1

        self.category_limit_labels = []
        self.category_limit_entries = []
        for category in self.expert_system.expenses:
            label = tk.Label(master, text=f"Лимит по '{category.capitalize()}' (руб.):")
            label.grid(row=row_index, column=0, padx=10, pady=5)
            entry = tk.Entry(master, textvariable=self.category_limit_vars[category])
            entry.grid(row=row_index, column=1, padx=10, pady=5)
            row_index += 1

        self.buttons_frame = tk.Frame(master)
        self.buttons_frame.grid(row=0, column=2, rowspan=row_index, padx=10, pady=10, sticky="n")

        self.calculate_button = tk.Button(self.buttons_frame, text="Рассчитать баланс", command=self.calculate_balance)
        self.calculate_button.grid(row=0, column=0, pady=10)

        self.recommendations_button = tk.Button(self.buttons_frame, text="Получить рекомендации", command=self.give_recommendations)
        self.recommendations_button.grid(row=1, column=0, pady=10)

        self.optimize_expenses_button = tk.Button(self.buttons_frame, text="Оптимизировать расходы", command=self.optimize_expenses)
        self.optimize_expenses_button.grid(row=2, column=0, pady=10)

        self.check_savings_button = tk.Button(self.buttons_frame, text="Проверить сбережения", command=self.check_savings)
        self.check_savings_button.grid(row=3, column=0, pady=10)

        self.show_over_limit_button = tk.Button(self.buttons_frame, text="Показать превышения лимитов", command=self.show_over_limit_expenses)
        self.show_over_limit_button.grid(row=4, column=0, pady=10)

        self.show_distribution_button = tk.Button(self.buttons_frame, text="Показать распределение расходов", command=self.show_expense_distribution)
        self.show_distribution_button.grid(row=5, column=0, pady=10)

        self.result_label = tk.Label(master, text="Результат будет отображен здесь", width=50, height=5, relief="solid")
        self.result_label.grid(row=row_index, column=0, columnspan=2, padx=10, pady=10)

    def calculate_balance(self):
        self.expert_system.set_income(self.income_var.get())
        for category, var in self.expense_vars.items():
            self.expert_system.set_expenses(category, var.get())
        for category, var in self.category_limit_vars.items():
            self.expert_system.set_category_limit(category, var.get())
        balance = self.expert_system.calculate_balance()
        self.result_label.config(text=f"Баланс: {balance:.2f} руб.", bg="green" if balance >= 0 else "red")

    def give_recommendations(self):
        recommendations = self.expert_system.recommend_budget()
        messagebox.showinfo("Рекомендации", "\n".join(recommendations))

    def optimize_expenses(self):
        recommendations = ["Сократите расходы на жилье до 30% от дохода.", "Уменьшите расходы на развлечения."]
        messagebox.showinfo("Оптимизация расходов", "\n".join(recommendations))

    def check_savings(self):
        savings_report = f"Цель по сбережениям: {self.savings_goal_var.get()} руб.\nМесячные сбережения: {self.monthly_savings_var.get()} руб."
        messagebox.showinfo("Сбережения", savings_report)

    def show_over_limit_expenses(self):
        over_limit = self.expert_system.get_over_limit_expenses()
        messagebox.showinfo("Превышения лимитов", "\n".join(over_limit))

    def show_expense_distribution(self):
        distribution = self.expert_system.get_expense_distribution()
        if isinstance(distribution, str):  # Если нет данных для распределения
            messagebox.showinfo("Распределение расходов", distribution)
        else:
            dist_text = "\n".join([f"{cat}: {perc:.1f}%" for cat, perc in distribution.items()])
            messagebox.showinfo("Распределение расходов", dist_text)

# Главная функция для запуска приложения
def main():
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
