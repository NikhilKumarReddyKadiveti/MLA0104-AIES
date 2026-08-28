% ================================================================
% Batch Test Driver
% Run: swipl auto_expert.pl
% ================================================================

:- consult('knowledge_base.pl').

run_case(Number, Description, Symptoms, Goals) :-
    format('~n############ TEST CASE ~w: ~w ############~n',
           [Number, Description]),
    reset_symptoms,
    assert_symptoms(Symptoms),
    forward_chain,
    backward_goals(Goals).

assert_symptoms([]).
assert_symptoms([S|Rest]) :-
    assertz(symptom(S)),
    assert_symptoms(Rest).

backward_goals([]).
backward_goals([Goal|Rest]) :-
    backward_chain(Goal),
    why(Goal),
    backward_goals(Rest).

main :-
    run_case(
        1,
        'Weak Battery scenario',
        [slow_crank, dashboard_dim_lights, warning_light_battery],
        [weak_battery]
    ),

    run_case(
        2,
        'Starter Motor scenario',
        [clicking_sound, engine_wont_start],
        [faulty_starter_motor]
    ),

    run_case(
        3,
        'Multi-fault scenario (engine mounts + knock)',
        [abnormal_vibration_idle, engine_noise_knocking, warning_light_oil],
        [worn_engine_mounts, low_engine_oil]
    ),

    run_case(
        4,
        'Insufficient evidence for fuel pump',
        [squealing_brakes],
        [fuel_pump_failure]
    ),

    format('~nAll batch test cases completed.~n').

:- initialization(main, main).
