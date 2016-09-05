Maxixe
======

This document describes the Maxixe proof-checking language.

It contains many examples of proofs written in Maxixe.  These examples
are written in [Falderal][] format so that, as well as illustrating the
language for human readers, they can be automatically checked and thus
serve as a test suite.

However, because these examples are designed to show what is and what
is not valid in Maxixe, these proofs are neither particularly realistic
nor particularly interesting.  For examples of proofs that are more
interesting than these, please see the [Examples.md](Examples.md) document.

Note that in these examples the `===> ok` or the `???>` line is not part
of the proof (or even part of Maxixe's syntax); these lines are for
Falderal's benefit.

[Falderal]:     http://catseye.tc/node/Falderal

    -> Tests for functionality "Check Maxixe proof"

Basic Proof Structure
---------------------

A Maxixe proof consists of 3 sections: `given`, in which rules of inference
(including axioms and premises) are defined; `show`, which declares the goal
of the proof; and `proof`, which lists the steps to derive the goal from
the rules.

This is probably the shortest possible valid proof that can be written in
Maxixe (as well as the least interesting one).  It proves exactly what is
stated as a premise.

    given
        A = |- a
    show
        a
    proof
        C = a by A
    qed
    ===> ok

### Rules ###

In Maxixe we often call rules of inference just 'rules' for short.

A rule of inference consists of a name, an equals sign (`=`), a semicolon-separated
list of zero or more hypotheses, a turnstile (`|-`), and a conclusion.

A name must start with an upper-case letter and otherwise consists of alphanumeric
characters and underscores.

    given
        foo = |- a
    show
        a
    proof
        C = a by A
    qed
    ???> Expected variable, but found atom

No two rules may have the same name.

    given
        A = |- a
        A = |- b
    show
        a
    proof
        C = a by A
    qed
    ???> name has already been used for a rule of inference

Each hypothesis is a term, and so is the conclusion.  A term is given by a _constructor_,
which starts with a lower-case letter or a decimal digit and otherwise consists of
alphanumeric characters and underscores, followed by an optional comma-separated list
of subterms enclosed in parentheses.  A term with no subterms is called an _atom_.

    given
        A = atom_1 |- atom_2
        B =        |- term(subterm(a, b), c)
    show
        term(subterm(a, b), c)
    proof
        C = term(subterm(a, b), c) by B
    qed
    ===> ok

A term may also be a _variable_, in which case it starts with an upper-case letter.
Variables play a special role in the proof-checking process.

TODO: describe pattern-matching here!

    given
        Rule    = P |- and(P, P)
        Premise =   |- foo
    show
        and(foo, foo)
    proof
        S1 = foo           by Premise
        S2 = and(foo, foo) by Rule with S1
    qed
    ===> ok

The conclusion may not contain any variables which do not appear in the hypotheses.

    given
        Rule    = P |- and(P, Q)
        Premise =   |- foo
    show
        and(foo, foo)
    proof
        S1 = foo           by Premise
        S2 = and(foo, foo) by Rule with S1
    qed
    ???> Q

### Goal ###

The term given as the goal of a proof must not contain any variables.

    given
        A = |- a
    show
        A
    proof
        C = a by A
    qed
    ???> goal is not ground

### Steps ###

Each step in a proof consists of a name, an equals sign, a term, and a justification.

    given
        A = |- a
    show
        a
    proof
        a by A
    qed
    ???> Expected variable, but found atom

A step may not have the same name as a rule of inference.

    given
        A = |- a
    show
        a
    proof
        A = a by A
    qed
    ???> name has already been used for a rule of inference

No two steps may have the same name.

    given
        A = |- a
    show
        a
    proof
        C = a by A
        C = a by A
    qed
    ???> name has already been used for a step

Each step in a proof must name the rule being used in the justification (the `by` part)
of the step.

    given
        A = |- a
    show
        a
    proof
        C = a
    qed
    ???> Expected 'by'

The term given in a step of a proof must not contain any variables.

    given
        A = |- a
    show
        a
    proof
        C = Foo by A
    qed
    ???> 

If the rule named in the step of the proof has one or more hypotheses, the step
must also give _arguments_ to use in _instantiating_ the rule.  It must give exactly
one argument for every hypothesis.

    given
        Rule    = P |- and(P, P)
        Premise =   |- foo
    show
        and(foo, foo)
    proof
        S1 = foo           by Premise
        S2 = and(foo, foo) by Rule
    qed
    ???> Number of arguments provided (0) does not match number of hypotheses (1)

    given
        Rule    = P |- and(P, P)
        Premise =   |- foo
    show
        and(foo, foo)
    proof
        S1 = foo           by Premise
        S2 = and(foo, foo) by Rule with S1, S1
    qed
    ???> Number of arguments provided (2) does not match number of hypotheses (1)

The rule named in the justification must be one of the defined rules of inference.

    given
        Rule    = P |- and(P, P)
        Premise =   |- foo
    show
        and(foo, foo)
    proof
        S1 = foo           by Premise
        S2 = and(foo, foo) by Zanzibar_Land with S1
    qed
    ???> Zanzibar_Land

    given
        Rule    = P |- and(P, P)
        Premise =   |- foo
    show
        and(foo, foo)
    proof
        S1 = foo           by Premise
        S2 = and(foo, foo) by S1 with S1
    qed
    ???> S1

In most cases, the arguments given in the justification must be names of steps.
that occur before the current step in the proof.

    given
        Rule    = P |- and(P, P)
        Premise =   |- foo
    show
        and(foo, foo)
    proof
        S1 = foo           by Premise
        S2 = and(foo, foo) by Rule with Zanzibar_Land
    qed
    ???> Zanzibar_Land

    given
        Rule    = P |- and(P, P)
        Premise =   |- foo
    show
        and(foo, foo)
    proof
        S1 = foo           by Premise
        S2 = and(foo, foo) by Rule with Premise
    qed
    ???> Premise

Importantly, the steps given as arguments in a justification must occur *before*
the current step of the proof.

    given
        Rule    = P |- and(P, P)
        Premise =   |- foo
    show
        and(foo, foo)
    proof
        S1 = foo           by Premise
        S2 = and(foo, foo) by Rule with S2
    qed
    ???> In step 'S2': Step name 'S2' in with is not the name of a preceding step

Importantly, the term given in a step of a proof must follow from the rule and
arguments given in the step's justification.

    given
        A = |- a
    show
        a
    proof
        C = foo by A
    qed
    ???> foo does not follow from A

Importantly, the term in the last step in the proof must equal the term given
in `show`.

    given
        A = |- a
    show
        foo
    proof
        C = a by A
    qed
    ???> proof does not reach goal

Attributes and Substitution
---------------------------

Here is the exception to the rule that an argument in a justification must be
the name of a step.  Hypotheses may be decorated with _attributes_ in curly
braces.  If a hypothesis is given the attribute `term`, the argument may be
any ground term.

    given
        A = X{term} |- foo(X)
    show
        foo(zing(bar))
    proof
        C = foo(zing(bar)) by A with zing(bar)
    qed
    ===> ok

    given
        A = X{term} |- foo(X)
    show
        foo(zing(bar))
    proof
        C = foo(zing(bar)) by A with zing(Foo)
    qed
    ???> Not all variables replaced during rule instantiation

If a hypothesis is given the attribute `atom`, the argument may be any atom.

    given
        A = X{atom} |- foo(X)
    show
        foo(bar)
    proof
        C = foo(bar) by A with bar
    qed
    ===> ok

    given
        A = X{atom} |- foo(X)
    show
        foo(zing(bar))
    proof
        C = foo(zing(bar)) by A with zing(bar)
    qed
    ???> not an atom

The conclusion may be optionally followed by a substitution, which is a
comma-separated list of term-term pairs enclosed in square brackets.
If a substitution is given, all the terms will be replaced by the other
terms after conclusion has been derived.

    given
        A       = P ; X{atom} |- P[f->X]
        Premise =             |- foo(f)
    show
        foo(bar)
    proof
        S1 = foo(f)   by Premise
        S2 = foo(bar) by A with S1, bar
    qed
    ===> ok

    given
        A       = P ; X{atom} |- P[X->f]
        Premise =             |- foo(bar)
    show
        foo(f)
    proof
        S1 = foo(bar) by Premise
        S2 = foo(f)   by A with S1, bar
    qed
    ===> ok


Subproofs
---------

A proof may consist of nested subproofs, called _blocks_.  Each block must be introduced by
instantiating a specially-declared _block rule_.  The structure of a block rule determines
rules determine the structure of the block.

A block rule (and thus a block) consists of one or more _cases_.  Each case contains one
or two non-block rules.  The first rule must be used in the first step of the case, and
the second rule, if given, must be used in the final step of the case.

    given
        A =   |- a
        block Subproof
            case
                B = a |- b
                C = b |- c
            end
        end
        D = c |- d
    show
        d
    proof
        S1 = a by A
        block Subproof
            case
                S2 = b by B with S1
                S3 = c by C with S2
            end
        end
        S4 = d by D with S3
    qed
    ===> ok

If the second rule is not given, no restriction is placed on the final step of the case.

    given
        A =   |- a
        block Subproof
            case
                B = a |- b
            end
        end
        C = b |- c
        D = c |- d
    show
        d
    proof
        S1 = a by A
        block Subproof
            case
                S2 = b by B with S1
                S3 = c by C with S2
            end
        end
        S4 = d by D with S3
    qed
    ===> ok

As an act of syntactic sugar, if a block contains only one case, the `case` ... `end`
may be omitted, both in the proof, and in the rule definition.

    given
        A =   |- a
        block Subproof
            B = a |- b
        end
        C = b |- c
        D = c |- d
    show
        d
    proof
        S1 = a by A
        block Subproof
            S2 = b by B with S1
            S3 = c by C with S2
        end
        S4 = d by D with S3
    qed
    ===> ok

Blocks may contain other blocks.

    given
        A =   |- a
        block Subproof
            case
                B = a |- b
                C = b |- c
            end
        end
        D = c |- d
    show
        d
    proof
        S1 = a by A
        block Subproof
            case
                S2 = b by B with S1
                block Subproof
                    case
                        S3 = b by B with S1
                        S4 = c by C with S3
                    end
                end
                S5 = c by C with S2
            end
        end
        S6 = d by D with S5
    qed
    ===> ok

A step may refer to any preceding step in the same block, or in any
outer block (i.e. any block that contains the current block.)

    given
        A =   |- a
        block Subproof
            case
                B = a |- b
                C = b |- c
            end
        end
        D = c |- d
    show
        d
    proof
        S1 = a by A
        S2 = a by A
        block Subproof
            case
                S3 = b by B with S1
                S4 = b by B with S2
                S5 = c by C with S3
                S6 = c by C with S4
            end
        end
        S7 = d by D with S6
    qed
    ===> ok

However, a step may only refer to the _final_ step in any inner block
(i.e. any block that is contained by the current block.)

    given
        A =   |- a
        block Subproof
            case
                B = a |- b
                C = b |- c
            end
        end
        D = c |- d
    show
        c
    proof
        S1 = a by A
        block Subproof
            case
                S2 = b by B with S1
                S3 = c by C with S2
            end
        end
        S4 = c by C with S2
    qed
    ???> S2 is a non-final step in an inner block

The rule in the justification of the first step in a case must be the initial
rule specified for the case in the block rule.

    given
        A =   |- a
        block Subproof
            case
                B = a |- b
                C = b |- c
            end
        end
        D = c |- d
    show
        d
    proof
        S1 = a by A
        block Subproof
            case
                Sw = a by A
                S2 = b by B with S1
                S3 = c by C with S2
            end
        end
        S4 = d by D with S3
    qed
    ???> initial step of case 1 of Subproof must use rule B

The rule in the justification of the last step in a case must be the final
rule specified for the case in the block rule.

    given
        A =   |- a
        block Subproof
            case
                B = a |- b
                C = b |- c
            end
        end
        D = c |- d
        E = a |- c
    show
        d
    proof
        S1 = a by A
        block Subproof
            case
                S2 = b by B with S1
                S3 = c by C with S2
                S4 = c by E with S1
            end
        end
        S5 = d by D with S4
    qed
    ???> final step of case 1 of Subproof must use rule C

A block in a proof must have the same number of cases as the block rule used.

    given
        A =   |- a
        B = a |- b
        C = a |- c
        block Subproof
            case
                D = b |- d
                E = X |- X
            end
            case
                F = c |- d
                G = X |- X
            end
        end
        H = X |- X
    show
        d
    proof
        S1 = a by A
        S2 = b by B with S1
        S3 = c by C with S1
        block Subproof
            case
                S4 = d by D with S2
                S5 = d by E with S4
            end
            case
                S6 = d by F with S3
                S7 = d by G with S6
            end
        end
        S8 = d by H with S5
    qed
    ===> ok

    given
        A =   |- a
        B = a |- b
        C = a |- c
        block Subproof
            case
                D = b |- d
                E = X |- X
            end
            case
                F = c |- d
                G = X |- X
            end
        end
        H = X |- X
    show
        d
    proof
        S1 = a by A
        S2 = b by B with S1
        S3 = c by C with S1
        block Subproof
            case
                S4 = d by D with S2
                S5 = d by E with S4
            end
        end
        S8 = d by H with S5
    qed
    ???> block must have same number of cases as block rule

    given
        A =   |- a
        B = a |- b
        C = a |- c
        block Subproof
            case
                D = b |- d
                E = X |- X
            end
        end
        H = X |- X
    show
        d
    proof
        S1 = a by A
        S2 = b by B with S1
        S3 = c by C with S1
        block Subproof
            case
                S4 = d by D with S2
                S5 = d by E with S4
            end
            case
                S6 = d by D with S3
                S7 = d by E with S6
            end
        end
        S8 = d by H with S5
    qed
    ???> block must have same number of cases as block rule

When a block has multiple cases, the last step in each case must contain
the same term.

    given
        A =   |- a
        B = a |- b
        C = a |- c
        block Subproof
            case
                D = b |- d
                E = X |- X
            end
            case
                F = c |- d
                G = X |- X
            end
        end
        H = X |- X
    show
        d
    proof
        S1 = a by A
        S2 = b by B with S1
        S3 = c by C with S1
        block Subproof
            case
                S4 = d by D with S2
                S5 = d by E with S4
            end
            case
                S6 = d by F with S3
                Sw = c by H with S3
                S7 = c by G with Sw
            end
        end
        S8 = d by H with S5
    qed
    ???> cases do not finish with same term

### Locals ###

If a hypothesis has the `local` attribute, its argument must be an atom, and that atom may
only occur in the block in which the hypothesis is invoked.  To enforce this, because outer
blocks may only access the final step of a case in a block anyway, we only need check that
it does not occur in the final step of any case of the block.

    given
        A =   |- a
        block Subproof
            case
                B = a ; Q{local atom} |- Q
                C = b                 |- c
            end
        end
        D = c |- d
    show
        d
    proof
        S1 = a by A
        block Subproof
            case
                S2 = b by B with S1, b
                S3 = c by C with S2
            end
        end
        S4 = d by D with S3
    qed
    ===> ok

    given
        A =   |- a
        block Subproof
            case
                B = a ; Q{local atom} |- Q
                C = Any               |- Any
            end
        end
        D = Any |- Any
    show
        b
    proof
        S1 = a by A
        block Subproof
            case
                S2 = b by B with S1, b
                S3 = b by C with S2
            end
        end
        S4 = b by D with S3
    qed
    ???> Local atom 'b' cannot be used in final step of case
