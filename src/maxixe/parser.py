# encoding: UTF-8

from maxixe.ast import Proof, Rule, BlockRule, BlockRuleCase, Hyp, Subst, Block, BlockCase, Step
from maxixe.terms import Term, Var, Substor
from maxixe.scanner import Scanner


# Proof         ::= "given" {Rule | BlockRule} "show" Term "proof" {Step | Block} "qed".
# Rule          ::= Var Attributes "=" [Hyp {";" Hyp}] "|-" Term.
# BlockRule     ::= "block" Var ({BlockRuleCase} | Rule [Rule]) "end".
# BlockRuleCase ::= "case" Rule [Rule] "end".
# Hyp           ::= Term Attributes.
# Attributes    ::= ["{" {Atom} "}"].
# Block         ::= "block" Var ({BlockCase} | {Step | Block}) "end".
# BlockCase     ::= "case" {Step | Block} "end".
# Step          ::= Var "=" Term "by" Var ["with" Term {"," Term}].
# Term          ::= Var | Atom ["(" Term {"," Term} ")"] ["[" Subst {"," Subst} "]"].
# Subst         ::= Term "->" Term.
# Var           ::= <<A-Z followed by alphanumeric + _>>
# Atom          ::= <<a-z0-9 followed by alphanumeric + _>>


class Parser(object):
    def __init__(self, text):
        self.scanner = Scanner(text)
        self.current_block = None
        self.rule_map = {}
        self.block_rule_map = {}
        self.step_map = {}

    def proof(self):
        rules = []
        self.scanner.expect('given')
        while not self.scanner.on('show'):
            if self.scanner.on('block'):
                rules.append(self.block_rule())
            else:
                rules.append(self.rule())
        self.scanner.expect('show')
        goal = self.term()
        self.scanner.expect('proof')
        block = self.block(0)
        self.scanner.expect('qed')
        return Proof(
            rules=rules, goal=goal, block=block,
            rule_map=self.rule_map, block_rule_map=self.block_rule_map, step_map=self.step_map
        )

    def rule(self):
        hypotheses = []
        var = self.var()
        self.scanner.expect('=')
        if not self.scanner.on('|-'):
            hypotheses.append(self.hyp())
            while self.scanner.consume(';'):
                hypotheses.append(self.hyp())
        self.scanner.expect('|-')
        conclusion = self.term()
        rule = Rule(var=var, hypotheses=hypotheses, conclusion=conclusion)
        if var.name in self.rule_map:
            raise ValueError("name has already been used for a rule of inference")
        self.rule_map[var.name] = rule
        return rule

    def block_rule(self):
        cases = []
        self.scanner.expect('block')
        name = self.var()
        if self.scanner.on('case'):
            while self.scanner.on('case'):
                self.scanner.expect('case')
                cases.append(self.block_rule_case())
                self.scanner.expect('end')
        else:
            cases.append(self.block_rule_case())
        self.scanner.expect('end')
        block_rule = BlockRule(name=name, cases=cases)
        self.block_rule_map[name.name] = block_rule
        return block_rule

    def block_rule_case(self):
        initial = self.rule()
        final = None
        if not self.scanner.on('end'):
            final = self.rule()
        return BlockRuleCase(initial=initial, final=final)

    def hyp(self):
        term = self.term()
        attributes = self.attributes()
        return Hyp(term=term, attributes=attributes)

    def attributes(self):
        attributes = []
        if self.scanner.consume('{'):
            while not self.scanner.on('}'):
                attribute = self.scanner.token
                self.scanner.scan()
                attributes.append(attribute)
            self.scanner.expect('}')
        return attributes

    def block(self, level):
        cases = []
        name = None if level == 0 else self.var()
        prev_block = self.current_block
        block = Block(name=name, cases=cases, level=level)
        self.current_block = block
        if self.scanner.on('case'):
            while self.scanner.on('case'):
                self.scanner.expect('case')
                cases.append(self.block_case(level))
                self.scanner.expect('end')
        else:
            cases.append(self.block_case(level))
        self.current_block = prev_block
        return block

    def block_case(self, level):
        steps = []
        while not self.scanner.on('end', 'qed'):
            if self.scanner.consume('block'):
                steps.append(self.block(level + 1))
                self.scanner.expect('end')
            else:
                steps.append(self.step())
        return BlockCase(steps=steps)

    def step(self):
        var = self.var()
        self.scanner.expect('=')
        term = self.term()
        self.scanner.expect('by')
        by = self.var()
        with_ = []
        if self.scanner.consume('with'):
            with_.append(self.term())
            while self.scanner.consume(','):
                with_.append(self.term())
        step = Step(var=var, term=term, by=by, with_=with_)
        if var.name in self.rule_map:
            raise ValueError("name has already been used for a rule of inference")
        if var.name in self.step_map:
            raise ValueError("name has already been used for a step")
        # TODO: complication here: if the hypothesis to use this in is free, skip this step.
        # for now, approximate that with: if with_var is not a variable, skip this step.
        for with_var in with_:
            if not isinstance(with_var, Var):
                continue
            if with_var.name not in self.step_map:
                raise ValueError("In step '%s': Step name '%s' in with is not the name of a preceding step" %
                    (var.name, with_var.name)
                )
        self.step_map[var.name] = (step, self.current_block)
        return step

    def term(self):
        return self.basic_term()

    def basic_term(self):
        if self.scanner.on_type('variable'):
            return self.var()
        self.scanner.check_type('atom')
        constructor = self.scanner.token
        self.scanner.scan()
        subterms = []
        if self.scanner.consume('('):
            subterms.append(self.term())
            while self.scanner.consume(','):
                subterms.append(self.term())
            self.scanner.expect(')')
        term = Term(constructor, subterms=subterms)
        return self.substs(term)

    def var(self):
        self.scanner.check_type('variable')
        name = self.scanner.token
        self.scanner.scan()
        term = Var(name)
        return self.substs(term)

    def substs(self, term):
        substs = []
        if self.scanner.consume('['):
            substs.append(self.subst())
            while self.scanner.consume(','):
                substs.append(self.subst())
            self.scanner.expect(']')
        if substs:
            return Substor(term, substs)
        else:
            return term

    def subst(self):
        lhs = self.term()
        self.scanner.expect('->')
        rhs = self.term()
        return (lhs, rhs)


# Term          ::= Term0 {"∨" Term0}.
# Term0         ::= Term1 {"∧" Term1}.
# Term1         ::= BasicTerm.


class SugaredParser(Parser):

    def term(self):
        term_a = self.term0()
        while self.scanner.consume(u'∨'):
            term_b = self.term0()
            term_a = Term('or', [term_a, term_b])
        return term_a

    def term0(self):
        term_a = self.term1()
        while self.scanner.consume(u'∧'):
            term_b = self.term1()
            term_a = Term('and', [term_a, term_b])
        return term_a

    def term1(self):
        return self.basic_term()
