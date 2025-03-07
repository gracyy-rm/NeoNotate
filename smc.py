import json

class NoteManager:
    def __init__(self, data_file):
        """
        Initialize NoteManager with a data file path.
        """
        self.data_file = data_file
        self.notes = []
        self.categories = {}
        self.keyword_weights = {}

    def load_data(self):
        """
        Load notes, categories, and keyword weights from the data file.
        """
        print(f"Loading data from: {self.data_file}")
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                self.notes = data.get('notes', [])
                self.categories = data.get('categories', {})
                self.keyword_weights = data.get('keyword_weights', {})
                print("Data loaded successfully!")
        except FileNotFoundError:
            print(f"File '{self.data_file}' not found. A new file will be created upon saving.")
        except json.JSONDecodeError:
            print("Error: Invalid file format. Could not load data.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def save_data(self):
        """
        Save notes, categories, and keyword weights to the data file.
        """
        data = {
            'notes': self.notes,
            'categories': self.categories,
            'keyword_weights': self.keyword_weights,
        }
        try:
            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=4)
            print("Data saved successfully!")
        except IOError as e:
            print(f"Error saving data: {e}")
        except Exception as e:
            print(f"Unexpected error while saving data: {e}")

    def add_category(self, category, keywords):
        """
        Add a new category with associated keywords.
        """
        category = category.strip()
        keywords_list = [kw.strip() for kw in keywords if kw.strip()]
        
        if not category:
            print("Error: Category name cannot be empty.")
            return
        if not keywords_list:
            print("Error: Keywords cannot be empty.")
            return
        if category in self.categories:
            print(f"Error: Category '{category}' already exists.")
            return
        
        self.categories[category] = keywords_list
        self.save_data()
        print(f"Category '{category}' added successfully with keywords: {', '.join(keywords_list)}")

    def add_note(self, note_content):
        """
        Add a new note and categorize it automatically.
        """
        note_content = note_content.strip()
        if not note_content:
            print("Error: Note content cannot be empty.")
            return
        category = self.categorize_notes(note_content)
        self.notes.append({'content': note_content, 'category': category})
        self.update_keyword_weights(note_content.split(), category)
        self.save_data()
        print(f"Note added successfully under category '{category}'.")

    def categorize_notes(self, note_content):
        """
        Categorize a note based on its content using keywords.
        """
        words = [word.lower() for word in note_content.split()]
        scores = {category: 0 for category in self.categories}
        
        for word in words:
            for category, keywords in self.categories.items():
                if word in [kw.lower() for kw in keywords]:
                    scores[category] += self.keyword_weights.get(word, 1)
        
        suitable_category = max(scores, key=scores.get)
        if scores[suitable_category] == 0:
            return "Others"
        return suitable_category

    def update_keyword_weights(self, words, category):
        """
        Update keyword weights for the given category based on note content.
        """
        if category not in self.categories:
            print(f"Error: Category '{category}' does not exist.")
            return
        for word in words:
            if word in self.categories.get(category, []):
                self.keyword_weights[word] = self.keyword_weights.get(word, 0) + 1
        self.save_data()

    def view_notes(self):
        """
        Display all notes along with their categories.
        """
        if not self.notes:
            print("No notes available to view.")
        else:
            print("\n--- Viewing All Notes ---")
            for note in self.notes:
                print(f"Category: {note['category']} | Note: {note['content']}")

    def search_notes(self, keyword):
        """
        Search notes containing the given keyword.
        """
        keyword = keyword.strip()
        if not keyword:
            print("Error: Keyword cannot be empty.")
            return []
        results = [note for note in self.notes if keyword.lower() in note['content'].lower()]
        if not results:
            print(f"No notes found containing the keyword '{keyword}'.")
        return results

    def export_notes(self, filename):
        filename = filename.strip()
        if not filename:
            print("Error: Filename cannot be empty.")
            return
        try:
            with open(filename, 'w') as file:
                json.dump(self.notes, file, indent=4)
            print(f"Notes exported successfully to '{filename}'.")
        except IOError as e:
            print(f"Error exporting notes: {e}")
        except Exception as e:
            print(f"Unexpected error while exporting notes: {e}")

            
def menu():
    """
    Display the main menu and handle user inputs for various operations.
    """
    note_manager = NoteManager("0-Smart_Notes_Categorizer/notes.json")
    note_manager.load_data()
    

    while True:
        print("\n--- NEONOTATE ---")
        print("1. Add Category")
        print("2. Add Note")
        print("3. View Notes")
        print("4. Search Notes")
        print("5. Export Notes")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            category = input("Enter Category Name: ")
            keywords = input("Enter keywords (separated by commas): ").split(',')
            note_manager.add_category(category, keywords)

        elif choice == '2':
            note_content = input("Enter note content: ")
            note_manager.add_note(note_content)

        elif choice == '3':
            note_manager.view_notes()

        elif choice == '4':
            keyword = input("Enter keyword to search: ")
            results = note_manager.search_notes(keyword)
            if results:
                for note in results:
                    print(f"Category: {note['category']} | Note: {note['content']}")

        elif choice == '5':
            filename = input("Enter filename to export notes: ")
            note_manager.export_notes(filename)

        elif choice == '6':
            print("Thank you for using NEONOTATE! Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

menu()
