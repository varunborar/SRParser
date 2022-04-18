class SRParser:
    def __init__(self, CFG, Terminals, NonTerminals, Start):
        self.CFG = CFG
        self.Terminals = Terminals
        self.NonTerminals = NonTerminals
        self.start = Start

    def reduce(self, s, old, new, occurrence):
        li = s.rsplit(old, occurrence)
        return new.join(li)

    def parse(self, string: str):

        stack = "$"
        buffer = string + "$"
        headers = ["Stack", "Input Buffer", "Action"]

        outer = []
        action = ""

        # Perform Shift
        for terminal in self.Terminals:
            if buffer.startswith(terminal):
                action = f"SHIFT {terminal}"
                out = {"Stack": stack, "Input Buffer": buffer, "Action": action}
                outer.append(out)
                stack += terminal
                buffer = buffer[(len(terminal)):]
                break

        while buffer != "$" or stack != ("$" + self.start):

            # Check if reduce is possible
            reduced = False
            for symbol in self.CFG:
                for production in self.CFG[symbol]:
                    if stack.endswith(production):
                        reduced = True
                        action = f"REDUCE {symbol}->{production}"
                        out = {"Stack": stack, "Input Buffer": buffer, "Action": action}
                        outer.append(out)
                        stack = self.reduce(stack, production, symbol, 1)
                        break
                if reduced:
                    break

            if not reduced and buffer != "$":  # Reduce not possible perform shift
                for terminal in self.Terminals:
                    if buffer.startswith(terminal):
                        action = f"SHIFT {terminal}"
                        out = {"Stack": stack, "Input Buffer": buffer, "Action": action}
                        outer.append(out)
                        stack += terminal
                        buffer = buffer[(len(terminal)):]
                        break

            # ERROR CONDITIONS
            elif not reduced and buffer == "$" and stack != ("$" + self.start):  # Niether reduce nor shift possible
                action = f"ERROR"
                out = {"Stack": stack, "Input Buffer": buffer, "Action": action}
                outer.append(out)
                break

        if buffer == "$" and stack == ("$" + self.start):
            action = "ACCEPT"
            out = {"Stack": stack, "Input Buffer": buffer, "Action": action}
            outer.append(out)
        return outer


if __name__ == "__main__":
    CFG = {
        "S": ["(L)", "a"],
        "L": ["L,S", "S"]
    }
    Terminals = ["(", ")", "a", ","]
    NonTerminals = [ "L", "S" ]
    Start = "S"

    Parser = SRParser(CFG, Terminals, NonTerminals, Start)
    print(Parser.parse("(a)"))
