from maxixe.ast import Block


class Checker(object):
    def __init__(self, proof):
        self.proof = proof
        self.current_block = None
        self.local_atoms = set()
        self.used_atoms = set()
        self.last_step = None

    def check(self):
        assert self.proof.goal.is_ground(), "goal is not ground"
        for step in self.proof.steps:
            if isinstance(step, Block):
                self.check_block(step)
            else:
                self.check_step(step)

        if not self.last_step.term.equals(self.proof.goal):
            raise ValueError("proof does not reach goal")

    def check_block(self, block):
        prev_block, prev_local_atoms = self.current_block, self.local_atoms
        self.current_block, self.local_atoms = block, set()

        block_rule = self.proof.get_block_rule(self.current_block.name.name)
        if len(block_rule.cases) != len(block.cases):
            raise ValueError("block must have same number of cases as block rule")
        last_term = None
        for (case_num, (block_rule_case, case)) in enumerate(zip(block_rule.cases, block.cases)):
            self.check_case(case_num + 1, block_rule_case, case)
            if last_term is None:
                last_term = case.steps[-1].term
            elif not last_term.equals(case.steps[-1].term):
                raise ValueError("cases do not finish with same term")

        self.current_block, self.local_atoms = prev_block, prev_local_atoms

    def check_case(self, case_num, block_rule_case, case):
        if case.steps[0].by.name != block_rule_case.initial.var.name:
            raise ValueError("initial step of case %s of %s must use rule %s" %
                (case_num, self.current_block.name, block_rule_case.initial.var.name)
            )
        if block_rule_case.final is not None and case.steps[-1].by.name != block_rule_case.final.var.name:
            raise ValueError("final step of case %s of %s must use rule %s" %
                (case_num, self.current_block.name, block_rule_case.final.var.name)
            )

        for step in case.steps:
            if isinstance(step, Block):
                self.check_block(step)
            else:
                self.check_step(step)

        final_atoms = set()
        case.steps[-1].term.collect_atoms(final_atoms)
        for atom in self.local_atoms:
            if str(atom) in final_atoms:
                raise ValueError("Local atom '%s' cannot be used in final step of case" % atom)

    def check_step(self, step):
        block = self.current_block
        self.last_step = step
        rule = self.proof.get_rule(step.by.name)

        if len(rule.hypotheses) != len(step.with_):
            raise ValueError("In %s, Number of arguments provided (%s) does not match number of hypotheses (%s)" %
                (step.var.name, len(step.with_), len(rule.hypotheses))
            )
        unifier = {}
        with_terms = []
        for (hypothesis, with_) in zip(rule.hypotheses, step.with_):
            if hypothesis.has_attribute('atom'):
                assert with_.is_atom(), "argument '%s' to hypothesis '%s' is not an atom" % (with_, hypothesis)
                hypothesis.term.match(with_, unifier)
                with_term = with_
                if hypothesis.has_attribute('local'):
                    self.local_atoms.add(with_term)
            elif hypothesis.has_attribute('term'):
                hypothesis.term.match(with_, unifier)
                with_term = with_
            else:
                with_step, from_block = self.proof.find_step_and_block(with_.name)
                level = 0 if block is None else block.level
                from_level = 0 if from_block is None else from_block.level
                if from_level > level:
                    if not from_block.has_as_last_step(with_step):
                        raise ValueError('%s is a non-final step in an inner block' % with_.name)
                try:
                    hypothesis.term.match(with_step.term, unifier)
                except ValueError as e:
                    unifier_str = ", ".join(["%s -> %s" % (k, v) for k, v in unifier.iteritems()])
                    raise ValueError("In %s, could not match '%s' with '%s' with unifier '%s': %s" % (step.var.name, hypothesis.term, with_step.term, unifier_str, e))
                with_term = with_step.term
            with_terms.append(with_term)
            if hypothesis.has_attribute('unique'):
                if str(with_term) in self.used_atoms:
                    raise ValueError("In %s, '%s' has already been used as an atom in this proof" % (step.by.name, with_term))

        instance = rule.conclusion.subst(unifier)
        assert instance.is_ground(), "Not all variables replaced during rule instantiation"

        instance = instance.resolve_substs(unifier)
        
        if not instance.equals(step.term):
            raise ValueError("%s does not follow from %s with %s - it would be %s." % (
                step.term, step.by.name, ' ; '.join([str(t) for t in with_terms]), instance
            ))

        step.term.collect_atoms(self.used_atoms)
