% ================================================================
% Automobile Fault Diagnosis Expert System - Knowledge Base
% ================================================================

:- dynamic symptom/1.
:- dynamic known_fault/1.

% -------------------- Known Symptoms --------------------

known_symptom(engine_wont_start).
known_symptom(clicking_sound).
known_symptom(slow_crank).
known_symptom(engine_noise_knocking).
known_symptom(engine_noise_ticking).
known_symptom(rough_idle).
known_symptom(stalling).
known_symptom(abnormal_vibration_idle).
known_symptom(abnormal_vibration_driving).
known_symptom(reduced_mileage).
known_symptom(black_smoke_exhaust).
known_symptom(dashboard_dim_lights).
known_symptom(squealing_brakes).
known_symptom(overheating).
known_symptom(fuel_smell).
known_symptom(warning_light_battery).
known_symptom(warning_light_engine).
known_symptom(warning_light_oil).

% -------------------- Production Rules --------------------

rule(weak_battery,
     [slow_crank, dashboard_dim_lights, warning_light_battery],
     'Battery is weak or discharged. Charge or replace the battery.').

rule(faulty_starter_motor,
     [clicking_sound, engine_wont_start],
     'Starter motor is faulty. Inspect or replace the starter motor.').

rule(faulty_spark_plug,
     [engine_wont_start, rough_idle, reduced_mileage],
     'Spark plugs are worn or fouled. Inspect or replace spark plugs.').

rule(clogged_air_filter,
     [rough_idle, black_smoke_exhaust, reduced_mileage],
     'Air filter may be clogged. Inspect and replace the air filter.').

rule(faulty_alternator,
     [dashboard_dim_lights, warning_light_battery, stalling],
     'Alternator may be faulty. Inspect the charging system and alternator.').

rule(worn_timing_belt,
     [engine_noise_ticking, engine_wont_start],
     'Timing belt may be worn or broken. Inspect the timing system immediately.').

rule(faulty_ignition_coil,
     [engine_noise_knocking, rough_idle, stalling],
     'Ignition coil may be faulty. Inspect the ignition system and coil.').

rule(low_engine_oil,
     [warning_light_oil, engine_noise_knocking],
     'Engine oil level is low. Top up or change engine oil immediately.').

rule(exhaust_leak,
     [engine_noise_knocking, reduced_mileage, fuel_smell],
     'An exhaust leak may be present. Inspect the exhaust system.').

rule(worn_engine_mounts,
     [abnormal_vibration_idle, engine_noise_knocking],
     'Engine mounts are worn. Inspect and replace engine mounts.').

rule(wheel_misalignment,
     [abnormal_vibration_driving],
     'Wheels may be misaligned. Check and perform wheel alignment.').

rule(low_tire_pressure,
     [abnormal_vibration_driving, reduced_mileage],
     'Tire pressure may be low. Check and correct tire pressure.').

rule(faulty_oxygen_sensor,
     [black_smoke_exhaust, reduced_mileage, warning_light_engine],
     'Oxygen sensor may be faulty. Inspect the sensor and engine control system.').

rule(radiator_overheating_issue,
     [overheating, warning_light_engine],
     'Cooling-system fault may be present. Inspect coolant, radiator and thermostat.').

rule(worn_brake_pads,
     [squealing_brakes],
     'Brake pads are worn. Inspect and replace brake pads.').

rule(fuel_pump_failure,
     [engine_wont_start, stalling, fuel_smell],
     'Fuel pump may be failing. Inspect fuel pressure and the fuel pump.').

% -------------------- Working-Memory Utilities --------------------

reset_symptoms :-
    retractall(symptom(_)),
    retractall(known_fault(_)).

all_symptoms_present([]).
all_symptoms_present([S|Rest]) :-
    symptom(S),
    all_symptoms_present(Rest).

% -------------------- Forward Chaining --------------------

forward_chain :-
    format('~n=== FORWARD CHAINING ===~n'),
    forward_loop,
    format('~nForward chaining complete.~n'),
    print_faults.

forward_loop :-
    rule(Fault, Conditions, _Advice),
    \+ known_fault(Fault),
    all_symptoms_present(Conditions),
    !,
    assertz(known_fault(Fault)),
    format('Rule fired -> ~w (conditions: ~w)~n', [Fault, Conditions]),
    forward_loop.
forward_loop.

print_faults :-
    findall(Fault-Advice,
            (known_fault(Fault), rule(Fault, _, Advice)),
            Results),
    ( Results == []
    -> format('No fault could be diagnosed from the observed symptoms.~n')
    ;  format('Diagnosed fault(s):~n'),
       print_fault_list(Results)
    ).

print_fault_list([]).
print_fault_list([Fault-Advice|Rest]) :-
    format(' - ~w : ~w~n', [Fault, Advice]),
    print_fault_list(Rest).

% -------------------- Backward Chaining --------------------

backward_chain(Goal) :-
    format('~n=== BACKWARD CHAINING: testing goal ~w ===~n', [Goal]),
    ( prove(Goal)
    -> format('GOAL PROVED: ~w~n', [Goal]),
       rule(Goal, _, Advice),
       format('Advice: ~w~n', [Advice])
    ;  format('GOAL FAILED: insufficient evidence for ~w~n', [Goal])
    ).

prove(Goal) :-
    rule(Goal, Conditions, _Advice),
    format('Trying rule for ~w, needs: ~w~n', [Goal, Conditions]),
    prove_all(Conditions).

prove_all([]).
prove_all([S|Rest]) :-
    ( symptom(S)
    -> format('  [OK] ~w is present~n', [S]),
       prove_all(Rest)
    ;  format('  [MISSING] ~w not observed~n', [S]),
       fail
    ).

why(Goal) :-
    ( rule(Goal, Conditions, Advice)
    -> format('~n=== EXPLANATION ===~n'),
       format('Fault: ~w~n', [Goal]),
       format('Required symptoms: ~w~n', [Conditions]),
       format('Reason: all required symptoms support this rule.~n'),
       format('Recommended action: ~w~n', [Advice])
    ;  format('No rule exists for ~w.~n', [Goal])
    ).
