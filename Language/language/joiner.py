import re

from .scopes import Scope
from . import tokens #mutually dependent

class TokenStream():
    def __init__(self, tokenlist):
        self.tokenlist = tokenlist
        self.ptr = 0
        self.lpeekptr = 0
        self.rpeekptr = 0
        self.length = len(tokenlist)
    def rpeek(self):
        return self.tokenlist[self.ptr + self.rpeekptr]
    def lpeek(self):
        return self.tokenlist[self.ptr - self.lpeekptr - 1] if self.ptr - self.lpeekptr >= 0 else None
    def radvance(self):
        self.rpeekptr += 1
        return self.tokenlist[self.ptr + self.rpeekptr - 1]
    def ladvance(self):
        if (self.ptr - self.lpeekptr >= 1):
            self.lpeekptr += 1
            return self.tokenlist[self.ptr - self.lpeekptr]
        else: return None
    def passs(self):
        self.ptr += 1
    def take(self):
        returns = self.tokenlist[self.ptr - self.lpeekptr:self.ptr + self.rpeekptr]
        del self.tokenlist[self.ptr - self.lpeekptr:self.ptr + self.rpeekptr]
        self.length -= self.rpeekptr + self.lpeekptr
        self.ptr += -self.lpeekptr
        self.rpeekptr = 0
        self.lpeekptr = 0
        return returns
    def leave(self, value):
        self.tokenlist.insert(self.ptr, value)
        self.length += 1
        self.ptr += 1
    def turndown(self): self.rpeekptr = 0; self.lpeekptr = 0;
    def rpeekable(self):
        return self.ptr + self.rpeekptr < self.length
    def leftover(self):
        return self.ptr + self.rpeekptr == self.length + 1
    def ended(self):
        return self.ptr + self.rpeekptr == self.length

scope = Scope()
def rejoin(token_1s:tokens.Token_1) -> tokens.Token_2:
    tokenstream = TokenStream(token_1s)
    for token2class in tokens.token2_list:
        tokenstream.ptr = 0
        tokenstream.turndown()
        while (not tokenstream.ended()):
            if token2class.check(tokenstream):
                pass
            else:
                tokenstream.passs()
    return tokenstream