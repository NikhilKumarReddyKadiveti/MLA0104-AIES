# Automobile Fault Diagnosis Expert System

A rule-based Automobile Fault Diagnosis Expert System developed in **SWI-Prolog** for an Artificial Intelligence and Expert Systems project.

## Features

- 16 automotive diagnostic production rules
- Interactive symptom collection
- Forward chaining
- Backward chaining
- Explanation facility
- Multiple-fault diagnosis
- Negative/insufficient-evidence testing
- Procedural Python comparison

## Project Structure

```text
automobile-fault-diagnosis-expert-system/
├── knowledge_base.pl
├── auto_expert.pl
├── auto_expert_interactive.pl
├── procedural_equivalent.py
├── test_run_log.txt
└── README.md
```

## Requirements

- SWI-Prolog
- Python 3.x (only required for the paradigm-comparison file)

## Run the Batch Tests

Open a terminal in this folder:

```bash
swipl auto_expert.pl
```

The batch driver runs four scenarios:

1. Weak battery
2. Faulty starter motor
3. Multiple faults
4. Insufficient evidence for fuel pump failure

## Run the Interactive System

```bash
swipl auto_expert_interactive.pl
```

The program asks whether each known symptom is present.

Enter:

```text
y.
```

or

```text
n.
```

After the questions, the system performs forward chaining and displays diagnosed faults.

It then asks for a specific fault to verify using backward chaining.

Example:

```text
weak_battery.
```

or:

```text
none.
```

## Example

Input symptoms:

```text
slow_crank
dashboard_dim_lights
warning_light_battery
```

Forward chaining derives:

```text
weak_battery
```

Backward chaining can then verify:

```text
weak_battery
```

## Knowledge Representation

Rules use the structure:

```prolog
rule(Fault, Conditions, Advice).
```

Example:

```prolog
rule(
    weak_battery,
    [slow_crank, dashboard_dim_lights, warning_light_battery],
    'Battery is weak or discharged.'
).
```

Observed symptoms are stored as:

```prolog
symptom(SymptomName).
```

## Disclaimer

This is an educational expert-system project. Its conclusions are based only on the symptoms and rules encoded in the knowledge base and should not be treated as professional vehicle diagnosis.
