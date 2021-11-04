import numpy as np
import random
from PIL import Image, ImageColor

'''
A class to represent an elementary cellular automaton

Attributes
----------
rule : numpy array
    the rule that defines the automaton in binary

width : int
    the number of cells in a row

height : int
    the number of generations

history : numpy array
    an array of the generations of the automaton
'''
class ElemCA:
    def __init__(self, rule, width, height, random_state):
        '''
        Initialises the elementary cellular automaton object

        Parameters
        ----------
        rule : int
            the rule that defines the cellular automaton
        
        width : int
            the number of cells in a row

        height : int
            the number of generations to compute

        random_state : boolean
            whether the cellular automaton has a random initial state
        '''
        self.width = width
        self.height = height
        self.rule = self.binary_rule(rule)

        self.current_state = np.zeros((width))
        
        if (random_state):
            for i in range(width):
                self.current_state[i] = random.randint(0,1)
        else:
            self.current_state[(width + 1) // 2] = 1.0

        self.history = self.generate()

    def apply_rule(self, parents):
        '''
        Applies the rule to a cell given the set of parent cells

        Parameters
        ----------
        parents : list
            the parents of the cell of focus

        Returns
        -------
        int
            the value of the cell
        '''
        if (parents[0] == 1 and parents[1] == 1 and parents[2] == 1):
            return self.rule[0]
        elif (parents[0] == 1 and parents[1] == 1 and parents[2] == 0):
            return self.rule[1]
        elif (parents[0] == 1 and parents[1] == 0 and parents[2] == 1):
            return self.rule[2]
        elif (parents[0] == 1 and parents[1] == 0 and parents[2] == 0):
            return self.rule[3]
        elif (parents[0] == 0 and parents[1] == 1 and parents[2] == 1):
            return self.rule[4]
        elif (parents[0] == 0 and parents[1] == 1 and parents[2] == 0):
            return self.rule[5]
        elif (parents[0] == 0 and parents[1] == 0 and parents[2] == 1):
            return self.rule[6]
        else:
            return self.rule[7]
    
    def binary_rule(self, rule):
        '''
        Returns an array with the binary representation of the rule

        Parameters
        ----------
        rule : int
            The integer value of the rule

        Returns
        -------
        numpy array
            an array containing the binary representation of the rule
        '''
        rule_bin = np.zeros((8))

        quotient = rule
        i = 7

        while (quotient > 0):
            remainder = quotient % 2
            rule_bin[i] = remainder
            quotient = quotient // 2
            i = i - 1
        
        return rule_bin
    
    def create_image(self, scale):
        '''
        
        '''
        img = Image.new('L', (self.width * scale, self.height * scale), 'white')
        pixels = img.load()

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                if self.history[j // scale, i // scale] == 1:
                    img.putpixel((i,j), 0)

        return img
    
    def generate(self):
        '''
        Generates the complete history of the cellular automata

        Returns
        -------
        numpy array
            an array where each row represents a generation of the automata
        '''
        history = self.current_state

        for i in range(self.height - 1):
            next = self.next_generation()
            history = np.append(history, next)

        history = history.reshape((self.height, self.width))

        return history
    
    def next_generation(self):
        '''
        Calculate the next generation of the cellular automata and update
        current state

        Returns
        -------
        numpy array
            the next state of the cellular automata
        '''
        next_state = np.zeros((self.width))

        for i in range(self.width):
            next_state[i] = self.apply_rule(self.parents(i))

        self.current_state = next_state

        return next_state

    def parents(self, i):
        '''
        Returns the parents of a cell number in the previous generation

        Parameters
        ----------
        i : int
            the cell index

        Returns
        -------
        numpy array
            the parents of the given cell
        '''
        parents = np.zeros((3))

        if (i == 0):
            parents[0] = self.current_state[self.width - 1]
            parents[1] = self.current_state[0]
            parents[2] = self.current_state[1]
        elif (i == self.width - 1):
            parents[0] = self.current_state[self.width - 2]
            parents[1] = self.current_state[self.width - 1]
            parents[2] = self.current_state[0]
        else:
            parents[0] = self.current_state[i - 1]
            parents[1] = self.current_state[i]
            parents[2] = self.current_state[i + 1]

        return parents

if __name__ == "__main__":
    elemCA = ElemCA(90, 400, 200, False)
    print(elemCA.history)
    img = elemCA.create_image(2)
    img.show()