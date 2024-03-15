from tkinter import *
from tkinter import filedialog
import random
from PIL import ImageTk, Image
import os



class App(Frame, Canvas):

    def __init__(self, master):

        super(App, self).__init__(master)
        self.grid()

        self.gridsizes = [["615x590",20,20,100,100],["708x684",20,20,100,100],
                          ["805x798",20,20,100,100],["904x904",20,20,100,100],
                          ["990x940",15,30,101,94],["1000x990",15,20,93,90]]

        root.configure(background="#3c4043")
        root.geometry("500x300")
        self.main_menu = Frame(self, background="#3c4043")
        self.puzzle_grid = Frame(self, width = 1000, height= 1000)
        self.settings_menu = Frame(self, background="#3c4043", width = 1000, height= 1000)
        self.create_main_menu()
        self.main_menu.grid()
    

    def create_main_menu(self):


        Label(self.main_menu, text = "Puzzle Game", font = "Arial 25", bg = "#3c4043", fg = "#e8eaed").pack(padx=150, pady=10)

        self.loadButton = Button(self.main_menu, text = "Load Puzzle", width=15, bg = "#5f6368", fg = "#e8eaed", font = "Arial 15",
        command= lambda: self.load_game())
        self.loadButton.pack(side="left", padx=52,pady=100)

        self.createButton = Button(self.main_menu, text = "Create Puzzle", width=15, bg = "#5f6368", fg = "#e8eaed", font = "Arial 15",
        command = lambda: self.choose_settings())
        self.createButton.pack(side="left")

    def choose_settings(self):

        root.geometry("700x500")
        self.main_menu.grid_remove()
        self.settings_menu.grid()

        Label(self.settings_menu, text = "Choose Game Settings", font = "Arial 25", bg = "#3c4043", fg = "#e8eaed").place(x=175, y=10)
        Label(self.settings_menu, text="Enter Grid Size:", font = "Arial 15", bg = "#3c4043", fg = "#e8eaed").place(x= 10, y=150)

        grid_size = Scale(self.settings_menu, from_=5, to=10, bg = "#5f6368", fg = "#e8eaed", troughcolor= "#5f6368", borderwidth= 3, orient= HORIZONTAL, length= 200)
        grid_size.place(x=160, y=145)

        Button(self.settings_menu, text="Start Game" , width=15, bg = "#5f6368", fg = "#e8eaed", font = "Arial 15", command=lambda: self.create_game(grid_size.get())).place(x=275, y=450)
    
    def create_game(self, grid_size):

        self.grid_size = grid_size

        root.geometry(self.gridsizes[grid_size-5][0])

        self.settings_menu.grid_remove()
        self.puzzle_grid.grid()

        grid = ImageTk.PhotoImage(Image.open(f"{os.getcwd()}\grids\{grid_size}x{grid_size}.jpg"))

        img_label = Label(self.puzzle_grid, image=grid)
        img_label.image = grid
        img_label.grid()

        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=lambda: start_again())
        filemenu.add_command(label="Save as...", command=lambda: self.MyPuzzle.save_game())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)


        self.MyPuzzle = Puzzle(grid_size, int(grid_size * grid_size * 0.6), False)

    def load_game(self):

        filename = filedialog.askopenfilename(initialdir = "/saved" ,title = "Select a File", 
        filetypes = (("Text files", "*.txt*"),("all files","*.*")))

        self.main_menu.grid_remove()
        self.puzzle_grid.grid()

        self.MyPuzzle = Puzzle(0,0,filename)

        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=lambda: start_again())
        filemenu.add_command(label="Save as...", command=lambda: self.MyPuzzle.save_game())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)




class Puzzle(App):

    def __init__(self, *args):

        self.__AllowedPatterns = []
        self.__AllowedSymbols = []
        self.__Score = 0
        self.__SymbolsLeft = args[1]
        self.__GridSize = args[0]
        self.__Grid = []

        if args[2] == False:

            self.ScoreLabel = Label(puzzle.puzzle_grid, text = f"Score: {self.__Score} ", font = "Arial 15", bg = "#3c4043", fg = "#e8eaed",relief="raised")
            self.ScoreLabel.place(x=320, y=5)

            self.MovesLabel = Label(puzzle.puzzle_grid, text = f"Moves Remaining: {self.__SymbolsLeft} ", font = "Arial 15", bg = "#3c4043", fg = "#e8eaed",relief="raised")
            self.MovesLabel.place(x=100, y=5)

            # Loop for number of cells
            for Count in range(0, self.__GridSize * self.__GridSize):

                # 88% Chance of cell being unblocked
                if random.randrange(1, 101) < 90:
                    
                    C = Cell(Count)

                # 12% Chance of cell being blocked
                else:
                    C = BlockedCell(Count)

                # Add cell type to grid
                self.__Grid.append(C)   
            
            QPattern = Pattern("Q", "QQ--Q--QQ")
            self.__AllowedPatterns.append(QPattern)
            self.__AllowedSymbols.append("Q")
            XPattern = Pattern("X", "X-X-X-X-X")
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")
            TPattern = Pattern("T", "TTT--T--T")
            self.__AllowedPatterns.append(TPattern)
            self.__AllowedSymbols.append("T")
        else:

            try:
                with open(args[2]) as f:
                    NoOfSymbols = int(f.readline().rstrip())
                    for Count in range (1, NoOfSymbols + 1):
                        self.__AllowedSymbols.append(f.readline().rstrip())

                    NoOfPatterns = int(f.readline().rstrip())
                    for Count in range(1, NoOfPatterns + 1):
                        Items = f.readline().rstrip().split(",")
                        P = Pattern(Items[0], Items[1])
                        self.__AllowedPatterns.append(P)


                    self.__GridSize = int(f.readline().rstrip())
                    puzzle.grid_size = self.__GridSize
                    root.geometry(puzzle.gridsizes[self.__GridSize-4][0])

                    grid = ImageTk.PhotoImage(Image.open(f"{os.getcwd()}\grids\{self.__GridSize}x{self.__GridSize}.jpg"))

                    img_label = Label(puzzle.puzzle_grid, image=grid)
                    img_label.image = grid
                    img_label.grid()

                    for Count in range (0, self.__GridSize * self.__GridSize):
                        Items = f.readline().rstrip().split(",")
                        if Items[0] == "@":
                            C = BlockedCell(Count)
                        else:
                            C = Cell(Count)
                            if Items[0] in self.__AllowedSymbols:
                                C._Symbol.set(Items[0])

                        self.__Grid.append(C)
                    self.__Score = int(f.readline().rstrip())
                    self.__SymbolsLeft = int(f.readline().rstrip())

                    self.ScoreLabel = Label(puzzle.puzzle_grid, text = f"Score: {self.__Score} ", font = "Arial 15", bg = "#3c4043", fg = "#e8eaed",relief="raised")
                    self.ScoreLabel.place(x=320, y=5)

                    self.MovesLabel = Label(puzzle.puzzle_grid, text = f"Moves Remaining: {self.__SymbolsLeft} ", font = "Arial 15", bg = "#3c4043", fg = "#e8eaed",relief="raised")
                    self.MovesLabel.place(x=100, y=5)
                
                for index in range(0, self.__GridSize * self.__GridSize):
                    self.CheckforMatchWithPattern(index)

            except Exception as e:
                print(e)

    def AttemptPuzzle(self,index):

        CurrentCell = self.__Grid[index]

        if CurrentCell.CheckAllowed():
            CurrentCell._Symbol.set(CurrentCell.queue.get())
            if CurrentCell.HasClicked():
                self.__SymbolsLeft -= 1
            
            AddAmount = self.CheckforMatchWithPattern(index)
            self.__Score += AddAmount

            self.ScoreLabel.configure(text = f"Score: {self.__Score} ")
            self.MovesLabel.configure(text = f"Moves Remaining: {self.__SymbolsLeft} ")

            if self.__SymbolsLeft <= 0:

                for widget in puzzle.puzzle_grid.winfo_children():
                    
                    widget.config(state= "disabled")
                
                Label(puzzle.puzzle_grid, text = "Game Over", font = "Arial 25", bg = "#3c4043", fg = "#e8eaed").place(x=int(puzzle.gridsizes[self.__GridSize-4][:3]) // 3 ,y=int(puzzle.gridsizes[self.__GridSize-4][4:]) // 3)

                Button(puzzle.puzzle_grid, text= "Play Again?", font = "Arial 25", bg = "#3c4043", fg = "#e8eaed", command= lambda: start_again()
                ).place(x=int(puzzle.gridsizes[self.__GridSize-4][0][:3]) // 3 - 15 ,y=int(puzzle.gridsizes[self.__GridSize-4][4:]) // 3 + 100)


    def __GetCell(self, Row, Column):

        # Calculates Index
        # Example:
        #    1  2  3  4  5  6  7  8
        # 8  00 01 02 03 04 05 06 07
        # 7  08 09 10 11 12 13 14 15
        # 6  16 17 18 19 20 21 22 23
        # 5  24 25 26 27 28 29 30 31
        # 4  32 33 34 35 36 37 38 39
        # 3  40 41 42 43 44 45 46 47
        # 2  48 49 50 51 52 53 54 55
        # 1  56 57 58 59 60 61 62 63

        # Calculates index
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        if Index >= 0:
            return self.__Grid[Index]
        else:
            raise IndexError()

    def CheckforMatchWithPattern(self, index):

        Column = index % puzzle.grid_size+1
        Row = self.__GridSize - (index // puzzle.grid_size)

        # Checks every Cell in a 3x3 area
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    # Will check around the cell in a spiral starting in the top left
                    # →→→
                    # ↑→↓ 
                    # ←←↓

                    PatternString = ""
                    PatternString += (self.__GetCell(StartRow, StartColumn)).get()
                    PatternString += (self.__GetCell(StartRow, StartColumn + 1)).get()
                    PatternString += (self.__GetCell(StartRow, StartColumn + 2)).get()

                    PatternString += (self.__GetCell(StartRow - 1, StartColumn + 2)).get()
                    PatternString += (self.__GetCell(StartRow - 2, StartColumn + 2)).get()
                    PatternString += (self.__GetCell(StartRow - 2, StartColumn + 1)).get()

                    PatternString += (self.__GetCell(StartRow - 2, StartColumn)).get()
                    PatternString += (self.__GetCell(StartRow - 1, StartColumn)).get()
                    PatternString += (self.__GetCell(StartRow - 1, StartColumn + 1)).get()
                    for P in self.__AllowedPatterns:
                        # If matches pattern
                        if P.MatchesPattern(PatternString):
                            # Makes sure you are not allowed to change the symbol in a pattern

                            area = [(0,0), (0,1), (0,2),
                                    (1,2), (2,2), (2,1),
                                    (2,0), (1,0), (1,1)]

                            for i,j in enumerate(P.get()[2:]):
                                if j == P.get()[0]:
                                    (self.__GetCell(StartRow - area[i][0], StartColumn + area[i][1])).ChangeAllowed()

                            # Score increases by 10
                            return 10
                except Exception as e:
                    pass
        return 0
    
    def save_game(self):

        filename = filedialog.asksaveasfilename(initialdir="/saved",title= "Save file as",
        filetypes = (("Text files", "*.txt*"),("all files","*.*")))

        with open(f"{filename}.txt", "x") as f:

            f.write(f"{len(self.__AllowedSymbols)}\n")
            for Count in self.__AllowedSymbols:
                f.write(f"{Count}\n")
            
            f.write(f"{len(self.__AllowedPatterns)}\n")
            for Count in self.__AllowedPatterns:
                f.write(f"{Count.get()}\n")
            
            f.write(f"{self.__GridSize}\n")
            for Count in range(0, self.__GridSize * self.__GridSize):
                f.write(f"{(self.__Grid[Count])._Symbol.get()},\n")
            f.write(f"{self.__Score}\n")
            f.write(f"{self.__SymbolsLeft}\n")
        
        start_again()
            


class Pattern():
    def __init__(self, SymbolToUse, PatternString):
        self.__Symbol = SymbolToUse
        self.__PatternSequence = PatternString

    # Checks for matching pattern
    def MatchesPattern(self, PatternString):
        
        for i, j in zip(PatternString, self.__PatternSequence):
            if i != j and j == self.__Symbol:
                return False

        
        return True


    def GetPatternSequence(self):
      return self.__PatternSequence

    def get(self):
        return f"{self.__Symbol},{self.__PatternSequence}"
    

class Cell():
    def __init__(self,index):

        self.index = index
        self._Symbol = StringVar()
        self._Symbol.set("-")
        self.queue = circular_queue()
        self.Allowed = True
        self.Clicked = False

        

        self.button = Button(puzzle.puzzle_grid, textvariable = self._Symbol, font = "Arial 20", bg = "#3c4043", fg = "#e8eaed",
        command= lambda: puzzle.MyPuzzle.AttemptPuzzle(self.index))
        self.button.place(x=((index % puzzle.grid_size+1)*puzzle.gridsizes[puzzle.grid_size-4][3])-puzzle.gridsizes[puzzle.grid_size-4][1], y=((index // puzzle.grid_size+1)*puzzle.gridsizes[puzzle.grid_size-4][4])-puzzle.gridsizes[puzzle.grid_size-4][2])


    def CheckAllowed(self):
        if self.Allowed == True:
            return True
        else:
            return False
    
    def ChangeAllowed(self):
        self.Allowed = False
    
    def HasClicked(self):

        if self.Clicked == False:

            self.Clicked = True
            return True
        
        return False
    
    def get(self):

        if self.Allowed:
            return self._Symbol.get()
        else:
            return "-"
        
    




class BlockedCell(Cell):
    def __init__(self, index):
        self._Symbol = StringVar()
        self._Symbol.set("@")

        self.button = Label(puzzle.puzzle_grid, text="X", font = "Arial 20", bg = "#3c4043", fg = "#e8eaed"
        ).place(x=((index % puzzle.grid_size+1)*puzzle.gridsizes[puzzle.grid_size-4][3])-puzzle.gridsizes[puzzle.grid_size-4][1], y=((index // puzzle.grid_size+1)*puzzle.gridsizes[puzzle.grid_size-4][4])-puzzle.gridsizes[puzzle.grid_size-4][2])


    def get(self):

        return "-"    

class circular_queue():

    def __init__(self):

        self.queue = ["T","Q","X","-"]
        self.pointer = -1

    
    def get(self):


        if self.pointer != len(self.queue)-1:


            self.pointer += 1
            return self.queue[self.pointer]
        

        else:


            self.pointer = 0
            return self.queue[self.pointer]


def start_again():

    root.destroy()

    os.system('python SkelProg2.py')







if __name__ == "__main__":

    root = Tk()
    puzzle = App(root)

    root.mainloop()