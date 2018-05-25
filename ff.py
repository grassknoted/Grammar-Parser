import sys
from collections import defaultdict

# Grammar Class
class GrammarParser:
    epsilon = 'EPSILON'

    def __init__(self, grammar):

        # Set for all non-terminals
        self.nt = set()

        # Set for all productions
        self.productions = defaultdict(list)

        # Set for non-terminals that are never executed
        self.non_entry_nt = set()

        # Set for first computation
        self.first = defaultdict(set)

        # Set for follow computation
        self.follow = defaultdict(set)
        
        #self.predict = defaultdict(set)

        # Set for all symbols
        self.symbols = set()

        # Set for epsilon predictions
        self.eps = defaultdict(lambda: False)

        # Set to maintain the order of non-terminals
        self.nt_order = []

        # Replace 'e', 'ε' or 'epsilon' in grammar
        grammar = grammar.replace("e", self.epsilon)
        grammar = grammar.replace("ε", self.epsilon)
        grammar = grammar.replace("epsilon", self.epsilon)

        # Work on the grammar production by production
        for production in filter(lambda x: "->" in x, grammar.split("\n")):

            # Split into non-terminal and RHS
            nt, rhs = production.split("->")

            # Remove unnecessay spaces
            nt = nt.strip()

            # Maintain order in which the non-terminals are encountered
            if nt not in self.nt_order:
                self.nt_order.append(nt)

            # Add the non-terminal symbol to sets: nt and symbols
            self.nt.add(nt)
            self.symbols.add(nt)

            # Spaces between symbols on RHS to make it readable
            rhs = ' '.join(rhs[i:i+1] for i in range(0, len(rhs), 1))

            # Consider individual symbols in the RHS
            for s_prod in rhs.split("|"):
                cur_prod = []

                # Consider individual symbols in RHS
                for symbol in s_prod.split():

                    # Remove unnecessay spaces
                    symbol = symbol.strip()

                    # Add symbol to set of non-entering non-terminal
                    self.non_entry_nt.add(symbol)
                    # Add to list of symbols in the current production
                    cur_prod.append(symbol)

                    # Check if the symbol is epsilon
                    if symbol == self.epsilon:
                        self.eps[nt] = True
                        # Add to the first of the current (LHS) non-terminal
                        self.first[nt].add(self.epsilon)
                    else:
                        # If not epsilon, add to current symbols
                        self.symbols.add(symbol)

                # Add current production to list of all productions
                self.productions[nt].append(cur_prod)

        # Get list of all terminals
        self.terminals = self.symbols - self.nt

        # Get list of all start symbols
        self.start_symbols = self.nt - self.non_entry_nt

        # Add terminal to it's own First
        for terminal in self.terminals:
            self.first[terminal].add(terminal)

        # Calculate the First set
        changed = True

        while changed:
            changed = False

            # For each non-terminal
            for nt in self.nt:

                # Traverse all productions of the non-terminal
                for prod in self.productions[nt]:
                    found = False

                    # For individual symbols in the production
                    for symbol in prod:

                        # If length of [First(symbol)-First(Non-terminal)] > 0
                        if len(self.first[symbol] - self.first[nt]) > 0:
                            changed = True
                            # Add First(symbol) to First(Non-terminal)
                            self.first[nt] |= (self.first[symbol] - set(self.epsilon))

                        # Check for epsilon
                        if self.epsilon not in self.first[symbol]:
                            break

                    else:
                        # If epsilon is not present, and no other symbols, add epsilon
                        if self.epsilon not in self.first[nt]:
                            self.first[nt].add(self.epsilon)
                            changed = True

        # Calculate the follow set
        # start_symbols = non terminals that don't appear in RHS
        if not self.start_symbols:
            # Add the first non-terminal of the grammar (start symbol)
            self.start_symbols.add(self.nt_order[0])

        print("Start Symbols: ", self.start_symbols)
        # For non-terminals in set of start symbols
        for nt in self.start_symbols:
            # Add '$', as it is possible that nothing could follow those symbols
            self.follow[nt].add("$")
            print("First-Follow: ", self.follow[nt])

        changed = True
        while changed:
            changed = False

            # Consider non-terminals one at a time
            for nt in self.nt:
                # Consider all productions of the current non-terminal
                for prod in self.productions[nt]:
                    # BUGGY
                    # Consider union of current production and future productions
                    print("Prod1: ", prod, "Prod2: ", prod[1:])
                    for symbol1, symbol2 in zip(prod, prod[1:]):
                        print("Symbol1: ", symbol1, "Symbol2: ", symbol2)
                       
                        # The first symbol must be a non-terminal
                        if symbol1 in self.nt:
                            # first_sym2 = First(symbol2) without epsilon productions
                            first_sym2 = self.first[symbol2] - set([self.epsilon])
                            
                            # If first_sym2 - Follow(sym2) contains elements
                            if len(first_sym2 - self.follow[symbol1]) > 0:
                                changed = True
                                # Add first_sym2 to Follow(sym1)
                                self.follow[symbol1] |= first_sym

                    print("Next-follow: ", nt, self.follow[nt])
                    # last_item = Last production
                    last_item = prod[-1]
                    # If the last_item is in set of non-terminal and Follow(non-termina)-Follow(last_item) contains items
                    if last_item in self.nt and len(self.follow[nt] - self.follow[last_item]) > 0:
                        changed = True
                        # Add Follow(non-terminal) to Follow(last_item)
                        self.follow[last_item] |= self.follow[nt]

                    # If production exists
                    if len(prod) > 1:
                        # Get last production for non-terminal
                        last = prod[-1]
                        # If First(last) = epsilon
                        if self.epsilon in self.first[last]:
                            second_last = prod[-2]
                            # If Follow(non-terminal)-Follow(second_last) = 0
                            if len(self.follow[nt] - self.follow[second_last]) > 0:
                                changed = True
                                # Add Follow(non-terminal) to Follow(second last production)
                                self.follow[second_last] |= self.follow[nt]

    # Function to print a set
    def _print_set(self, pset):
        for symbol, f_set in filter(lambda x: x[0] != self.epsilon, sorted(pset.items(),key=lambda x: self.nt_order.index(x[0]) if x[0] in self.nt_order else len(self.nt_order) + 1)):
            if symbol not in self.terminals:
                print("{}\t:\t{}".format(symbol, ', '.join(sorted(filter(lambda x: x in self.symbols, f_set)))))

    # Function to return a set
    def _return_set(self, pset):
        set_to_consider = []
        for symbol, f_set in filter(lambda x: x[0] != self.epsilon, sorted(pset.items(),key=lambda x: self.nt_order.index(x[0]) if x[0] in self.nt_order else len(self.nt_order) + 1)):
            if symbol not in self.terminals:
                set_to_consider.append(str(symbol + " : " + ', '.join(sorted(filter(lambda x: x in self.symbols, f_set)))))
        return set_to_consider

    # Call to print first
    def print_first_set(self):
        self._print_set(self.first)

    # Call to print follow
    def print_follow_set(self):
        self._print_set(self.follow)

    def return_first_set(self):
        return self._return_set(self.first)

    def return_follow_set(self):
        return self._return_set(self.follow)

if __name__ == "__main__":
    file_contents = open("temp_rules.txt","r").read()

    grammar_in_consideration = GrammarParser(file_contents)
    print("\nFirst set\n")
    grammar_in_consideration.print_first_set()

    print("\n Follow set\n")
    grammar_in_consideration.print_follow_set()