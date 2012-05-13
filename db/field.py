
class Field(object):
    def __init__(self, name, type, extras = "", primary = False):
        self.name = name
        if type.__class__ is (str, unicode):
            type = getClassByName(type)
        self.type = type
        self.extras = extras
        self.primary = primary

    def __repr__(self):
        return "[Field %s: %s%s]" % (self.name, self.type.__name__, (" (primary)" if self.primary else ""))

    @property
    def sqlType(self):
        t = ""
        if self.type == int:
            t = "INTEGER"
        elif self.type in (str, unicode):
            t = "VARCHAR(255)"

        if self.extras:
            t += " " + self.extras

        if self.primary:
            if self.type == int:
                t += " PRIMARY KEY"
            else:
                t += " PRIMARY KEY"

        return t
