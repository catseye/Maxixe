# encoding: UTF-8


class Term(object):
    def __init__(self, constructor, subterms=None):
        if subterms is None:
            subterms = []
        self.constructor = constructor
        self.subterms = subterms

    def __str__(self):
        if len(self.subterms) == 0:
            return self.constructor
        return "%s(%s)" % (self.constructor, ', '.join([str(s) for s in self.subterms]))

    def __repr__(self):
        if self.subterms:
            return "%s(%r, subterms=%r)" % (
                self.__class__.__name__, self.constructor, self.subterms
            )
        else:
            return "%s(%r)" % (
                self.__class__.__name__, self.constructor
            )

    def __eq__(self, other):
        if not isinstance(other, Term):
            return False
        if self.constructor != other.constructor:
            return False
        if len(self.subterms) != len(other.subterms):
            return False
        for (st1, st2) in zip(self.subterms, other.subterms):
            if st1 != st2:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self))

    def is_atom(self):
        return len(self.subterms) == 0

    def is_ground(term):
        for subterm in term.subterms:
            if not subterm.is_ground():
                return False
        return True

    def contains(self, other):
        if self == other:
            return True
        for st in self.subterms:
            if st.contains(other):
                return True
        return False

    def replace(self, old, new):
        if self == old:
            return new
        else:
            return Term(self.constructor, subterms=[subterm.replace(old, new) for subterm in self.subterms])

    def match(self, term, unifier):
        if self.constructor != term.constructor:
            raise ValueError("`%s` != `%s`" % (self.constructor, term.constructor))
        if len(self.subterms) != len(term.subterms):
            raise ValueError("`%s` != `%s`" % (len(self.subterms), len(term.subterms)))
        for (subpat, subterm) in zip(self.subterms, term.subterms):
            subpat.match(subterm, unifier)

    def subst(self, unifier):
        return Term(self.constructor, subterms=[subterm.subst(unifier) for subterm in self.subterms])

    def resolve_substs(self, unifier):
        return Term(self.constructor, subterms=[subterm.resolve_substs(unifier) for subterm in self.subterms])

    def collect_atoms(self, atoms):
        if self.is_atom():
            atoms.add(self)
        else:
            for subterm in self.subterms:
                subterm.collect_atoms(atoms)


class Var(object):
    def __init__(self, name):
        assert name[0].isupper()
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.name)

    def __eq__(self, other):
        if not isinstance(other, Var):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def is_atom(self):
        return False

    def is_ground(term):
        return False

    def match(self, term, unifier):
        if self.name in unifier:
            unifier[self.name].match(term, unifier)
        else:
            unifier[self.name] = term

    def subst(self, unifier):
        return unifier[self.name]

    def resolve_substs(self, unifier):
        return self

    def collect_atoms(self, atoms):
        pass


class Substor(object):
    def __init__(self, subterm, substs):
        self.subterm = subterm
        self.substs = substs  # list of pairs of terms

    def __str__(self):
        substs_str = ", ".join(["%s -> %s" % (k, v) for k, v in self.substs])
        return "%s[%s]" % (self.subterm, substs_str)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.subterm, self.substs)

    def resolve_substs(self, unifier):
        instance = self.subterm
        for lhs, rhs in self.substs:
            lhs = lhs.subst(unifier)
            rhs = rhs.subst(unifier)
            if instance.contains(rhs):
                raise ValueError("'%s' already occurs in '%s'" % (rhs, instance))
            instance = instance.replace(lhs, rhs)
        return instance

    def is_ground(self):
        return self.subterm.is_ground()

    def subst(self, unifier):
        return Substor(self.subterm.subst(unifier), self.substs)
