import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main3 import Recipe, MainWindow, AddRecipeWindow, SearchRecipesWindow

class TestRecipe(unittest.TestCase):
    def test_recipe_init(self):
        recipe = Recipe("Spaghetti", ["pasta", "tomato sauce"], "Cook pasta, add tomato sauce", "Main Course", "Easy")
        self.assertEqual(recipe.name, "Spaghetti")
        self.assertEqual(recipe.ingredients, ["pasta", "tomato sauce"])
        self.assertEqual(recipe.instructions, "Cook pasta, add tomato sauce")
        self.assertEqual(recipe.dish_type, "Main Course")
        self.assertEqual(recipe.difficulty, "Easy")

if __name__ == '__main__':
    unittest.main()