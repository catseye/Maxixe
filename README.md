Maxixe
======

Version 0.2 | _Entry_ [@ catseye.tc](https://catseye.tc/node/Maxixe)
| _See also:_ [Madison](https://catseye.tc/node/Madison)
∘ [LCF-Style-ND](https://github.com/cpressey/LCF-Style-ND#readme)

- - - -

Maxixe is a simple proof-checking language.  Given a proof written out fully and
explicitly (including all rules of inference), a computer can check if it is valid
or not.

Here is an example of a valid proof in propositional logic written in Maxixe:

    given
        Modus_Ponens                 = impl(P, Q) ; P |- Q
        Simplification               = and(P, Q)      |- Q
        Commutativity_of_Conjunction = and(P, Q)      |- and(Q, P)
        Premise                      =                |- and(p, impl(p, q))
    show
        q
    proof
        Step_1 = and(p, impl(p, q))    by Premise
        Step_2 = and(impl(p, q), p)    by Commutativity_of_Conjunction with Step_1
        Step_3 = impl(p, q)            by Simplification with Step_1
        Step_4 = p                     by Simplification with Step_2
        Step_5 = q                     by Modus_Ponens with Step_3, Step_4
    qed

For Maxixe's design goals, related work, and discussion, see
[doc/Design.md](doc/Design.md).

For a description of the language, see [doc/Maxixe.md](doc/Maxixe.md).

For examples of proofs witten in Maxixe, see [doc/Examples.md](doc/Examples.md).

The reference implementation of Maxixe, called `maxixe`, is written in Python,
and runs under (at least) Python 2.7.18 and Python 3.8.10.  To use `maxixe`,
simply add the `bin` directory of this repository to your executable search path
and run it on a text file containing your proof, like

    maxixe my_proof.maxixe

It will output `ok` if the proof is valid.  Otherwise it will display a (currently
rather poor) error message.

### Disclaimer ###

I am not prepared to claim that, given an invalid proof, Maxixe will never
mistakenly tell you that it is valid.

However, if you find such a proof, please do open a bug report about it.

Note that since Maxixe requires that you supply all the axioms and rules of
inference used in a proof, it is entirely possible to give it an inconsistent
system of logic in which anything can be proved — but that's not quite the
same thing as what I'm talking about.  Such a proof is still "valid", relative
to the definitions that it is using, even if those definitions are flawed.

But on that note, I am also not prepared to claim that all of the rules of
inference I've used in the example proofs Maxixe are consistent (or otherwise
fit for writing proofs in), either.

So, if you find a flaw in one of the example proofs, please do open a bug
report about that as well.
