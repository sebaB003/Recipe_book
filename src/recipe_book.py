from tkinter import *
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import os
import tkinter.messagebox
import shutil
import re


class App:
    def __init__(self, root, version, releaseDate):
        self.version = version
        self.releaseDate = releaseDate
        self.current_recipe = None
        self.current_book = None
        self.root = root
        self.root.title("Recipe Book")
        self.root.iconbitmap("assets/icon.ico")
        self.addButtonImage = PhotoImage(file="assets/add_recipebook_button.gif")
        self.removeButtonImage = PhotoImage(file="assets/remove_recipe_button.gif")
        self.recipeBookImage = PhotoImage(file="assets/ico.gif")

        # add main menu --------------------------------------
        self.menu = Menu(self.root)
        self.root.configure(menu=self.menu)

        # Add file menu --------------------------------------
        self.fileMenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.fileMenu)

        # Add command to self.fileMenu ----------------------------
        self.fileMenu.add_command (label="Add recipe book from file", command=self.addRecipeBookFromFile)
        self.fileMenu.add_command(label="Add recipe from file", command=self.addRecipeFromFile)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Quit", command=quit)

        # Add editMenu ---------------------------------------
        self.editMenu = Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.editMenu)

        # Add command to self.editMenu ----------------------------
        self.editMenu.add_command(label="Add recipe book", command=self.newRecipeBook)
        self.editMenu.add_command(label="Add recipe", command=self.newRecipe)
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Remove recipe book", command=self.removeRecipeBook)
        self.editMenu.add_command(label="Remove recipe", command=self.removeRecipe)
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Rename recipe book", command=self.renameRecipeBookLayout)
        self.editMenu.add_command(label="Rename recipe", command=self.renameRecipeLayout)
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Edit recipe", command=self.editLayout)
        self.editMenu.add_command(label="Find by ingredients", command=self.findLayout)
        # self.editMenu.add_separator()
        # self.editMenu.add_command(label="Options")

        # Add self.helpMenu ---------------------------------------
        self.helpMenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpMenu)

        # Add command to helpMenu ----------------------------
        self.helpMenu.add_command(label="Help", command=self.helpLayout)
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label="Info", command=self.info)

        ttk.Separator(self.root, orient=HORIZONTAL).pack(fill="x")

        # Add the toolBar ------------------------------------
        self.toolBar = Frame(self.root, height="30", pady=3, padx=4)
        self.toolBar.pack(fill="x")

        # Add button to the self.toolBar ---------------------
        self.button1 = Button(self.toolBar, text="Add recipe book", bg="white", bd=1, anchor="s", relief=RIDGE, command=self.newRecipeBook)
        self.button1.config(image=self.addButtonImage, compound=LEFT, font=("Arial", "12", "bold"))
        self.button1.pack(side=LEFT)

        self.button2 = Button(self.toolBar, text="Add recipe", bg="white", bd=1, anchor="s", relief=RIDGE, command=self.newRecipe)
        self.button2.config(image=self.addButtonImage, compound=LEFT, font=("Arial", "12", "bold"))
        self.button2.pack(side=LEFT, padx=4)

        self.button3 = Button(self.toolBar, text="Remove recipe book", bg="white", bd=1, anchor="s", relief=RIDGE, command=self.removeRecipeBook)
        self.button3.config(image=self.removeButtonImage, compound=LEFT, font=("Arial", "12", "bold"))
        self.button3.pack(side=LEFT, padx=4)

        self.button4 = Button(self.toolBar, text="Remove recipe", bg="white", bd=1, anchor="s", relief=RIDGE, command=self.removeRecipe)
        self.button4.config(image=self.removeButtonImage, compound=LEFT, font=("Arial", "12", "bold"))
        self.button4.pack(side=LEFT, padx=4)

        ttk.Separator(self.root, orient=HORIZONTAL).pack(fill="x")

        # Add mainFrame --------------------------------
        self.mainFrame = Frame(self.root, bg="white")
        self.mainFrame.pack(fill="both", expand=1)
        self.spaceFrame = Frame(self.mainFrame, height="50", bg="white")
        self.spaceFrame.pack(fill="x")

        # Add recipeBooksList --------------------------
        self.recipeFrame = LabelFrame(self.mainFrame, text="Recipe books", bg="white", bd=0)
        self.recipeFrame.config(font=("Arial", "15", "bold"))
        self.recipeFrame.pack(fill="y", side="left", anchor="n")

        self.s = Frame(self.recipeFrame, bg="white", bd=0, pady=10)
        self.s.pack(fill="x")
        self.search_var = StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.update_list())
        self.srch = Label(self.s, text="Serch", bg="white", padx=10)
        self.srch.grid(sticky="w")
        self.srchEntry = Entry(self.s, textvariable=self.search_var, width=30, bg="snow")
        self.srchEntry.grid(row=0, column=1, sticky="w")

        self.scrolly1 = Scrollbar(self.recipeFrame)
        self.scrolly1.pack(side="right", fill="y")
        self.recipeBookList = Listbox(self.recipeFrame, bg="snow", width=50, bd=3, yscrollcommand=self.scrolly1.set)
        self.recipeBookList.config(font=("Arial", "12"))
        self.recipeBookList.pack(fill="y", expand=True)
        self.recipeBookList.bind("<Double-Button-1>", self.setBook)
        self.scrolly1.config(command=self.recipeBookList.yview)

        self.refresh = Button(self.recipeFrame, text="Refresh list", relief=RIDGE, bd=1, command=self.load_books)
        self.refresh.pack(side="left")
        # Add recipe frame -----------------------------
        self.spaceFrame2 = Frame(self.mainFrame, bd=0, bg="white", width="100")
        self.spaceFrame2.pack(fill="y", side="left", anchor="n")
        self.recipeFrame = LabelFrame(self.mainFrame, text="Recipes", bd=1, bg="white")
        self.recipeFrame.config(font=("Arial", "15", "bold"))
        self.recipeFrame.pack(fill="both", expand=1, side="left")

        # Add recipe list ------------------------------
        self.r = Frame(self.recipeFrame, bd=0, bg="white")
        self.r.pack(fill="y", side="left", anchor="n")
        self.scrolly2 = Scrollbar(self.r)
        self.scrolly2.pack(fill="y", side="right", anchor="n")

        self.s2 = Frame(self.r, bg="white", pady=10)
        self.s2.pack(side="top", fill="x")
        self.search_var2 = StringVar()
        self.search_var2.trace("w", lambda name, index, mode: self.update_list2())
        self.srch2 = Label(self.s2, text="Serch", bg="white")
        self.srch2.grid(sticky="w")
        self.srchEntry2 = Entry(self.s2, bg="snow", textvariable=self.search_var2, width=24)
        self.srchEntry2.grid(row=0, column=1, sticky="w")

        self.recipeList = Listbox(self.r, bd=1, bg="snow", yscrollcommand=self.scrolly2.set)
        self.recipeList.config(font=("Arial", "12"))
        self.recipeList.pack(fill="y", side="left", anchor="n")
        self.scrolly2.config(command=self.recipeList.yview)
        self.recipeList.bind("<Double-Button-1>", self.openRecipe)
        ttk.Separator(self.recipeFrame, orient=VERTICAL).pack(side="left", fill="y", padx=10)
        ttk.Separator(self.recipeFrame, orient=HORIZONTAL).pack(side="top", fill="x")

        # Add edit window ------------------------------
        self.editFrame = Frame(self.recipeFrame, bg="white", bd=1)
        self.editFrame.pack(side="left", anchor="s", fill="both", expand=1)
        self.recipeTitle = Label(self.editFrame, text=self.current_recipe, bg="white")
        self.recipeTitle.config(font=("Brush Script MT", "31", "bold"))
        self.recipeTitle.pack(side="top", anchor="center", pady=60)

        # Add ingredientsEntry -------------------------
        self.ingredientsFrame = LabelFrame(self.editFrame, text="Ingredients:", bd=0, bg="white", height="10")
        self.ingredientsFrame.config(font=("Arial", "15", "bold"))
        self.ingredientsFrame.pack(side="top", fill="x")
        self.scrolly3 = Scrollbar(self.ingredientsFrame)
        self.scrolly3.pack(side="right", fill="y")
        self.ingredientsEntry = Text(self.ingredientsFrame, bd=1, bg="snow", yscrollcommand=self.scrolly3.set, height="10")
        self.ingredientsEntry.pack(fill="x", anchor="n")
        self.scrolly3.configure(command=self.ingredientsEntry.yview())

        self.spaceFrame3 = Frame(self.editFrame, height=50, bg="white")
        self.spaceFrame3.pack(fill="x", side="top")

        # Add recipeEntry -------------------------
        self.recipeFrame = LabelFrame(self.editFrame, text="Recipe:", bd=0, bg="white")
        self.recipeFrame.config(font=("Arial", "15", "bold"))
        self.recipeFrame.pack(side="top", fill="x")
        self.scrolly4 = Scrollbar(self.recipeFrame)
        self.scrolly4.pack(side="right", fill="y")
        self.recipeEntry = Text(self.recipeFrame, bd=1, bg="snow", yscrollcommand=self.scrolly4.set)
        self.recipeEntry.pack(fill="x", expand=1, anchor="n", pady=10)
        self.scrolly4.configure(command=self.recipeEntry.yview())

        # Add status bar --------------------------
        ttk.Separator(self.root, orient=HORIZONTAL).pack(side="top", fill="x", padx=10)
        self.statusBar = Label(self.root, text="All ok!")
        self.statusBar.pack(side="left", fill="x", anchor="w", pady=1)
        self.load_books()

    def setBook(self, event):
        w = event.widget
        self.current_book = w.get(ACTIVE)
        print(self.current_book)
        self.load_recipes()

    def setRecipe(self):
        self.current_recipe = self.recipeList.get(ACTIVE)

    def load_books(self):
        self.recipeBookList.delete("0", "end")
        path = "recipe_books/"
        for book in os.listdir(path):
            self.recipeBookList.insert("end", book)

    def load_recipes(self):
        leng = 0
        self.recipeList.delete("0", "end")
        path = f"recipe_books/{self.current_book}/"
        for recipe in os.listdir(path):
            self.recipeList.insert("end", recipe)
            leng +=1
        self.set_statusBar(f"{str(self.current_book).capitalize()} contains {leng} recipes")

    def reloadRecipe(self):
        self.recipeTitle.configure(text="")
        self.ingredientsEntry.configure(state=NORMAL)
        self.recipeEntry.configure(state=NORMAL)
        self.ingredientsEntry.delete("1.0", "end")
        self.recipeEntry.delete("1.0", "end")
        self.ingredientsEntry.configure(state=DISABLED)
        self.recipeEntry.configure(state=DISABLED)

    def set_statusBar(self, text):
        self.statusBar.destroy()
        self.statusBar = Label(self.root, text=text)
        self.statusBar.pack(side="left", fill="x", anchor="w", pady=1)

    def openRecipe(self, event):
        w = event.widget
        self.current_recipe = w.get(ACTIVE)
        self.recipeTitle.configure(text=self.current_recipe)

        if self.current_book is None or self.current_recipe not in self.current_book:
            for recipebook in os.listdir("recipe_books/"):
                for recipe in os.listdir(f"recipe_books/{recipebook}"):
                    if recipe == self.current_recipe:
                        self.current_book = recipebook
                        break

        path_i = f"recipe_books/{self.current_book}/{self.current_recipe}/ingredients"
        path_r = f"recipe_books/{self.current_book}/{self.current_recipe}/recipe"

        try:
            ingredients = open(path_i, "U")
        except FileNotFoundError:
            f = open(f"recipe_books/{self.current_book}/{self.current_recipe}/ingredients", "w")
            f.write("")
            f.close()
            ingredients = open(path_i, "U")

        try:
            recipe = open(path_r, "U")
        except FileNotFoundError:
            f = open(f"recipe_books/{self.current_book}/{self.current_recipe}/recipe", "w")
            f.write("")
            f.close()
            recipe = open(path_r, "U")

        self.ingredientsEntry.configure(state=NORMAL)
        self.recipeEntry.configure(state=NORMAL)
        self.ingredientsEntry.delete('1.0', "end")
        self.recipeEntry.delete('1.0', "end")
        self.ingredientsEntry.insert("1.0", ingredients.read())
        self.recipeEntry.insert("1.0", recipe.read())
        self.ingredientsEntry.configure(state=DISABLED)
        self.recipeEntry.configure(state=DISABLED)

    def newRecipeBook(self):
        self.nr = Tk()
        self.nr.title("Add new recipe book")
        self.nr.resizable(width=False , height=False)

        self.title = Label(self.nr, text="Add new recipe book")
        self.title.grid(sticky="wn")
        ttk.Separator(self.nr, orient=HORIZONTAL).grid(columnspan=2, sticky="s")
        self.bookTitle = Label(self.nr, text="Title")
        self.bookTitle.grid(row=1, column=0, sticky="w", padx=10)
        self.textTitle = Entry (self.nr)
        self.textTitle.grid(row=1, column=1, sticky="w", padx=10)

        self.saveButton = Button(self.nr, text="Save", padx=10, relief=RIDGE, bd=1, command=self.addRecipeBook)
        self.saveButton.grid(row=2, column=0, sticky="w")
        self.cancelButton = Button(self.nr, text="Cancel", padx=10, relief=RIDGE, bd=1, command=self.nr.destroy)
        self.cancelButton.grid(row=2, column=1, sticky="e")
        self.nr.mainloop()

    def addRecipeBook(self):
        if len(self.textTitle.get()) > 0:
            if not os.path.exists(f"recipe_books/{str(self.textTitle.get()).capitalize()}"):
                os.makedirs(f"recipe_books/{str(self.textTitle.get()).capitalize()}")
                self.nr.destroy()
            else:
                result = tkinter.messagebox.askyesno("Warning",
                                                     "Another recipe book have this name, you wont overwrite? "
                                                     "If yes you'll miss all the recipe in it.")
                if result:
                    shutil.rmtree(f"recipe_books/{str(self.textTitle.get())}", True)
                    os.makedirs(f"recipe_books/{str(self.textTitle.get()).capitalize()}")
                    self.load_books()
                    self.nr.destroy()
                else:
                    pass
            self.load_books()
        else:
            tkinter.messagebox.showinfo("Info", "You can't leave empty fields")

    def removeRecipeBook(self):
        if self.current_book is not None:
            result = tkinter.messagebox.askyesno("Advertment",
                                                 f"You're sure you want to remove {self.recipeBookList.get(ACTIVE)}, "
                                                 f"you'll lost the recipe in it!")
            if result:
                shutil.rmtree(f"recipe_books/{self.recipeBookList.get(ACTIVE)}", True)
            else:
                pass
            self.load_books()
            self.load_recipes()
            self.reloadRecipe()
        else:
            tkinter.messagebox.showinfo("Info", "First you have to create or select a recipe book")

    def newRecipe(self):
        if self.current_book is not None:
            # Make new window ------------------------
            self.nr = Tk()
            self.nr.title(f"Add recipe in {self.current_book}")
            self.nr.resizable(width=False , height=False)

            # Add title ------------------------------
            self.mainTitle = Label(self.nr, text="Add recipe")
            self.mainTitle.pack(side="top", anchor="w")
            ttk.Separator(self.nr, orient=HORIZONTAL).pack(fill="x", side="top")

            # Add frame for title --------------------
            f = Frame(self.nr, bg="white")
            f.pack(fill="both", expand=1)
            self.labelTitle = Label(f, text="Title", bg="white")
            self.labelTitle.grid(sticky="w")
            self.textTitle = Entry(f, bg="snow")
            self.textTitle.grid(row=0, column=1, sticky="w")

            # add frame for ingredientsTextBox -------
            i = LabelFrame(self.nr, text="Ingredients:", bg="white", bd=0, padx=10, pady=20)
            i.pack(fill="x", expand=1)

            scrolly = Scrollbar(i)
            scrolly.pack(side="right", fill="y")
            self.ingredients = Text(i, bd=1, bg="snow", height=10, yscrollcommand=scrolly.set)
            self.ingredients.pack(fill="x", expand=1)
            scrolly.configure(command=self.ingredients.yview)

            # add frame for recipeTextBox ------------
            r = LabelFrame(self.nr, text="Recipe:", bg="white", bd=0, padx=10, pady=10)
            r.pack(fill="x", expand=1)

            scrolly2 = Scrollbar(r)
            scrolly2.pack(side="right", fill="y")
            self.recipe = Text(r, bd=1, bg="snow", height=20, yscrollcommand=scrolly2.set)
            self.recipe.pack(fill="x", expand=1)
            scrolly2.configure(command=self.recipe.yview)

            # add frame for save and cancel button ---
            b = Frame(self.nr, padx=10, pady=2, bg="white")
            b.pack(fill="x")
            self.save_button = Button(b, text="Save", relief=RIDGE, bd=1, command=self.addRecipe)
            cancel_button = Button(b, text="Cancel", relief=RIDGE, bd=1, command=self.nr.destroy)
            self.save_button.pack(side="left")
            cancel_button.pack(side="right")
        else:
            tkinter.messagebox.showinfo("Info", "First you have to create or select a recipe book")

    def addRecipe(self):
        c_b = self.current_book
        if c_b is not None:
            if len(self.textTitle.get()) == 0:
                tkinter.messagebox.showinfo("Info" , "You can't leave empty fields")
            elif len(self.ingredients.get("1.0", "end")) > 0 and len(self.recipe.get("1.0", "end")) > 0:

                if not os.path.exists(f"recipe_books/{c_b}/"
                                      f"{str(self.textTitle.get()).capitalize()}"):
                    os.makedirs(f"recipe_books/{c_b}/"
                                f"{str(self.textTitle.get()).capitalize()}")
                    ingredients = open(f"recipe_books/{c_b}/"
                                       f"{str(self.textTitle.get()).capitalize()}/ingredients", "w")
                    ingredients.write(self.ingredients.get("1.0", "end"))
                    ingredients.close()
                    recipes = open(f"recipe_books/{c_b}/"
                                   f"{str(self.textTitle.get()).capitalize()}/recipe", "w")
                    recipes.write(self.recipe.get("1.0", "end"))
                    recipes.close()
                    self.load_recipes()
                    self.nr.destroy()
                else:
                    result = tkinter.messagebox.askyesno("Warning", "Another recipe have this name, you wont overwrite?"
                                                                    "If yes you'll miss all the recipe in it.")
                    if result:
                        shutil.rmtree(f"recipe_books/{c_b}/"
                                      f"{str(self.textTitle.get()).capitalize()}", True)

                        os.mkdir(f"recipe_books/{c_b}/"
                                 f"{str(self.textTitle.get()).capitalize()}")
                        ingredients = open(f"recipe_books/{c_b}/"
                                           f"{str(self.textTitle.get()).capitalize()}/ingredients", "w")
                        ingredients.write(self.ingredients.get("1.0", "end"))
                        ingredients.close()
                        recipes = open(f"recipe_books/{c_b}/"
                                       f"{str(self.textTitle.get()).capitalize()}/recipe", "w")
                        recipes.write(self.recipe.get("1.0", "end"))
                        recipes.close()
                        self.load_recipes()
                        self.nr.destroy()
                    else:
                        pass
            else:
                tkinter.messagebox.showinfo("Info", "You can't leave empty fields")
        else:
            tkinter.messagebox.showinfo("Info", "First you have to create or select a recipe book")

    def removeRecipe(self):
        if self.current_book is not None:
            c_b = self.current_book
            result = tkinter.messagebox.askyesno("Advertment",
                                                  f"You're sure you want to remove {self.recipeList.get(ACTIVE)} "
                                                  f"from {c_b}, "
                                                  f"you'll can't recover it.")
            if result:
                shutil.rmtree(f"recipe_books/{c_b}/{self.recipeList.get(ACTIVE)}", True)
            else:
                pass
            self.load_recipes()
            self.reloadRecipe()
        else:
            tkinter.messagebox.showinfo("Info", "First you have to create or select a recipe book")

    def update_list(self):
        search_term = self.search_var.get()
        self.load_books()
        a = [x for x in self.recipeBookList.get(0, END)]

        self.recipeBookList.delete(0, END)

        for item in a:
            if search_term.lower() in item.lower():
                self.recipeBookList.insert(END, item)

    def update_list2(self):
        serch_term = self.search_var2.get()
        print(serch_term)
        self.load_recipes()
        a = [x for x in self.recipeList.get("0", "end")]

        self.recipeList.delete("0", "end")
        for item in a:
            if serch_term.lower() in item.lower():
                self.recipeList.insert("end", item)

    def renameRecipeBookLayout(self):
        c_b = self.current_book
        self.rrb = Tk()
        self.rrb.title("Rename recipe book")
        self.rrb.resizable(width=False , height=False)
        windowTitle = Label(self.rrb, text="Rename recipe book", bg="white")
        windowTitle.pack(fill="x")
        ttk.Separator(self.rrb, orient=HORIZONTAL).pack(fill="x")
        rrbf = Frame(self.rrb, bg="white", pady=10, padx=10)
        rrbf.pack(fill="both", expand=1)
        rLabel = Label(rrbf, text=f"Rename {c_b} to ", bg="white")
        rLabel.grid(row=0, column=0)
        self.renameEntry = Entry(rrbf, width=20, bg="snow")
        self.renameEntry.grid(row=0, column=1)
        renameButton = Button(rrbf, text="Rename", relief=RIDGE, bd=1, command=self.renameRecipeBook)
        renameButton.grid(row=1, column=0, padx=5, sticky="w")
        renameButton = Button(rrbf, text="Cancel", relief=RIDGE, bd=1, command=self.rrb.destroy)
        renameButton.grid(row=1, column=1, padx=5, sticky="e")

    def renameRecipeBook(self):
        c_b = self.current_book
        newName = self.renameEntry.get()
        print(os.path.exists(f"recipe_books/{newName.capitalize()}"))
        if not c_b == None:
            if not newName.capitalize() == c_b.capitalize():
                if newName is not None:
                    if not os.path.exists(f"recipe_books/{newName.capitalize()}"):
                        os.rename(f"recipe_books/{c_b}", f"recipe_books/{newName.capitalize()}")
                        self.load_books()
                        self.rrb.destroy()
                    else:
                        result = tkinter.messagebox.askyesno("Warning", "Another recipe book have this name, you wont overwrite?"
                                                                            "If yes you'll miss all the recipes in it.")
                        if result:
                            shutil.rmtree(f"recipe_books/{newName.capitalize()}", True)
                            os.rename(f"recipe_books/{c_b}", f"recipe_books/{newName.capitalize()}")
                            self.load_books()
                            self.rrb.destroy()
                        else:
                            pass
                else:
                    tkinter.messagebox.showinfo("Info", "You can't leave empty fields")
            else:
                tkinter.messagebox.showinfo("Info", "You can't rename the recipe book with the same name")
        else:
            tkinter.messagebox.showinfo("Info", "First you have to create or select a recipe book")

    def renameRecipeLayout(self):
        c_r = self.recipeList.get(ACTIVE)
        self.rrb = Tk()
        self.rrb.title("Rename recipe")
        self.rrb.resizable(width=False , height=False)
        windowTitle = Label(self.rrb, text="Rename recipe", bg="white")
        windowTitle.pack(fill="x")
        ttk.Separator(self.rrb, orient=HORIZONTAL).pack(fill="x")
        rrbf = Frame(self.rrb, bg="white", pady=10, padx=10)
        rrbf.pack(fill="both", expand=1)
        rLabel = Label(rrbf, text=f"Rename {c_r} to ", bg="white")
        rLabel.grid(row=0, column=0)
        self.renameEntry = Entry(rrbf, width=20, bg="snow")
        self.renameEntry.grid(row=0, column=1)
        renameButton = Button(rrbf, text="Rename", relief=RIDGE, bd=1, command=self.renameRecipe)
        renameButton.grid(row=1, column=0, padx=5, sticky="w")
        renameButton = Button(rrbf, text="Cancel", relief=RIDGE, bd=1, command=self.rrb.destroy)
        renameButton.grid(row=1, column=1, padx=5, sticky="e")

    def renameRecipe(self):
        c_b = self.current_book
        c_r = self.recipeList.get(ACTIVE)
        newName = self.renameEntry.get()
        if not c_b == None:
            if not c_r == None:
                if not newName.capitalize() == c_r.capitalize():
                    if newName is not None:
                        if not os.path.exists(f"recipe_books/{c_b.capitalize()}/{newName.capitalize()}"):
                            os.rename(f"recipe_books/{c_b.capitalize()}/{c_r.capitalize()}",
                                      f"recipe_books/{c_b.capitalize()}/{newName.capitalize()}")
                            self.load_recipes()
                            self.rrb.destroy()
                        else:
                            result = tkinter.messagebox.askyesno("Warning", "Another recipe have this name, you wont overwrite?"
                                                                                "If yes you'll miss the recipe.")
                            if result:
                                shutil.rmtree(f"recipe_books/{c_b.capitalize()}/{newName.capitalize()}", True)
                                os.rename(f"recipe_books/{c_b.capitalize()}/{c_r.capitalize()}",
                                          f"recipe_books/{c_b.capitalize()}/{newName.capitalize()}")
                                self.load_recipes()
                                self.rrb.destroy()
                            else:
                                pass
                    else:
                        tkinter.messagebox.showinfo("Info", "You can't leave empty fields")
                else:
                    tkinter.messagebox.showinfo("Info", "You can't rename the recipe book with the same name")
            else:
                tkinter.messagebox.showinfo("Info", "First you have to create or select a recipe")
        else:
            tkinter.messagebox.showinfo("Info", "First you have to create or select a recipe book")

    def editLayout(self):
        c_r = self.recipeList.get(ACTIVE)
        c_b = self.current_book
        print(c_r)
        if c_r is not "":
            self.edit = Tk()
            self.edit.title("Edit recipe")
            self.edit.resizable(width=False , height=False)
            mf = Frame(self.edit, bg="white", bd=0, padx=20)
            mf.pack(fill="both", expand=1)

            menu = Menu(self.edit)
            self.edit.configure(menu=menu)

            fMenu = Menu(menu)
            menu.add_cascade(label="File", menu=fMenu)
            fMenu.add_command(label="Import ingredients", command=self.importIngredients)
            fMenu.add_command(label="Import recipe", command=self.importRecipe)
            fMenu.add_separator()
            fMenu.add_command(label="Export ingredients", command=self.exportIngredients)
            fMenu.add_command(label="Export recipe", command=self.exportRecipe)

            eMenu = Menu(menu)
            menu.add_cascade(label="Edit", menu=eMenu)
            eMenu.add_command(label="Delete all", command=self.delAll)

            ttk.Separator(mf, orient=HORIZONTAL).pack(fill="x")
            i = LabelFrame(mf, text="Ingredients:", bg="white", bd=0, pady=30, padx=10)
            i.pack(fill="x", expand=1)
            scrolly = Scrollbar(i)
            scrolly.pack(side="right", fill="y")
            self.it = Text(i, bg="snow", height=10, yscrollcommand=scrolly.set)
            file = open(f"recipe_books/{c_b}/{c_r}/Ingredients", "r")
            self.it.insert("1.0", file.read())
            self.it.pack(fill="x", expand=1)
            scrolly.configure(command=self.it.yview)
            r = LabelFrame(mf, text="Recipe:", bg="white", bd=0, pady=30, padx=10)
            r.pack(fill="x", expand=1)
            file = open(f"recipe_books/{c_b}/{c_r}/Recipe", "r")
            scrolly2 = Scrollbar(r)
            scrolly2.pack(side="right", fill="y")
            self.rt = Text(r, bg="snow", height=20, yscrollcommand=scrolly2.set)
            self.rt.insert("1.0", file.read())
            self.rt.pack(fill="x", expand=1)
            scrolly2.configure(command=self.rt.yview)

            b = Frame(self.edit, padx=10, bg="white")
            b.pack(fill="x")

            saveButton = Button(b, text="Save", relief=RIDGE, bd=1, padx=10, command=self.save)
            saveButton.grid(sticky="w")
            cancelButton = Button(b, text="Cancel", relief=RIDGE, bd=1, padx=10, command=self.edit.destroy)
            cancelButton.grid(row=0, column=1, sticky="e")
        else:
            tkinter.messagebox.showinfo("Info", "First you have to create or select a recipe")

    def save(self):
        c_r = self.recipeList.get(ACTIVE)
        c_b = self.current_book

        file = open(f"recipe_books/{c_b}/{c_r}/Ingredients", "w")
        file.write(self.it.get("1.0", "end"))
        file.close()

        file = open(f"recipe_books/{c_b}/{c_r}/Recipe", "w")
        file.write(self.rt.get("1.0", "end"))
        file.close()
        self.reloadRecipe()

    def delAll(self):
        self.it.delete("1.0", "end")
        self.rt.delete("1.0", "end")

    def importIngredients(self):
        filetype = [("Text file", "*.txt")]
        path = fd.askopenfilename(title="Chose the file of the ingredients", filetypes=filetype)

        file = open(path, "r")
        self.it.delete("1.0", "end")
        self.it.insert("1.0", file.read())
        file.close()

    def importRecipe(self):
        filetype = [("Text file", "*.txt")]
        path = fd.askopenfilename(title="Chose the file of the recipe", filetypes=filetype)

        file = open(path, "r")
        self.rt.delete("1.0", "end")
        self.rt.insert("1.0", file.read())
        file.close()

    def exportIngredients(self):
        filetype = [("Text file", "*.txt")]
        path = fd.asksaveasfilename(title="Chose where you wont to save the file", filetypes=filetype)
        f = open(path, "w")
        f.write(self.it.get("1.0", "end"))
        f.close()

    def exportRecipe(self):
        filetype = [("Text file", "*.txt")]
        path = fd.asksaveasfilename(title="Chose where you wont to save the file", filetypes=filetype)
        f = open(path, "w")
        f.write(self.rt.get("1.0", "end"))
        f.close()

    def addRecipeBookFromFile(self):
        path = fd.askdirectory(title="recipe")
        a = path.split("/")
        b = [x for x in self.recipeBookList.get("0", "end")]
        if not a[len(a)-1] in b:
            shutil.move(path, "recipe_books/")
        else:
            result = tkinter.messagebox.askyesno("Warning", "Another recipe book have this name, you wont overwrite?"
                                                            "If yes you'll miss all the recipe in it.")
            if result:
                shutil.rmtree(f"recipe_books/{a[len(a) - 1]}")
                shutil.move(path, "recipe_books/")
            else:
                pass

    def addRecipeFromFile(self):
        c_b = self.current_book
        path = fd.askdirectory(title="recipe")
        a = path.split("/")
        b = [x for x in self.recipeList.get("0", "end")]
        if not c_b is None:
            if not a[len(a) - 1] in b:
                shutil.move(path, f"recipe_books/{c_b}/")

            else:
                result = tkinter.messagebox.askyesno("Warning", "Another recipe have this name, you wont overwrite?"
                                                                "If yes you'll miss the recipe.")
                if result:
                    shutil.rmtree(f"recipe_books/{c_b}/{a[len(a) - 1]}")
                    shutil.move(path, f"recipe_books/{c_b}/")
                else:
                    pass
        else:
            tkinter.messagebox.showinfo("Info", "First you have to create or select a recipe book")

    def findLayout(self):
        self.fl = Tk()
        self.fl.title("Find by ingredients")
        self.fl.resizable(width=False , height=False)
        title = Label(self.fl, text="Find by ingredient")
        title.pack(side="top", anchor="w")
        ttk.Separator(self.fl, orient=HORIZONTAL).pack(fill="x")
        sF = Frame(self.fl, bg="white", bd=0, pady=10, padx=5)

        sF.pack(fill="both", expand=1, side="left")
        srch = Label(sF, text="Find: ", bg="white")
        srch.grid(row=0, column=0, sticky="w")
        self.findEntry = Entry(sF, bg="snow")
        self.findEntry.grid(row=0, column=1, sticky="w")
        b = Button(sF, text="Find", bg="white", bd=1, relief=RIDGE, command=self.find)
        b.grid(row=1)
        sfT = LabelFrame(self.fl, text="Search terms", bg="white")
        sfT.pack(fill="both", expand=1, side="right")

        rF = Frame(sF, bg="white")
        rF.grid(row=2, columnspan=2)
        title2 = Label(rF, text="Search results", bg="white")
        title2.pack(side="top", anchor="w")
        ttk.Separator(rF, orient=HORIZONTAL).pack(fill="x")
        scrolly = Scrollbar(rF)
        scrolly.pack(side="right", fill="y")
        self.srchResults = Listbox(rF, bg="snow", yscrollcommand=scrolly.set)
        self.srchResults.pack(side="bottom", fill="x", expand=1)
        self.srchResults.bind("<Double-Button-1>", self.openRecipe)
        scrolly.configure(command=self.srchResults.yview)
        self.fl.mainloop()

    def find(self):
        srchterms = self.findEntry.get()
        srchterms = srchterms.replace(" ", "")
        srchterms = srchterms.split(",")

        print(srchterms)
        r = [x for j in os.listdir("recipe_books/") for x in os.listdir(f"recipe_books/{j}")]
        for x in r:
            self.srchResults.insert("end", x)

        self.srchResults.delete("0", "end")
        for srchterm in srchterms:
            for recipebook in os.listdir("recipe_books/"):
                for recipe in os.listdir(f"recipe_books/{recipebook}"):
                    file = open(f"recipe_books/{recipebook}/{recipe}/ingredients")
                    file = file.read()
                    if srchterm.lower() in file.lower():
                        if recipe not in self.srchResults.get("0", "end"):
                            self.srchResults.insert("end", recipe)

    def helpLayout(self):
        self.hl = Tk()
        self.hl.title("Help")
        fhb = Frame(self.hl, bg="white", bd=0, width=50, pady=10)
        fhb.pack(fill="y", side="left")
        b1 = Button(fhb, text="Main window")
        b1.pack()
        b2 = Button(fhb, text="Add recipe")
        b2.pack()
        b3 = Button(fhb, text="Search window")
        b3.pack()
        b4 = Button(fhb, text="Edit window")
        b4.pack()
        fh = Frame(self.hl, bg="white", bd=0, pady=10)
        fh.pack(fill="both", expand=1, side="right")
        a = Text(fh, bg="snow", state=DISABLED)
        a.pack(fill="both", expand=1)

    def info(self):
        self.inf = Tk()
        self.inf.title("Info")
        self.inf.resizable(width=False , height=False)

        title = Label(self.inf, text="Info")
        title.pack(fill="x")
        ttk.Separator(self.inf, orient=HORIZONTAL).pack(fill="x")
        version = Label(self.inf, text=f"Version: {self.version}")
        relaseDate = Label(self.inf, text=f"Release date: {self.releaseDate}")
        developer = Label(self.inf, text="Developer: Sebastiano Bisacchi")
        rBug = Label(self.inf, text="Report bug: sebastianobisacchi@outlook.com")
        version.pack()
        relaseDate.pack()
        developer.pack()
        rBug.pack()
        ttk.Separator(self.inf, orient=HORIZONTAL).pack(fill="x")
        exit = Button(self.inf, text="Exit", relief=RIDGE, bd=1, command=self.inf.destroy)
        exit.pack(side="top")
        self.inf.mainloop()

if __name__ == '__main__':
    root = Tk()
    main = App(root, "1.0", None)
    root.mainloop()
