import tkinter as tk
from tkinter import messagebox
from io import open


 

class Recipe:
    def __init__(self, name: str, ingredients: list, instructions: str, dish_type: str, difficulty: str):
        self.name = name  # str
        self.ingredients = ingredients  # list
        self.instructions = instructions  # str
        self.dish_type = dish_type  # str
        self.difficulty = difficulty  # str

    def edit_recipe(self, name=None, ingredients=None, instructions=None, dish_type=None, difficulty=None):
        self.name = name if name is not None else self.name
        self.ingredients = ingredients if ingredients is not None else self.ingredients
        self.instructions = instructions if instructions is not None else self.instructions
        self.dish_type = dish_type if dish_type is not None else self.dish_type
        self.difficulty = difficulty if difficulty is not None else self.difficulty


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Recipe Organizer")
        self.geometry("600x500")
        self.configure(bg="lightblue")

        self.recipes = []
        self.recipes = load_recipes_from_file()

        self.create_widgets()

    def on_closing(self):
        save_recipes_to_file(self.recipes)  
        self.destroy()   
        

    def create_widgets(self):
        self.label = tk.Label(self, text="Welcome to the Recipe Organizer", font=("Helvetica", 24, "bold"), foreground="#333", background="lightblue")
        self.label.pack(pady=10)

        self.frame = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.frame.pack(pady=5, fill=tk.BOTH, expand=True)

        self.add_recipe_button = tk.Button(self.frame, text="Add Recipe", command=self.open_add_recipe_window, 
                                     relief=tk.RAISED, bg="lightgreen", fg="black", font=("Arial", 12))
        self.add_recipe_button.pack(pady=5)
        self.add_recipe_button.bind("<Enter>", lambda e: self.add_recipe_button.config(bg="#90EE90"))  # Світліший зелений
        self.add_recipe_button.bind("<Leave>", lambda e: self.add_recipe_button.config(bg="lightgreen"))

        self.search_recipes_button = tk.Button(self.frame, text="Show Recipes based on Ingredients", 
                                            command=self.open_search_recipes_window, relief=tk.RAISED, 
                                            bg="lightblue", fg="black", font=("Arial", 12))
        self.search_recipes_button.pack(pady=5)
        self.search_recipes_button.bind("<Enter>", lambda e: self.search_recipes_button.config(bg="#ADD8E6"))  # Світліший блакитний
        self.search_recipes_button.bind("<Leave>", lambda e: self.search_recipes_button.config(bg="lightblue"))

        self.delete_recipe_button = tk.Button(self.frame, text="Delete Recipe", command=self.delete_recipe, 
                                            relief=tk.RAISED, bg="lightpink", fg="black", font=("Arial", 12))
        self.delete_recipe_button.pack(pady=5)
        self.delete_recipe_button.bind("<Enter>", lambda e: self.delete_recipe_button.config(bg="#FFB6C1"))  # Світліший рожевий
        self.delete_recipe_button.bind("<Leave>", lambda e: self.delete_recipe_button.config(bg="lightpink"))

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # Встановлення обробника події закриття вікна

        self.recipe_list.bind("<Double-Button-1>", self.show_recipe_instructions)

        self.update_recipe_list()

    def show_recipe_instructions(self, event):
        # Отримання індексу обраного рецепту
        selected_index = self.recipe_list.curselection()
        if selected_index:
            # Отримання обраного рецепту
            selected_recipe = self.recipes[selected_index[0]]
            # Створення діалогового вікна для відображення інструкцій рецепту
            instructions_window = tk.Toplevel(self)
            instructions_window.title("Recipe Instructions")
            instructions_window.geometry("400x300")

        # Додавання мітки з інгредієнтами рецепту до діалогового вікна
        ingredients_label = tk.Label(instructions_window, text="Ingredients:", font=("Arial", 12, "bold"), background="#e5fcb3")
        ingredients_label.pack(pady=5)
        ingredients_text = tk.Text(instructions_window, wrap=tk.WORD, height=8, width=50)
        ingredients_text.insert(tk.END, "\n".join(selected_recipe.ingredients))
        ingredients_text.config(state=tk.DISABLED)  # Заборона редагування тексту
        ingredients_text.pack(pady=5)  

        # Додавання мітки з інструкціями рецепту до діалогового вікна
        instructions_label = tk.Label(instructions_window, text="Instructions:", font=("Arial", 12, "bold"), background="#e5fcb3")
        instructions_label.pack(pady=5)
        instructions_text = tk.Text(instructions_window, wrap=tk.WORD, height=8, width=50)
        instructions_text.insert(tk.END, selected_recipe.instructions)
        instructions_text.config(state=tk.DISABLED)  # Заборона редагування тексту
        instructions_text.pack(pady=5)



    def open_add_recipe_window(self):
        add_recipe_window = AddRecipeWindow(self)

    def open_search_recipes_window(self):
        search_recipes_window = SearchRecipesWindow(self)

    def update_recipes(self, recipe: Recipe):
        self.recipes.append(recipe)
        self.update_recipe_list()

    def delete_recipe(self):
        selected_index = self.recipe_list.curselection()
        if selected_index:
            recipe_name = self.recipe_list.get(selected_index)
            confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete the recipe '{recipe_name}'?")
            if confirmation:
                self.recipes.pop(selected_index[0])
                self.update_recipe_list()

    def update_recipe_list(self):
        self.recipe_list.delete(0, tk.END)
        for recipe in self.recipes:
            self.recipe_list.insert(tk.END, recipe.name)

class AddRecipeWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Add Recipe")
        self.geometry("400x450")
        self.configure(bg="#a882fa")

        self.create_widgets()

    def create_widgets(self):
        self.name_label = tk.Label(self, text="Name:")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=5)

        self.ingredients_label = tk.Label(self, text="Ingredients (separated by comma):")
        self.ingredients_label.pack(pady=5)
        self.ingredients_entry = tk.Entry(self)
        self.ingredients_entry.pack(pady=5)

        self.instructions_label = tk.Label(self, text="Instructions:")
        self.instructions_label.pack(pady=5)
        self.instructions_entry = tk.Text(self, height=10, width=40)
        self.instructions_entry.pack(pady=5)

        self.add_button = tk.Button(self, text="Add Recipe", command=self.add_recipe, background="#e5fcb3")
        self.add_button.pack(pady=5)

    def add_recipe(self):
        name = self.name_entry.get().strip()
        ingredients = [ingredient.strip() for ingredient in self.ingredients_entry.get().split(',')]
        instructions = self.instructions_entry.get("1.0", tk.END).strip()

        if not name or not ingredients or not instructions:
            messagebox.showerror("Error", "Invalid format of ingredient.")
            return

        recipe = Recipe(name, ingredients, instructions, "", "")
        self.master.update_recipes(recipe)
        self.destroy()

class SearchRecipesWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Search Recipes")
        self.geometry("400x100")
        self.configure(bg="#a882fa")

        self.create_widgets()

    def create_widgets(self):
        self.ingredients_label = tk.Label(self, text="Enter available ingredients (separated by comma):" )
        self.ingredients_label.pack(pady=5)
        self.ingredients_entry = tk.Entry(self)
        self.ingredients_entry.pack(pady=5)

        self.search_button = tk.Button(self, text="Search", command=self.find_recipes, background="#e5fcb3")
        self.search_button.pack(pady=5)

    def find_recipes(self):
        available_ingredients = set(ingredient.strip().lower() for ingredient in self.ingredients_entry.get().split(','))
        matching_recipes = []

        for recipe in self.master.recipes:  
            recipe_ingredients = set(ingredient.lower() for ingredient in recipe.ingredients)
            if available_ingredients.issubset(recipe_ingredients):
                matching_recipes.append(recipe.name)

        result_window = tk.Toplevel(self)
        result_window.title("Search Results")
        result_window.geometry("400x300")
        self.configure(bg="#a882fa")

        if matching_recipes:
            result_label = tk.Label(result_window, text="Recipes that you can make with your ingredients:")
            result_label.pack(pady=5)

            recipe_list = tk.Listbox(result_window)
            recipe_list.pack(pady=5)

            for recipe in matching_recipes:
                recipe_list.insert(tk.END, recipe)
        else:
            result_label = tk.Label(result_window, text="Unfortunately, no recipes were found based on your query.")
            result_label.pack(pady=5)


    def save_recipe(self):
        name = self.name_entry.get().strip()
        ingredients = [ingredient.strip() for ingredient in self.ingredients_entry.get().split(',')]
        instructions = self.instructions_entry.get("1.0", tk.END).strip()
        dish_type = self.dish_type_entry.get().strip()
        difficulty = self.difficulty_entry.get().strip()

        if not name or not ingredients or not instructions or not dish_type or not difficulty:
            messagebox.showerror("Error", "Invalid format of recipe data.")
            return

        self.recipe.edit_recipe(name, ingredients, instructions, dish_type, difficulty)

        messagebox.showinfo("Success", "Recipe updated successfully.")
        self.destroy()

# Збереження та завантаження рецептів:
def save_recipes_to_file(recipes):
    with open("recipes.txt", "w", encoding="utf-8") as file: 
        for recipe in recipes:
            file.write(f"{recipe.name}|{','.join(recipe.ingredients)}|{recipe.instructions}|{recipe.dish_type}|{recipe.difficulty}\n")

def load_recipes_from_file():
    recipes = []
    try:
        with open("recipes.txt", "r", encoding="utf-8") as file:  
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 5:
                    name, ingredients, instructions, dish_type, difficulty = parts
                    recipes.append(Recipe(name, ingredients.split(','), instructions, dish_type, difficulty))
                else:
                    print("Invalid data format:", line)
    except FileNotFoundError:
        pass
    return recipes


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()