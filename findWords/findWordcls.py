import random


class FindWords:
    def __init__(self, size,hardKind, wordKind):

        with open('txtFiles\\'+wordKind+'.txt', 'r') as file:
            self.allWords = file.read().split()

        self.sol = {}
        self.puzzle = [[' ' for _ in range(size)] for _ in range(size - 6)]
        self.n = size

        hardLevel = {'hard': 3, 'medium': 2, 'easy': 1}
        self.makePuzzle(hardLevel[hardKind])

    def makePuzzle(self, hardness):
        self.sol = {}

        nWords = random.randint(0, 10)
        words = list(zip(random.sample(range(0, self.n - 6), k=nWords),
                         random.sample(self.allWords, k=nWords)))

        for wrd in words:
            word = wrd[1]
            ir = wrd[0]
            word_len = len(word)

            ic = (random.randint(0, self.n - word_len)) % self.n

            self.sol[word] = {'from': (str(ic), str(ir)),
                              'to': (str(ic + word_len - 1), str(ir))}

            self.puzzle[ir][ic:word_len] = list(word)
            self.puzzle[ir] = self.puzzle[ir][:self.n]

        letters = [chr(ltr)
                   for ltr in range(ord('a'), ord('z') + 20 - ((hardness-1) * 10))]

        for r in range(len(self.puzzle)):
            for c in range(len(self.puzzle[r])):
                if self.puzzle[r][c] == " ":
                    self.puzzle[r][c] = random.choice(letters)

    def checkAnswer(self, pos):

        for word,wordPos in self.sol.items():
            if pos == [wordPos['from'], wordPos['to']]:
                return 1,word
        return 0,
