Examples of Proofs in Maxixe
============================

Note that in these examples the `===> ok` is not part of the proof (or
even part of Maxixe's syntax); these lines are for Falderal's benefit.

    -> Tests for functionality "Check Maxixe proof"

Propositional Logic
-------------------

The rules of inference from pages 8-15 of [these slides](http://www.inf.ed.ac.uk/teaching/courses/dmmr/slides/13-14/Ch1c.pdf)
plus the proof on page 17 of same (which only uses a small subset of the rules.)

That proof uses the fact that conjunction is commutative without stating it,
so we've added it as a rule here.

Note that we could also, in this case, have two rules for Simplification
(Left Simplification and Right Simplification) and we have in fact used
that approach in other example proofs in these documents.

Or, we could have stated the rule as an "axiom schema" like
`impl(and(P, Q), and(Q, P))` and used Modus Ponens.  However, Maxixe does
require at least one hypothesis on the LHS of a rule, so we would need to
write it like `and(P, Q) |- impl(and(P, Q), and(Q, P))`.

    given
        Modus_Ponens                 = impl(P, Q)    ; P           |- Q
        Modus_Tollens                = impl(P, Q)    ; not(Q)      |- not(P)
        Hypothetical_Syllogism       = impl(P, Q)    ; impl(Q, R)  |- impl(P, R)
        Disjunctive_Syllogism        = or(P, Q)      ; not(P)      |- Q
        Addition                     = P                           |- or(P, Q)
        Simplification               = and(P, Q)                   |- Q
        Conjunction                  = P             ; Q           |- and(P, Q)
        Resolution                   = or(not(P, R)) ; or(P, Q)    |- or(Q, R)
    
        Commutativity_of_Conjunction = and(P, Q)                   |- and(Q, P)
    
        Premise                      =                             |- and(p, impl(p, q))
    show
        q
    proof
        Step_1 = and(p, impl(p, q))              by Premise
        Step_2 = and(impl(p, q), p)              by Commutativity_of_Conjunction with Step_1
        Step_3 = impl(p, q)                      by Simplification with Step_1
        Step_4 = p                               by Simplification with Step_2
        Step_5 = q                               by Modus_Ponens with Step_3, Step_4
    qed
    ===> ok

### Supposition ###

A proof that from a→(b→c) and a→b and d, we can conclude (a→c)^d.

    given
        Modus_Ponens           = impl(P, Q) ; P |- Q
        Conjunction            = P          ; Q |- and(P, Q)
        block Suppose
            case
                Supposition    = A{term}        |- A
                Conclusion     = P ; Q          |- impl(P, Q)
            end
        end
    
        Premise_1              =                |- impl(a, impl(b, c))
        Premise_2              =                |- impl(a, b)
        Premise_3              =                |- d
    show
        and(impl(a, c), d)
    proof
        Step_1 = impl(a, impl(b, c))   by Premise_1
        Step_2 = impl(a, b)            by Premise_2
        Step_3 = d                     by Premise_3
        block Suppose
            case
                Step_4 = a             by Supposition with a
                Step_5 = impl(b, c)    by Modus_Ponens with Step_1, Step_4
                Step_6 = b             by Modus_Ponens with Step_2, Step_4
                Step_7 = c             by Modus_Ponens with Step_5, Step_6
                Step_8 = impl(a, c)    by Conclusion with Step_4, Step_7
            end
        end
        Step_9 = and(impl(a, c), d)    by Conjunction with Step_8, Step_3
    qed
    ===> ok

### Reasoning by Cases ###

A proof that disjunction is commutative.

    given
        Modus_Ponens            = impl(P, Q) ; P |- Q
        Disj_Intro_Left         = P ; Q{term}    |- or(Q, P)
        Disj_Intro_Right        = P ; Q{term}    |- or(P, Q)
        block Disjunction
            case
                Disj_Elim_Left  = or(P, Q)       |- P
                Disj_Conc_Left  = P              |- P
            end
            case
                Disj_Elim_Right = or(P, Q)       |- Q
                Disj_Conc_Right = P              |- P
            end
        end
        Tautology               = P              |- P
        Premise                 =                |- or(a, b)
    show
        or(b, a)
    proof
        Step_1 = or(a, b)      by Premise
        block Disjunction
            case
                Step_2 = a                                by Disj_Elim_Left with Step_1
                Step_3 = or(b, a)                         by Disj_Intro_Left with Step_2, b
                Step_4 = or(b, a)                         by Disj_Conc_Left with Step_3
            end
            case
                Step_5 = b                                by Disj_Elim_Right with Step_1
                Step_6 = or(b, a)                         by Disj_Intro_Right with Step_5, a
                Step_7 = or(b, a)                         by Disj_Conc_Right with Step_6
            end
        end
        Step_8 = or(b, a)                                 by Tautology with Step_7
    qed
    ===> ok

Predicate Logic
---------------

### Universal Generalization (UG) ###

The following is adapted from the "short, dull proof" from page 13 of John C. Reynold's
_Theories of Programming Languages_.

In the original, the rules of inference aren't named, and the 2nd one (Commutivity_of_Equality)
is an "axiom schema" which has no hypotheses.  Maxixe requires that every variable on the RHS
of a turnstile can be filled out by a variable on the LHS, so I've taken the liberty of turning
it into a rule.

The atom introduced as the variable in the `forall` must be unique (i.e. not used previously in
the proof.)  This implements scope.  Without that restriction, it is possible to confuse
arbitrary and particular variables and write proofs that make no sense.

We use `c(zero)` to represent zero because we can't use `zero` because then you could use it as
a variable name and say something silly like `forall(zero, ...)`.

    given
        Premise                  =                               |- eq(add(x, c(zero)), x)
        Commutivity_of_Equality  = eq(E1, E0)                    |- impl(eq(E1, E0), eq(E0, E1))
        Modus_Ponens             = P0 ; impl(P0, P1)             |- P1
        Universal_Generalization = P  ; X{term} ; V{unique atom} |- forall(V, P)[X -> V]
    show
        forall(y, eq(y, add(y, c(zero))))
    proof
        Step_1 = eq(add(x, c(zero)), x)                                 by Premise
        Step_2 = impl(eq(add(x, c(zero)), x), eq(x, add(x, c(zero))))   by Commutivity_of_Equality with Step_1
        Step_3 = eq(x, add(x, c(zero)))                                 by Modus_Ponens with Step_1, Step_2
        Step_4 = forall(y, eq(y, add(y, c(zero))))                      by Universal_Generalization with Step_3, x, y
    qed
    ===> ok

### Universal Instantiation (UI) ###

All bugs are creepy and all bugs are crawly therefore all bugs are both creepy and crawly.

Note that the term introduced as the variable in the UI need *not* be unique, because if
something is true for all `x`, it is true for *all* `x`, even if `x` is something else
you've already been thinking about and given the name `x`.

Note that it also need not be an atom.

    given
        Modus_Ponens             = impl(P, Q)    ; P             |- Q
        Conjunction              = P             ; Q             |- and(P, Q)
        block Suppose
            case
                Supposition    = A{term}        |- A
                Conclusion     = P ; Q          |- impl(P, Q)
            end
        end
    
        Universal_Generalization = P ; X{term} ; V{unique atom}  |- forall(V, P)[X -> V]
        Universal_Instantiation  = forall(X, P) ; V{term}        |- P[X -> V]
    
        Premise_1                = |- forall(x, impl(bug(x), creepy(x)))
        Premise_2                = |- forall(x, impl(bug(x), crawly(x)))
    show
        forall(k, impl(bug(k), and(creepy(k), crawly(k))))
    proof
        Step_1 = forall(x, impl(bug(x), creepy(x)))                   by Premise_1
        Step_2 = impl(bug(x), creepy(x))                              by Universal_Instantiation with Step_1, x
        Step_3 = forall(x, impl(bug(x), crawly(x)))                   by Premise_2
        Step_4 = impl(bug(x), crawly(x))                              by Universal_Instantiation with Step_3, x
        block Suppose
            case
                Step_5 = bug(x)                                       by Supposition with bug(x)
                Step_6 = creepy(x)                                    by Modus_Ponens with Step_2, Step_5
                Step_7 = crawly(x)                                    by Modus_Ponens with Step_4, Step_5
                Step_8 = and(creepy(x), crawly(x))                    by Conjunction with Step_6, Step_7
                Step_9 = impl(bug(x), and(creepy(x), crawly(x)))      by Conclusion with Step_5, Step_8
            end
        end
        Step_10 = forall(k, impl(bug(k), and(creepy(k), crawly(k))))  by Universal_Generalization with Step_9, x, k
    qed
    ===> ok

### Existential Generalization (EG) ###

All bugs are creepy therefore there exists a bug which is creepy.

Again, the new variable name introduced into the `exists` must be unique to avoid
scope problems.

    given
        Universal_Instantiation    = forall(X, P) ; V{term}       |- P[X -> V]
        Existential_Generalization = P ; X{term} ; V{unique atom} |- exists(V, P)[X -> V]
    
        Premise                    = |- forall(x, impl(bug(x), creepy(x)))
    show
        exists(k, impl(bug(k), creepy(k)))
    proof
        Step_1 = forall(x, impl(bug(x), creepy(x)))                   by Premise
        Step_2 = impl(bug(x), creepy(x))                              by Universal_Instantiation with Step_1, x
        Step_3 = exists(k, impl(bug(k), creepy(k)))                   by Existential_Generalization with Step_2, x, k
    qed
    ===> ok

### Existential Instantiation (EI) ###

All men are mortal.  There exists a man named Socrates.  Therefore there exists a man who is mortal
and who is named Socrates.

Very unlike UI, the new variable name introduced during EI needs to be both unique to avoid
scope problems, and local, to prevent the name from "leaking out" of the EI block.

    given
        Modus_Ponens               = impl(P, Q)    ; P                   |- Q
        Conjunction                = P             ; Q                   |- and(P, Q)
        Simplification_Left        = and(P, Q)                           |- P
        Simplification_Right       = and(P, Q)                           |- Q
        Tautology                  = P                                   |- P
    
        Universal_Instantiation    = forall(X, P) ; V{term}              |- P[X -> V]
        Existential_Generalization = P ;  X{term} ; V{unique atom}       |- exists(V, P)[X -> V]
        block Existential_Instantiation
            case
                Let                = exists(X, P) ; V{unique local atom} |- P[X -> V]
                Then               = P                                   |- P
            end
        end
    
        Premise_1                 = |- forall(x, impl(man(x), mortal(x)))
        Premise_2                 = |- exists(x, and(man(x), socrates(x)))
    show
        exists(y, and(mortal(y), socrates(y)))
    proof
        Step_1 = forall(x, impl(man(x), mortal(x)))               by Premise_1
        Step_2 = exists(x, and(man(x), socrates(x)))              by Premise_2
        block Existential_Instantiation
            case
                Step_4 = and(man(k), socrates(k))                 by Let with Step_2, k
                Step_5 = man(k)                                   by Simplification_Left with Step_4
                Step_6 = impl(man(k), mortal(k))                  by Universal_Instantiation with Step_1, k
                Step_7 = mortal(k)                                by Modus_Ponens with Step_6, Step_5
                Step_8 = socrates(k)                              by Simplification_Right with Step_4
                Step_9 = and(mortal(k), socrates(k))              by Conjunction with Step_7, Step_8
                Step_10 = exists(y, and(mortal(y), socrates(y)))  by Existential_Generalization with Step_9, k, y
                Step_11 = exists(y, and(mortal(y), socrates(y)))  by Then with Step_10
            end
        end
        Step_12 = exists(y, and(mortal(y), socrates(y)))          by Tautology with Step_11
    qed
    ===> ok

For comparison, here are all of the rules for Universal (resp. Existential)
Generalization (resp. Instantiation) shown together in one place, with abbreviated names:

    UG           = P ;  X{term} ; V{unique atom}       |- forall(V, P)[X -> V]
    UI           = forall(X, P) ; V{term}              |- P[X -> V]
    EG           = P ;  X{term} ; V{unique atom}       |- exists(V, P)[X -> V]
    block EI
        case
            Let  = exists(X, P) ; V{unique local atom} |- P[X -> V]
            Then = P                                   |- P
        end
    end

Equational Reasoning
--------------------

Maxixe is not restricted to "logic" per se, by which I mean Modus Ponens and all that;
the rules of inference that are given can describe any algebra, with or without
accompanying logical connectives.  Here, we give an example of a proof of a simple
property of monoids.  It's simple enough that it does need any "logical" machinery,
only equational reasoning.

In this proof, `o(X, Y)` is the monoid operation.  `m(X)` means X is an element of the
monoid, `id(X)` means X is an identity element (meaning, *the* identity element, but we
don't assume or prove that it is unique.)  We show that `ee=e`.

    given
        Closure                   = m(A) ; m(B)          |- m(o(A, B))
        Associativity             = m(A) ; m(B) ; m(C)   |- eq(o(A, o(B, C)), o(o(A, B), C))
        Identity                  = m(A) ; id(E)         |- eq(o(A, E), A)
        Identity_is_an_Element    = id(E)                |- m(E)
        Premise                   =                      |- id(e)
    show
        eq(o(e, e), e)
    proof
        Step_1 = id(e)            by Premise
        Step_2 = m(e)             by Identity_is_an_Element with Step_1
        Step_3 = eq(o(e, e), e)   by Identity with Step_2, Step_1
    qed
    ===> ok

Number Theory
-------------

If y is odd, then y+1 is even.

The variable names used here are kind of painful, in order to avoid name clashes.
Perhaps the new variable introduced in UG and EG doesn't have to be unique?
As long as it's not the same as any atom already in P.  (This sounds familiar.)

    given
        UG           = P ;  X{term} ; V{unique atom}       |- forall(V, P)[X -> V]
        UI           = forall(X, P) ; V{term}              |- P[X -> V]
        EG           = P ;  X{term} ; V{unique atom}       |- exists(V, P)[X -> V]
        block EI
            case
                Let  = exists(X, P) ; V{unique local atom} |- P[X -> V]
                Then = P                                   |- P
            end
        end
    
        Weakening            = biimpl(X, Y)   |- impl(X, Y)
        Reverse_Weakening    = biimpl(X, Y)   |- impl(Y, X)
        Modus_Ponens         = P ; impl(P, Q) |- Q
    
        block Suppose
            case
                Supposition    = A{term}        |- A
                Conclusion     = P ; Q          |- impl(P, Q)
            end
        end
    
        Defn_of_Even = |- forall(n, biimpl(even(n), exists(m, eq(n, add(m, m)))))
        Defn_of_Odd  = |- forall(n, biimpl(odd(n), exists(k, eq(n, add(add(k, k), c(1))))))
    
        Add_One_to_Both_Sides = eq(X, Y)                         |- eq(add(X, c(1)), add(Y, c(1)))
        Provisional_Algebra   = eq(X, add(add(add(A, B), C), D)) |- eq(X, add(add(A, C), add(B, D)))
        
    show
        forall(y, impl(odd(y), even(add(y, c(1)))))
    proof
        block Suppose
            case
                Step_1 = odd(x)                                                              by Supposition with odd(x)
                Step_2 = forall(n, biimpl(odd(n), exists(k, eq(n, add(add(k, k), c(1))))))   by Defn_of_Odd
                Step_3 = biimpl(odd(x), exists(k, eq(x, add(add(k, k), c(1)))))              by UI with Step_2, x
                Step_4 = impl(odd(x), exists(k, eq(x, add(add(k, k), c(1)))))                by Weakening with Step_3
                Step_5 = exists(k, eq(x, add(add(k, k), c(1))))                              by Modus_Ponens with Step_1, Step_4
                block EI
                    case
                        Step_6 = eq(x, add(add(j, j), c(1)))                                 by Let with Step_5, j
                        Step_7 = eq(add(x, c(1)), add(add(add(j, j), c(1)), c(1)))           by Add_One_to_Both_Sides with Step_6
                        Step_8 = eq(add(x, c(1)), add(add(j, c(1)), add(j, c(1))))           by Provisional_Algebra with Step_7
                        Step_9 = exists(m, eq(add(x, c(1)), add(m, m)))                      by EG with Step_8, add(j, c(1)), m
                        
                        Step_10 = forall(n, biimpl(even(n), exists(m, eq(n, add(m, m)))))             by Defn_of_Even
                        Step_11 = biimpl(even(add(x, c(1))), exists(m, eq(add(x, c(1)), add(m, m))))  by UI with Step_10, add(x, c(1))
                        Step_12 = impl(exists(m, eq(add(x, c(1)), add(m, m))), even(add(x, c(1))))    by Reverse_Weakening with Step_11
                        Step_13 = even(add(x, c(1)))                                                  by Modus_Ponens with Step_9, Step_12
                        Step_14 = even(add(x, c(1)))                                                  by Then with Step_13
                    end
                end
                Step_15 = impl(odd(x), even(add(x, c(1))))       by Conclusion with Step_1, Step_14
            end
        end
        Step_16 = forall(y, impl(odd(y), even(add(y, c(1)))))    by UG with Step_15, x, y
    qed
    ===> ok
