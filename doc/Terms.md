### Operations on Terms ###

`is_atom(t)`

True iff t is an atom (is not a variable and has no subterms), false otherwise.

`is_ground(t)`

True iff t contains no variables, false otherwise.

`replace(t, old, new)`

Returns a new term which is like t except every subterm of t which equals old has been replaced with new.

`match(pattern, t, unifier)`

Attempts to match t to the given pattern.  Where there is a variable in the pattern, that part of t is
assigned to the variable in the unifier, unless it is already bound to something different in the unifier.

`subst(t, unifier)`

Returns a new term which is like t except all the variables in t have been replaced with the terms those
variables are associated with in the unifier.

`resolve_substs(t, unifier)`

Returns a new term which is like t but contains no embedded Substitutors; instead, each of those
Substitutors is applied to the term it contains, with the given unifier, and that result replaces
the Substitutor.

`collect_atoms(t, set)`

Adds all atoms in t to the given set.
