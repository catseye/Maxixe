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
            Supposition        = A{term}        |- A
            Conclusion         = P ; Q          |- impl(P, Q)
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
            Step_4 = a                 by Supposition with a
            Step_5 = impl(b, c)        by Modus_Ponens with Step_1, Step_4
            Step_6 = b                 by Modus_Ponens with Step_2, Step_4
            Step_7 = c                 by Modus_Ponens with Step_5, Step_6
            Step_8 = impl(a, c)        by Conclusion with Step_4, Step_7
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
            end
            case
                Disj_Elim_Right = or(P, Q)       |- Q
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
            end
            case
                Step_4 = b                                by Disj_Elim_Right with Step_1
                Step_5 = or(b, a)                         by Disj_Intro_Right with Step_4, a
            end
        end
        Step_6 = or(b, a)                                 by Tautology with Step_5
    qed
    ===> ok

### Proof by Contradiction ###

If we assume p and show that it leads to a contradiction,
we can then infer ¬p.  We can use proof by contradiction
to try to derive Modus Tollens:

    given
        Modus_Ponens            = impl(P, Q) ; P |- Q
    
        Double_Negation         = not(not(P))    |- P
        Contradiction           = P ; not(P)     |- bottom
        Explosion               = bottom         |- P
    
        block Reductio_ad_Absurdum
            Supposition         = A{term}        |- A
            Conclusion          = bottom         |- not(A)
        end
    
        Premise_1               =                |- impl(p, q)
        Premise_2               =                |- not(q)
    show
        not(p)
    proof
        Step_1 = impl(p, q)                               by Premise_1
        Step_2 = not(q)                                   by Premise_2
        block Reductio_ad_Absurdum
            Step_3 = p                                    by Supposition with p
            Step_4 = q                                    by Modus_Ponens with Step_1, Step_3
            Step_5 = bottom                               by Contradiction with Step_4, Step_2
            Step_6 = not(p)                               by Conclusion with Step_5
        end
        Step_7 = not(p)                                   by Tautology with Step_6
    qed

This proof is not yet accepted by Maxixe, and the reason seems to be
a small technical one: the scope of the bound variable `A` does not
extend to the right-hand side of the Conclusion of the
`Reduction_ad_Absurdum` block.  That's unfortunate, and I don't know
at the moment how much work it would take to fix.

Predicate Logic
---------------

### Universal Generalization (UG) ###

The following is adapted from the "short, dull proof" from page 13 of John C. Reynold's
_Theories of Programming Languages_.

In the original, the rules of inference aren't named, and the 2nd one (Commutivity_of_Equality)
is an "axiom schema" which has no hypotheses.  Maxixe requires that every variable on the RHS
of a turnstile can be filled out by a variable on the LHS, so I've taken the liberty of turning
it into a rule.

The variable being introduced by Universal Generalization need not be unique, because it
is bound in a `forall`.

Note that the substitution operation `P[X -> V]` used in the Universal Generalization rule
first checks that the instance of V does not already occur in P.

(This may in fact be overly restrictive.  But it seems like the most hardship it causes at
the moment is that it requires you to select different names for variables in parts of the
proof.  For example, below we show a result `forall(y, ...)`.  We could just as easily
want to show the result `forall(x, ...)` but x is already a free (arbitrary) variable in
this proof.)

We use `c(zero)` to represent zero because we can't use `zero` because then you could use it as
a variable name and say something silly like `forall(zero, ...)`.

    given
        Premise                  =                                 |- eq(add(x, c(zero)), x)
        Commutivity_of_Equality  = eq(E1, E0)                      |- impl(eq(E1, E0), eq(E0, E1))
        Modus_Ponens             = P0 ; impl(P0, P1)               |- P1
        Universal_Generalization = P  ; X{nonlocal term} ; V{atom} |- forall(V, P[X -> V])
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

Note that the term introduced as the variable in the UI need not be unique, because if
something is true for all `x`, it is true for *all* `x`, even if `x` is something else
you've already been thinking about and given the name `x`.  Note that it also need not
be an atom.

Note that the substitution operation `P[X -> V]` used in the Universal Instantiation rule
first checks that the instance of V does not already occur in P.  This prevents situations
like instantiating ∀x.∃y.x≠y with y, to obtain ∃y.y≠y.

    given
        Modus_Ponens             = impl(P, Q)    ; P             |- Q
        Conjunction              = P             ; Q             |- and(P, Q)
        block Suppose
            Supposition          = A{term}        |- A
            Conclusion           = P ; Q          |- impl(P, Q)
        end
    
        Universal_Generalization = P ; X{nonlocal term} ; V{atom} |- forall(V, P[X -> V])
        Universal_Instantiation  = forall(X, P) ; V{term}         |- P[X -> V]
    
        Premise_1                = |- forall(x, impl(bug(x), creepy(x)))
        Premise_2                = |- forall(x, impl(bug(x), crawly(x)))
    show
        forall(x, impl(bug(x), and(creepy(x), crawly(x))))
    proof
        Step_1 = forall(x, impl(bug(x), creepy(x)))                   by Premise_1
        Step_2 = impl(bug(y), creepy(y))                              by Universal_Instantiation with Step_1, y
        Step_3 = forall(x, impl(bug(x), crawly(x)))                   by Premise_2
        Step_4 = impl(bug(y), crawly(y))                              by Universal_Instantiation with Step_3, y
        block Suppose
            Step_5 = bug(y)                                           by Supposition with bug(y)
            Step_6 = creepy(y)                                        by Modus_Ponens with Step_2, Step_5
            Step_7 = crawly(y)                                        by Modus_Ponens with Step_4, Step_5
            Step_8 = and(creepy(y), crawly(y))                        by Conjunction with Step_6, Step_7
            Step_9 = impl(bug(y), and(creepy(y), crawly(y)))          by Conclusion with Step_5, Step_8
        end
        Step_10 = forall(x, impl(bug(x), and(creepy(x), crawly(x))))  by Universal_Generalization with Step_9, y, x
    qed
    ===> ok

About that gratuitous variable name restriction in the previous example.
What if we really did want to show `forall(x, eq(x, add(x, c(zero))))`?
Can we do it with an instantiation step?

    given
        Premise                  =                                 |- eq(add(x, c(zero)), x)
        Commutivity_of_Equality  = eq(E1, E0)                      |- impl(eq(E1, E0), eq(E0, E1))
        Modus_Ponens             = P0 ; impl(P0, P1)               |- P1
        Universal_Generalization = P  ; X{nonlocal term} ; V{atom} |- forall(V, P[X -> V])
        Universal_Instantiation  = forall(X, P) ; V{term}          |- P[X -> V]
    show
        forall(x, eq(x, add(x, c(zero))))
    proof
        Step_1 = eq(add(x, c(zero)), x)                                 by Premise
        Step_2 = impl(eq(add(x, c(zero)), x), eq(x, add(x, c(zero))))   by Commutivity_of_Equality with Step_1
        Step_3 = eq(x, add(x, c(zero)))                                 by Modus_Ponens with Step_1, Step_2
        Step_4 = forall(y, eq(y, add(y, c(zero))))                      by Universal_Generalization with Step_3, x, y
        Step_5 = eq(z, add(z, c(zero)))                                 by Universal_Instantiation with Step_4, z
        Step_6 = forall(x, eq(x, add(x, c(zero))))                      by Universal_Generalization with Step_5, z, x
    qed
    ===> ok

Yes.

### Existential Generalization (EG) ###

All bugs are creepy therefore there exists a bug which is creepy.

The variable being introduced by Existential Generalization need not be unique, because it
is bound in an `exists`.

Like always with `[X -> V]`, an occurs check occurs.  Not sure if necessary atm.

    given
        Universal_Instantiation    = forall(X, P) ; V{term}       |- P[X -> V]
        Existential_Generalization = P ; X{term} ; V{atom}        |- exists(V, P[X -> V])
    
        Premise                    = |- forall(x, impl(bug(x), creepy(x)))
    show
        exists(x, impl(bug(x), creepy(x)))
    proof
        Step_1 = forall(x, impl(bug(x), creepy(x)))                   by Premise
        Step_2 = impl(bug(j), creepy(j))                              by Universal_Instantiation with Step_1, j
        Step_3 = exists(x, impl(bug(x), creepy(x)))                   by Existential_Generalization with Step_2, j, x
    qed
    ===> ok

### Existential Instantiation (EI) ###

All men are mortal.  There exists a man who is Socrates.  Therefore there exists a man who is mortal
and who is Socrates, i.e. Socrates is mortal.

Very unlike UI, to avoid scoping problems, the new variable name introduced during EI needs to be:

*   an atom, because instantiating an entire term is probably unjustifiable sometimes
*   unique, to avoid clashing with another variable that was previously instantiated
*   local, to prevent the name from "leaking out" of the EI block.

Note that the substitution operation `P[X -> V]` used in the Existential Instantiation rule
first checks that the instance of V does not already occur in P.  This prevents situations
like instantiating ∃x.∀y.p(y)→x≠y with y, to obtain ∀y.p(y)→y≠y.

    given
        Modus_Ponens               = impl(P, Q)    ; P                   |- Q
        Conjunction                = P             ; Q                   |- and(P, Q)
        Simplification_Left        = and(P, Q)                           |- P
        Simplification_Right       = and(P, Q)                           |- Q
        Tautology                  = P                                   |- P
    
        Universal_Instantiation    = forall(X, P) ; V{term}              |- P[X -> V]
        Existential_Generalization = P ;  X{term} ; V{atom}              |- exists(V, P[X -> V])
        block Existential_Instantiation
            Let                    = exists(X, P) ; V{unique local atom} |- P[X -> V]
        end
    
        Premise_1                  = |- forall(x, impl(man(x), mortal(x)))
        Premise_2                  = |- exists(x, and(man(x), socrates(x)))
    show
        exists(x, and(mortal(x), socrates(x)))
    proof
        Step_1 = forall(x, impl(man(x), mortal(x)))               by Premise_1
        Step_2 = exists(x, and(man(x), socrates(x)))              by Premise_2
        block Existential_Instantiation
            Step_3 = and(man(k), socrates(k))                     by Let with Step_2, k
            Step_4 = man(k)                                       by Simplification_Left with Step_3
            Step_5 = impl(man(k), mortal(k))                      by Universal_Instantiation with Step_1, k
            Step_6 = mortal(k)                                    by Modus_Ponens with Step_5, Step_4
            Step_7 = socrates(k)                                  by Simplification_Right with Step_3
            Step_8 = and(mortal(k), socrates(k))                  by Conjunction with Step_6, Step_7
            Step_9 = exists(x, and(mortal(x), socrates(x)))       by Existential_Generalization with Step_8, k, x
        end
        Step_10 = exists(x, and(mortal(x), socrates(x)))          by Tautology with Step_9
    qed
    ===> ok

For comparison, here are all of the rules for Universal (resp. Existential)
Generalization (resp. Instantiation) shown together in one place, with abbreviated names:

    UG           = P ;  X{nonlocal term} ; V{atom}              |- forall(V, P[X -> V])
    UI           = forall(X, P)          ; V{term}              |- P[X -> V]
    EG           = P ;  X{term}          ; V{atom}              |- exists(V, P[X -> V])
    block EI
        Let      = exists(X, P)          ; V{unique local atom} |- P[X -> V]
    end

Equational Reasoning
--------------------

Maxixe is not restricted to propositional and predicate logic.  While
some systems of logic impose their own side conditions that cannot
be expressed in Maxixe (for example, [relevance logic][] requires that
the consequent of every rule be "relevant" to its premiss) and thus
cannot be checked, other systems of logic (or fragments thereof) can
be expressed in it.  Maxixe tries to be very general in this way, and
to not impose unnecessary restrictions.

One such logic is [equational logic][], which is the logic that
underpins universal algebra.  The basic idea is "replacing equals
with equals", and often it is convenient to work with it without
even regarding it as a logic per se — often this process is referred
to only as "equational reasoning".  (A bit of trivia: there was an
early educational version of the programming language Haskell called
"Gofer", which is an acronym for "Good for equational reasoning".)

Here, we give an example of a proof of a simple property of monoids
using equational reasoning.

In this proof, `o(X, Y)` is the monoid operation.  `m(X)` means X
is an element of the monoid, `id(X)` means X is an identity element
(meaning, *the* identity element, but we don't assume or prove that it
is unique.)  We show that, if `e` is an identity element, then `ee=e`.

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

[relevance logic]: http://en.wikipedia.org/wiki/Relevance_logic
[equational logic]: http://en.wikipedia.org/wiki/Equational_logic

Number Theory
-------------

If y is odd, then y+1 is even.

    given
        UG           = P ; X{nonlocal term} ; V{atom}              |- forall(V, P[X -> V])
        UI           = forall(X, P)         ; V{term}              |- P[X -> V]
        EG           = P ; X{term}          ; V{atom}              |- exists(V, P[X -> V])
        block EI
            Let      = exists(X, P)         ; V{unique local atom} |- P[X -> V]
        end
    
        Weakening            = biimpl(X, Y)   |- impl(X, Y)
        Reverse_Weakening    = biimpl(X, Y)   |- impl(Y, X)
        Modus_Ponens         = P ; impl(P, Q) |- Q
    
        block Suppose
            Supposition      = A{term}        |- A
            Conclusion       = P ; Q          |- impl(P, Q)
        end
    
        Defn_of_Even = |- forall(n, biimpl(even(n), exists(k, eq(n, add(k, k)))))
        Defn_of_Odd  = |- forall(n, biimpl(odd(n), exists(k, eq(n, add(add(k, k), c(1))))))
    
        Add_One_to_Both_Sides = eq(X, Y)                         |- eq(add(X, c(1)), add(Y, c(1)))
        Provisional_Algebra   = eq(X, add(add(add(A, B), C), D)) |- eq(X, add(add(A, C), add(B, D)))
        
    show
        forall(y, impl(odd(y), even(add(y, c(1)))))
    proof
        block Suppose
            Step_1 = odd(x)                                                              by Supposition with odd(x)
            Step_2 = forall(n, biimpl(odd(n), exists(k, eq(n, add(add(k, k), c(1))))))   by Defn_of_Odd
            Step_3 = biimpl(odd(x), exists(k, eq(x, add(add(k, k), c(1)))))              by UI with Step_2, x
            Step_4 = impl(odd(x), exists(k, eq(x, add(add(k, k), c(1)))))                by Weakening with Step_3
            Step_5 = exists(k, eq(x, add(add(k, k), c(1))))                              by Modus_Ponens with Step_1, Step_4
            block EI
                Step_6 = eq(x, add(add(j, j), c(1)))                                     by Let with Step_5, j
                Step_7 = eq(add(x, c(1)), add(add(add(j, j), c(1)), c(1)))               by Add_One_to_Both_Sides with Step_6
                Step_8 = eq(add(x, c(1)), add(add(j, c(1)), add(j, c(1))))               by Provisional_Algebra with Step_7
                Step_9 = exists(k, eq(add(x, c(1)), add(k, k)))                          by EG with Step_8, add(j, c(1)), k
                
                Step_10 = forall(n, biimpl(even(n), exists(k, eq(n, add(k, k)))))             by Defn_of_Even
                Step_11 = biimpl(even(add(x, c(1))), exists(k, eq(add(x, c(1)), add(k, k))))  by UI with Step_10, add(x, c(1))
                Step_12 = impl(exists(k, eq(add(x, c(1)), add(k, k))), even(add(x, c(1))))    by Reverse_Weakening with Step_11
                Step_13 = even(add(x, c(1)))                                                  by Modus_Ponens with Step_9, Step_12
            end
            Step_14 = impl(odd(x), even(add(x, c(1))))                   by Conclusion with Step_1, Step_13
        end
        Step_15 = forall(y, impl(odd(y), even(add(y, c(1)))))            by UG with Step_14, x, y
    qed
    ===> ok

The sum of an odd number and an odd number is an even number.

    given
        UG           = P ; X{nonlocal term} ; V{atom}              |- forall(V, P[X -> V])
        UI           = forall(X, P)         ; V{term}              |- P[X -> V]
        EG           = P ; X{term}          ; V{atom}              |- exists(V, P[X -> V])
        block EI
            Let      = exists(X, P)         ; V{unique local atom} |- P[X -> V]
        end
    
        Weakening            = biimpl(X, Y)   |- impl(X, Y)
        Reverse_Weakening    = biimpl(X, Y)   |- impl(Y, X)
        Modus_Ponens         = P ; impl(P, Q) |- Q
        Simplification_Left  = and(P, Q)      |- P
        Simplification_Right = and(P, Q)      |- Q
        Tautology            = P              |- P
    
        block Suppose
            Supposition      = A{term}        |- A
            Conclusion       = P ; Q          |- impl(P, Q)
        end
    
        Defn_of_Even = |- forall(n, biimpl(even(n), exists(k, eq(n, add(k, k)))))
        Defn_of_Odd  = |- forall(n, biimpl(odd(n), exists(k, eq(n, add(add(k, k), c(1))))))
    
        Addition_Both_Sides = eq(X0, Y0) ; eq(X1, Y1)            |- eq(add(X0, X1), add(Y0, Y1))
        Provisional_Algebra = eq(X, add(add(add(A, B), C), add(add(D, E), F))) |- eq(X, add(add(add(A, E), C), add(add(B, E), F)))
        
    show
        forall(x, forall(y, impl(and(odd(x), odd(y)), even(add(x, y)))))
    proof
        block Suppose
            Step_1 = and(odd(x0), odd(y0))                                               by Supposition with and(odd(x0), odd(y0))
            Step_2 = odd(x0)                                                             by Simplification_Left with Step_1
            Step_3 = odd(y0)                                                             by Simplification_Right with Step_1
            Step_4 = forall(n, biimpl(odd(n), exists(k, eq(n, add(add(k, k), c(1))))))   by Defn_of_Odd
            Step_5 = biimpl(odd(x0), exists(k, eq(x0, add(add(k, k), c(1)))))            by UI with Step_4, x0
            Step_6 = impl(odd(x0), exists(k, eq(x0, add(add(k, k), c(1)))))              by Weakening with Step_5
            Step_7 = exists(k, eq(x0, add(add(k, k), c(1))))                             by Modus_Ponens with Step_2, Step_6
            Step_8 = biimpl(odd(y0), exists(k, eq(y0, add(add(k, k), c(1)))))            by UI with Step_4, y0
            Step_9 = impl(odd(y0), exists(k, eq(y0, add(add(k, k), c(1)))))              by Weakening with Step_8
            Step_10 = exists(k, eq(y0, add(add(k, k), c(1))))                            by Modus_Ponens with Step_3, Step_9
            block EI
                Step_11 = eq(x0, add(add(k0, k0), c(1)))                                 by Let with Step_7, k0
                block EI
                    Step_12 = eq(y0, add(add(k1, k1), c(1)))                             by Let with Step_10, k1
                    Step_13 = eq(add(x0, y0), add(add(add(k0, k0), c(1)), add(add(k1, k1), c(1))))
                                                                                         by Addition_Both_Sides with Step_11, Step_12
                    Step_14 = eq(add(x0, y0), add(add(add(k0, k1), c(1)), add(add(k0, k1), c(1))))
                                                                                         by Provisional_Algebra with Step_13
                    Step_15 = exists(k, eq(add(x0, y0), add(k, k)))                      by EG with Step_14, add(add(k0, k1), c(1)), k
                end
                Step_16 = forall(n, biimpl(even(n), exists(k, eq(n, add(k, k)))))           by Defn_of_Even
                Step_17 = biimpl(even(add(x0, y0)), exists(k, eq(add(x0, y0), add(k, k))))  by UI with Step_16, add(x0, y0)
                Step_18 = impl(exists(k, eq(add(x0, y0), add(k, k))), even(add(x0, y0)))    by Reverse_Weakening with Step_17
                Step_19 = even(add(x0, y0))                                                 by Modus_Ponens with Step_15, Step_18
            end
            Step_20 = impl(and(odd(x0), odd(y0)), even(add(x0, y0)))                     by Conclusion with Step_1, Step_19
        end
        Step_21 = forall(y, impl(and(odd(x0), odd(y)), even(add(x0, y))))                by UG with Step_20, y0, y
        Step_22 = forall(x, forall(y, impl(and(odd(x), odd(y)), even(add(x, y)))))       by UG with Step_21, x0, x
    qed
    ===> ok
