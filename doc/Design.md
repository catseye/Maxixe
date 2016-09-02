Maxixe: Design
==============

Design Goals
------------

Maxixe's design goals are:

*   **Simplicity**: the implementation should be simple.  Re-implementing Maxixe in a
    different host language should be a conceivable weekend project.
    
*   **Familiarity**: proofs should look more or less like "classical" proofs which
    consist of a list of steps and the justification for each step.

*   **Explicitness**: the supplied proof must be written out completely explicitly;
    the implementation must not be made to search for any information that is not
    stated.

*   **Generality**: the proof language itself should make as few assumptions about
    the object language as possible.  In particular, it shouldn't "know logic".

*   **Predicate Logic**: on the other hand, the proof language should, when given
    the rules of predicate logic, be powerful enough to allow one to check proofs
    using predicate logic.

*   **Correctness**: the proof-checking capability of the language must not
    claim that an incorrect proof is correct for the given rules.  It would also
    be nice if it does not claim that a correct proof is incorrect.

Here are some things which are *not* goals of Maxixe:

*   **Theorem proving**.  Maxixe need only check that a proof supplied to it is a valid
    proof.  It need not search for a proof given a theorem.

*   **Efficiency**.

### How well are these goals met? ###

*   **Simplicity**: as of this writing, the reference implementation of Maxixe, in Python, is
    about 600 lines of code.  About 250 lines of that is the parser and scanner.  Another 200
    is the AST and term (matching, replacing) infrastructure.

*   **Familiarity**: aside from the term language (meaning, you have to say `impl(A,B)` instead
    of `A→B`), the layout of a proof is fairly classical.  A proof consists of a set of
    rules of inference (which includes axioms and premises), the goal to be proved, and a
    list of steps.  Each step includes a phrase "by [rule] with [previous steps]" as its
    justification.  The last step must equal the goal to be proved.

*   **Explicitness**: virtually everything must be spelled out.  Maxixe will not even search
    for what previous proof steps were used in a step.

*   **Generality**: instead of coding the rules for Existential Instantiation (etc) in
    the proof language, we have coded constraints on hypotheses and conclusions which
    allow rules like EI to be written.

*   **Predicate Logic**: see the Generality point above.  It's getting there.

*   **Correctness**: see the Disclaimer in the README.  It's probably close, but I wouldn't
    put money on it.

Related Work
------------

The most proximal influence on Maxixe is certainly [The Incredible Proof Machine][], which
displays proof steps graphically as a network of nodes, and lets you hook them up to form
a valid proof.  I learned a lot from it and have had a lot of fun with it.  You should
check it out too.

But I've been interested in writing a proof checker since reading (I think) an example in
one of Emil Post's early papers on [Post canonical systems][].  I don't remember the
exact example, but this was part of the research on effective computation, and he was
showing that what a mathematician or logicial does when checking a proof is essentially
a string-rewriting process.  Symbol manipulation.  Replacing equals with equals.

My interest was further piqued by a few mentions of this in the book
Advanced Topics in Term Rewriting.

And there is a proof in ML for the Working Programmer that I've always wanted to
mechanize (forthcoming in Maxixe, hopefully.)

I looked into Agda and while the Howard-Curry Isomorphism is really cool, I have to say
it also makes it possible to conflate two concepts, computing and proving, which are
in many respects _different_.  And for whatever reason, proofs written as computations
look just terribly pained to me.  I wanted something with a more classical approach.

And Coq is probably nice for what it does, but I really don't care much right now
about _finding_ proofs, I just want to check ones I've already found.

And both of these tools are really quite heavyweight; I wanted something lighter.

A modern but somewhat older proof-checker that is based on symbol manipulation is
[MetaMath].  It fits the bill in many ways, but its syntax is quite ugly.  It has
a huge body of work rendered to web pages though, so you should check it out too.

[The Incredible Proof Machine]:     http://incredible.pm/
[Post canonical systems]:           https://en.wikipedia.org/wiki/Post_canonical_system
[MetaMath]:                         http://us.metamath.org/
