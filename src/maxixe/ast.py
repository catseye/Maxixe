# encoding: UTF-8

class AST(object):
    def __init__(self, **kwargs):
        self.attrs = kwargs

    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__,
            ', '.join(['%s=%r' % (k, v) for k, v in self.attrs.iteritems()])
        )

    def __getattr__(self, name):
        if name in self.attrs:
            return self.attrs[name]
        raise AttributeError(name)


class Proof(AST):
    def get_rule(self, rule_name):
        return self.rule_map[rule_name]

    def get_block_rule(self, var):
        if var is None:
            return BlockRule(cases=[BlockRuleCase(initial=None, final=None)])
        return self.block_rule_map[var.name]

    def find_step_and_block(self, step_name):
        return self.step_map[step_name]


class Rule(AST):
    pass


class BlockRule(AST):
    pass


class BlockRuleCase(AST):
    pass


class Hyp(AST):
    def has_attribute(self, attribute):
        return attribute in self.attributes


class Subst(AST):
    pass


class Block(AST):
    def has_as_last_step(self, step):
        for case in self.cases:
            if case.has_as_last_step(step):
                return True
        return False


class BlockCase(AST):
    def has_as_last_step(self, step):
        return step == self.steps[-1]


class Step(AST):
    pass
