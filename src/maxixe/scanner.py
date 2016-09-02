# encoding: UTF-8

import re


class Scanner(object):
    def __init__(self, text):
        self.text = text
        self.token = None
        self.type = None
        self.scan()

    def near_text(self, length=10):
        if len(self.text) < length:
            return self.text
        return self.text[:length]

    def scan_pattern(self, pattern, type, token_group=1, rest_group=2):
        pattern = r'^(' + pattern + r')(.*?)$'
        match = re.match(pattern, self.text, re.DOTALL)
        if not match:
            return False
        else:
            self.type = type
            self.token = match.group(token_group)
            self.text = match.group(rest_group)
            return True

    def scan(self):
        self.scan_pattern(r'[ \t\n\r]*', 'whitespace')
        while self.scan_pattern(r'\/\/.*?[\n\r]', 'comment'):
            self.scan_pattern(r'[ \t\n\r]*', 'whitespace')
        if not self.text:
            self.token = None
            self.type = 'EOF'
            return
        if self.scan_pattern(r'\=|\;|\|-|\,|\(|\)|\{|\}|\[|\]|\-\>', 'operator'):
            return
        if self.scan_pattern(r'[A-Z][a-zA-Z0-9_]*', 'variable'):
            return
        if self.scan_pattern(r'[a-z0-9][a-zA-Z0-9_]*', 'atom'):
            return
        if self.scan_pattern(r'.', 'unknown character'):
            return
        else:
            raise AssertionError("this should never happen, self.text=(%s)" % self.text)

    def expect(self, token):
        if self.token == token:
            self.scan()
        else:
            raise SyntaxError("Expected '%s', but found '%s' (near '%s')" %
                              (token, self.token, self.near_text()))

    def on(self, *tokens):
        return self.token in tokens

    def on_type(self, type):
        return self.type == type

    def check_type(self, type):
        if not self.type == type:
            raise SyntaxError("Expected %s, but found %s ('%s') (near '%s')" %
                              (type, self.type, self.token, self.near_text()))

    def consume(self, token):
        if self.token == token:
            self.scan()
            return True
        else:
            return False
