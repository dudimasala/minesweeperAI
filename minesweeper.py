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
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if(len(self.cells) == self.count):
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if(self.count == 0):
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if(cell in self.cells):
            self.count -= 1
            self.cells.remove(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if(cell in self.cells):
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
        self.allCells = set()
        for i in range(0, self.height):
            for j in range(0, self.width):
                self.allCells.add((i, j))
        
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
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
               
        1.
        """
        self.moves_made.add(cell)
        
        #2
        
        self.mark_safe(cell)
        
        #3
        yind, xind = cell
        unknownNeighbours = set()
        
        for i in range(max(0, yind-1), min(yind+2, self.height)):
            for j in range(max(0, xind-1), min(xind+2, self.width)):
                if (yind, xind) != (i, j):
                    if (i, j) in self.mines:
                        count -= 1
                    elif (i, j) not in self.safes:
                        unknownNeighbours.add((i, j))
       
        nSent = Sentence(unknownNeighbours, count)
        if(nSent not in self.knowledge):
            self.knowledge.append(nSent)
        
        #4
        for sentence in self.knowledge:
            for safeExpl in sentence.known_safes():
                if(safeExpl not in self.safes):
                    self.safes.add(safeExpl)
            for mineExpl in sentence.known_mines():
                if(mineExpl not in self.mines):
                    self.mines.add(mineExpl)
                    
        #5
        """
        not working, I think because of the for loops, change this...
        
        inferences = []
        for ind1 in range(len(self.knowledge)-1):
            for ind2 in range(ind1+1, len(self.knowledge)):
                if(len(self.knowledge[ind1].cells)  > 1 and len(self.knowledge[ind2].cells) > 1):
                    if(len(self.knowledge[ind1].cells)  > len(self.knowledge[ind2].cells) and self.knowledge[ind2].cells.issubset(self.knowledge[ind1].cells)):
                        tempCells = self.knowledge[ind1].cells - self.knowledge[ind2].cells
                        tempCount = self.knowledge[ind1].count - self.knowledge[ind1].count
                        inferences.append(Sentence(tempCells, tempCount))
                    
                    elif(len(self.knowledge[ind2].cells) > len(self.knowledge[ind1].cells) and self.knowledge[ind1].cells.issubset(self.knowledge[ind2].cells)):
                        tempCells = self.knowledge[ind2].cells - self.knowledge[ind1].cells
                        tempCount = self.knowledge[ind2].count - self.knowledge[ind1].count
                        if(tempCount > -1):
                            inferences.append(Sentence(tempCells, tempCount))
                        
        for inference in inferences:
            if(inference not in self.knowledge):
                self.knowledge.append(inference)
                       
        """
        """
        this works
        """ 
        
        inferences = []
        for s1 in self.knowledge:
            for s2 in self.knowledge:
                if len(s1.cells) > 0 and len(s2.cells) > 0 and s1 != s2:
                    if s1.cells.issubset(s2.cells):
                        tempCells = s2.cells - s1.cells
                        tempCount = s2.count - s1.count
                        if(tempCount > -1):
                            inferences.append(Sentence(tempCells, tempCount))
        
        for inference in inferences:
            if(inference not in self.knowledge):
                self.knowledge.append(inference)
           

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for sCell in self.safes:
            if(sCell not in self.moves_made and sCell not in self.mines):
                print(sCell)
                print(self.mines)
                print(self.safes)
                return sCell
        print(self.mines)
        print(self.safes)
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        choicesSet = self.allCells - self.moves_made - self.mines
        choicesSet = list(choicesSet)
        return random.choice(choicesSet)
    
