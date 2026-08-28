% ================================================================
% Interactive Automobile Fault Diagnosis Expert System
% Run: swipl auto_expert_interactive.pl
% ================================================================

:- consult('knowledge_base.pl').

:- initialization(main, main).

main(_Argv) :-
    reset_symptoms,
    format('~n===== AUTOMOBILE FAULT DIAGNOSIS EXPERT SYSTEM =====~n'),
    format('Answer y. or n. (with a full stop) for each symptom.~n~n'),
    findall(S, known_symptom(S), Symptoms),
    ask_all(Symptoms),
    forward_chain,
    ask_backward_goal,
    halt.

ask_all([]).
ask_all([S|Rest]) :-
    format('Do you observe ~w ? (y/n): ', [S]),
    read(Ans),
    ( Ans == y
    -> assertz(symptom(S))
    ;  true
    ),
    ask_all(Rest).

ask_backward_goal :-
    format('~nEnter a specific fault name to verify via backward chaining (or none.): '),
    read(Goal),
    ( Goal == none
    -> true
    ;  ( rule(Goal, _, _)
       -> backward_chain(Goal),
          why(Goal)
       ;  format('Unknown fault name.~n')
       )
    ).
