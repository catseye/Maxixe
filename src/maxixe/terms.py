# encoding: UTF-8


class AbstractTerm(object):
    def is_atom(self):
        raise NotImplementedError

    def is_ground(self):
        raise NotImplementedError

    def equals(self, t2):
        raise NotImplementedError

    def replace(self, old, new):
        raise NotImplementedError

    def match(self, term, unifier):
        raise NotImplementedError

    def subst(self, unifier):
        raise NotImplementedError

    def collect_atoms(self, atoms):
        raise NotImplementedError


class Term(AbstractTerm):
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
            

    def is_atom(self):
        return len(self.subterms) == 0

    def is_ground(term):
        for subterm in term.subterms:
            if not subterm.is_ground():
                return False
        return True

    def equals(self, other):
        if not isinstance(other, Term):
            return False
        if self.constructor != other.constructor:
            return False
        if len(self.subterms) != len(other.subterms):
            return False
        for (st1, st2) in zip(self.subterms, other.subterms):
            if not st1.equals(st2):
                return False
        return True

    def replace(self, old, new):
        if self.equals(old):
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

    def collect_atoms(self, atoms):
        if self.is_atom():
            atoms.add(str(self))
        else:
            for subterm in self.subterms:
                subterm.collect_atoms(atoms)


class Var(AbstractTerm):
    def __init__(self, name):
        assert name[0].isupper()
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s(%r)" % (
            self.__class__.__name__, self.name
        )

    def is_atom(self):
        return False

    def is_ground(term):
        return False

    def equals(self, other):
        if not isinstance(other, Var):
            return False
        return self.name == other.name

    def match(self, term, unifier):
        if self.name in unifier:
            unifier[self.name].match(term, unifier)
        else:
            unifier[self.name] = term

    def subst(self, unifier):
        return unifier[self.name]

    def collect_atoms(self, atoms):
        pass
