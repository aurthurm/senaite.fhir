# -*- coding: utf-8 -*-

import re

RX = re.compile(r"\S+( \S+)*")


class Code(str):
    """A code is restricted to a string which has at least one character and
    no leading or trailing whitespace, and where there is no whitespace other
    than single spaces in the contents
    """

    def __init__(self, code):
        super(Code, self).__init__(code.strip())
        if not RX.match(self):
            raise ValueError("Wrong code")
