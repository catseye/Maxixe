from maxixe.ast import Block


class ProofStructureError(ValueError):
    pass


class ReasoningError(ValueError):
    pass


class Checker(object):
    def __init__(self, proof):
        self.proof = proof
        self.current_block = None
        self.local_atoms = set()
        self.used_atoms = set()
        self.current_step = None

    def check(self):
        if not self.proof.goal.is_ground():
            raise ProofStructureError("goal is not ground")

        self.check_block(self.proof.block)

        if self.current_step.term != self.proof.goal:
            raise ProofStructureError("proof does not reach goal")

    def check_block(self, block):
        prev_block, prev_local_atoms = self.current_block, self.local_atoms
        self.current_block, self.local_atoms = block, set()

        block_rule = self.proof.get_block_rule(self.current_block.name)
        if len(block_rule.cases) != len(block.cases):
            raise ProofStructureError("block must have same number of cases as block rule")
        last_term = None
        for (case_num, (block_rule_case, case)) in enumerate(zip(block_rule.cases, block.cases)):
            self.check_case(case_num + 1, block_rule_case, case)
            if last_term is None:
                last_term = case.steps[-1].term
            elif last_term != case.steps[-1].term:
                raise ProofStructureError("cases do not finish with same term")

        self.current_block, self.local_atoms = prev_block, prev_local_atoms

    def check_case(self, case_num, block_rule_case, case):
        if block_rule_case.initial is not None and case.steps[0].by.name != block_rule_case.initial.var.name:
            raise ProofStructureError("initial step of case %s of %s must use rule %s" %
                (case_num, self.current_block.name, block_rule_case.initial.var.name)
            )
        if block_rule_case.final is not None and case.steps[-1].by.name != block_rule_case.final.var.name:
            raise ProofStructureError("final step of case %s of %s must use rule %s" %
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
            if atom in final_atoms:
                raise ProofStructureError("Local atom '%s' cannot be used in final step of case" % atom)

    def check_step(self, step):
        block = self.current_block
        self.current_step = step
        rule = self.proof.get_rule(step.by.name)

        if len(rule.hypotheses) != len(step.with_):
            self.step_error("Number of arguments provided (%s) does not match number of hypotheses (%s)" %
                (len(step.with_), len(rule.hypotheses))
            )
        unifier = {}
        with_terms = []
        for (hypothesis, with_) in zip(rule.hypotheses, step.with_):
            if hypothesis.has_attribute('atom'):
                if not with_.is_atom():
                    self.step_error("argument '%s' to hypothesis '%s' is not an atom" % (with_, hypothesis))
                hypothesis.term.match(with_, unifier)
                with_term = with_
                if hypothesis.has_attribute('local'):
                    self.local_atoms.add(with_term)
            elif hypothesis.has_attribute('term'):
                hypothesis.term.match(with_, unifier)
                with_term = with_
                if hypothesis.has_attribute('nonlocal'):
                    atoms = set()
                    with_term.collect_atoms(atoms)
                    for atom in self.local_atoms:
                        if atom in atoms:
                            self.step_error("argument '%s' to hypothesis '%s' must not contain local atom '%s'" % (
                                with_, hypothesis, atom
                            ))
            else:
                with_step, from_block = self.proof.find_step_and_block(with_.name)
                if from_block.level > block.level:
                    if not from_block.has_as_last_step(with_step):
                        self.step_error('%s is a non-final step in an inner block' % with_.name)
                try:
                    hypothesis.term.match(with_step.term, unifier)
                except ValueError as e:
                    unifier_str = ", ".join(["%s -> %s" % (k, v) for k, v in unifier.iteritems()])
                    self.step_error(
                        "could not match '%s' with '%s' with unifier '%s': %s" % (
                            hypothesis.term, with_step.term, unifier_str, e
                        ), class_=ReasoningError
                    )
                with_term = with_step.term
            with_terms.append(with_term)
            if hypothesis.has_attribute('unique'):
                if with_term in self.used_atoms:
                    self.step_error("'%s' has already been used as an atom in this proof" % (step.by.name, with_term))

        instance = rule.conclusion.subst(unifier)
        if not instance.is_ground():
            self.step_error("Not all variables replaced during rule instantiation")

        instance = instance.resolve_substs(unifier)
        
        if instance != step.term:
            self.step_error("%s does not follow from %s with %s - it would be %s." % (
                step.term, step.by.name, ' ; '.join([str(t) for t in with_terms]), instance
            ), class_=ReasoningError)

        step.term.collect_atoms(self.used_atoms)

    def step_error(self, message, class_=ProofStructureError):
        message = "In %s, %s" % (self.current_step.var.name, message)
        raise class_(message)
