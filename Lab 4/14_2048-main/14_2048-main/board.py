import random

SIZE = 4


class Board:
    def __init__(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()

        self.last_merges = []

    def add_random_tile(self):
        empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    
    @staticmethod
    
    @staticmethod
    def slide_line_with_merges(line):
        values = [x for x in line if x]
        result = []
        merges = []
        i = 0

        while i < len(values):
            if i + 1 < len(values) and values[i] == values[i + 1]:
                merged_value = values[i] * 2
                result.append(merged_value)
                merges.append(merged_value)
                i += 2
            else:
                result.append(values[i])
                i += 1

        result += [0] * (SIZE - len(result))
        return result, merges

    @staticmethod
    def slide_line(line):
        result, _ = Board.slide_line_with_merges(line)
        return result



    
    def move_left(self):
        changed = False
        self.last_merges = []

        for r in range(SIZE):
            old = self.grid[r][:]
            new, merges = self.slide_line_with_merges(old)
            self.grid[r] = new
            self.last_merges.extend(merges)
            changed |= old != new

        return changed

    def move_right(self):
        changed = False
        self.last_merges = []

        for r in range(SIZE):
            old = self.grid[r][:]
            new, merges = self.slide_line_with_merges(list(reversed(old)))
            new = list(reversed(new))
            self.grid[r] = new
            self.last_merges.extend(merges)
            changed |= old != new

        return changed

    def move_up(self):
        changed = False
        self.last_merges = []

        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            new, merges = self.slide_line_with_merges(old)

            for r in range(SIZE):
                self.grid[r][c] = new[r]

            self.last_merges.extend(merges)
            changed |= old != new

        return changed

    def move_down(self):
        changed = False
        self.last_merges = []

        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            new, merges = self.slide_line_with_merges(list(reversed(old)))
            new = list(reversed(new))

            for r in range(SIZE):
                self.grid[r][c] = new[r]

            self.last_merges.extend(merges)
            changed |= old != new

        return changed


    def can_move(self):
        if any(0 in row for row in self.grid):
            return True
        for r in range(SIZE):
            for c in range(SIZE):
                if c + 1 < SIZE and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r + 1 < SIZE and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False
