import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        if len(self.cells) == self.count:
            if len(self.cells) != 0:
                return self.cells
        
        return None        

    def known_safes(self):
         if self.count == 0:
            if len(self.cells) != 0:
                return self.cells
        
         return None


    def mark_mine(self, cell):
       
        
        if cell in self.cells:
            self.count = self.count - 1
            self.cells.remove(cell)
                
    def mark_safe(self, cell):
                
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
    def add_knowledge(self, cell, count):
        
        self.moves_made.add(cell)
        
        self.mark_safe(cell)
        
        cells = []
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                
                if (i, j) == cell:
                    continue

                
                if 0 <= i < self.height and 0 <= j < self.width:
                   
                    if (i, j) in self.mines:
                        count = count - 1
                    elif (i, j) not in self.safes:
                        cells.append((i, j))
        self.knowledge.append(Sentence(cells, count))
        
        for sentence in self.knowledge:
            safe = sentence.known_safes()
            mine = sentence.known_mines()
            if safe != None:
                self.safes = self.safes.union(safe)
            if mine != None:
                self.mines = self.mines.union(mine)
        
        knowledgelength = len(self.knowledge)
        for i in range(knowledgelength):
            for j in range(i + 1, knowledgelength):
                sent1 = self.knowledge[i]
                sent2 = self.knowledge[j]
                if sent1.cells.issubset(sent2.cells):
                    cells = sent2.cells - sent1.cells
                    sent = Sentence(sent2.cells - sent1.cells, sent2.count - sent1.count)
                   
                    if sent not in self.knowledge:
                        self.knowledge.append(sent)
                elif sent2.cells.issubset(sent1.cells):
                    cells = sent1.cells - sent2.cells
                    sent = Sentence(sent1.cells - sent2.cells, sent1.count - sent2.count)
                 
                    if sent not in self.knowledge:
                        self.knowledge.append(sent)
        
                        
                
    def make_safe_move(self):
        for i in self.safes:
            if i not in self.moves_made:
                return i
        return None



    def make_random_move(self):
        
        for i in range(0,self.height):
            for j in range(0,self.width):
                newcell = (i,j)
                if newcell not in self.moves_made:
                    if newcell not in self.mines:
                        return newcell
        return None
