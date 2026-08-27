:- [kb].

:- forall(member(C, [c1,c2,c3,c4,c5,c6,c7]),
     ( format("~n=== Case ~w ===~n", [C]),
       ( findall(D, disease(C,D), Ds) -> format("Diagnoses: ~w~n", [Ds]) ; format("Diagnoses: none~n") )
     )).

:- format("~n--- diagnose/3 backward chaining test ---~n").
:- forall(diagnose(c1, D, T), format("c1 -> ~w | ~w~n", [D,T])).
:- forall(diagnose(c2, D, T), format("c2 -> ~w | ~w~n", [D,T])).
:- forall(diagnose(c4, D, T), format("c4 -> ~w | ~w~n", [D,T])).
:- forall(diagnose(c5, D, T), format("c5 -> ~w | ~w~n", [D,T])).
:- forall(diagnose(c6, D, T), format("c6 -> ~w | ~w~n", [D,T])).

:- format("~n--- forward chaining ---~n").
:- run_forward_chaining.
:- forall(derived_disease(C,D), format("derived: ~w -> ~w~n", [C,D])).

:- format("~n--- why/1 explanation for c1 ---~n").
:- why(c1, late_blight).

:- format("~n--- backtracking demo case c7 (multiple diagnoses) ---~n").
:- findall(D, disease(c7,D), L7), format("c7 diagnoses: ~w~n", [L7]).

:- halt.
