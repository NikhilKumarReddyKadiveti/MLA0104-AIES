"""
Procedural / imperative equivalent of the Automobile Fault Diagnosis logic.

This file is included only for the paradigm-analysis section of the report.
The main expert system is implemented in Prolog.
"""

def diagnose(symptoms: set) -> list:
    faults = []

    # Rule 1
    if {"slow_crank", "dashboard_dim_lights", "warning_light_battery"} <= symptoms:
        faults.append(
            ("weak_battery", "Battery is weak or discharged.")
        )

    # Rule 2
    if {"clicking_sound", "engine_wont_start"} <= symptoms:
        faults.append(
            ("faulty_starter_motor", "Starter motor is faulty.")
        )

    # Rule 3
    if {"engine_wont_start", "rough_idle", "reduced_mileage"} <= symptoms:
        faults.append(
            ("faulty_spark_plug", "Spark plugs are worn or fouled.")
        )

    return faults


def backward_check(goal_conditions: set, symptoms: set) -> bool:
    """Procedural backward-style check using an explicit loop."""
    for condition in goal_conditions:
        if condition not in symptoms:
            return False
    return True


if __name__ == "__main__":
    observed = {
        "slow_crank",
        "dashboard_dim_lights",
        "warning_light_battery",
    }

    print("Forward/procedural result:")
    print(diagnose(observed))

    print("\nBackward/procedural result:")
    print(backward_check(
        {
            "slow_crank",
            "dashboard_dim_lights",
            "warning_light_battery",
        },
        observed,
    ))
