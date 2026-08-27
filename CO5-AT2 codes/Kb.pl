% ============================================================
% Crop-Disease Advisory Expert System
% Domain: Agriculture
% Course: Artificial Intelligence and Expert Systems (MLA01)
% ============================================================

:- dynamic(crop/2).
:- dynamic(soil_type/2).
:- dynamic(weather/2).
:- dynamic(symptom/2).
:- dynamic(derived_disease/2).
:- discontiguous(crop/2).
:- discontiguous(soil_type/2).
:- discontiguous(weather/2).
:- discontiguous(symptom/2).

% ---------------- Case Facts (Knowledge Acquisition) ----------------
crop(c1, tomato).      soil_type(c1, clayey).       weather(c1, humid).
symptom(c1, leaf_spots).  symptom(c1, wilting).

crop(c2, wheat).       soil_type(c2, loamy).        weather(c2, humid).
symptom(c2, yellow_leaves). symptom(c2, orange_pustules).

crop(c3, cotton).      soil_type(c3, sandy).        weather(c3, dry).
symptom(c3, pest_infestation). symptom(c3, yellow_leaves). symptom(c3, poor_growth).

crop(c4, rice).        soil_type(c4, waterlogged).  weather(c4, humid).
symptom(c4, wilting).  symptom(c4, poor_growth).

crop(c5, potato).      soil_type(c5, loamy).        weather(c5, cool_wet).
symptom(c5, leaf_spots). symptom(c5, wilting).

crop(c6, tomato).      soil_type(c6, loamy).        weather(c6, warm_dry).
symptom(c6, yellow_leaves). symptom(c6, poor_growth).

crop(c7, cotton).      soil_type(c7, clayey).       weather(c7, dry).
symptom(c7, wilting).  symptom(c7, pest_infestation).
symptom(c7, yellow_leaves). symptom(c7, poor_growth).

% ---------------- Production Rules ----------------
disease(CaseID, late_blight) :-
    crop(CaseID, C), (C == tomato ; C == potato),
    weather(CaseID, W), (W == humid ; W == cool_wet),
    symptom(CaseID, leaf_spots),
    symptom(CaseID, wilting).

disease(CaseID, leaf_rust) :-
    crop(CaseID, wheat),
    weather(CaseID, humid),
    symptom(CaseID, orange_pustules),
    symptom(CaseID, yellow_leaves).

disease(CaseID, bacterial_leaf_blight) :-
    crop(CaseID, rice),
    weather(CaseID, humid),
    symptom(CaseID, yellow_leaves),
    symptom(CaseID, leaf_spots).

disease(CaseID, root_rot) :-
    soil_type(CaseID, waterlogged),
    symptom(CaseID, wilting),
    symptom(CaseID, poor_growth).

disease(CaseID, aphid_infestation) :-
    symptom(CaseID, pest_infestation),
    symptom(CaseID, yellow_leaves),
    symptom(CaseID, poor_growth).

disease(CaseID, powdery_mildew) :-
    weather(CaseID, warm_dry),
    symptom(CaseID, poor_growth),
    symptom(CaseID, white_powder).

disease(CaseID, nitrogen_deficiency) :-
    symptom(CaseID, yellow_leaves),
    symptom(CaseID, poor_growth),
    \+ symptom(CaseID, pest_infestation),
    \+ symptom(CaseID, leaf_spots).

disease(CaseID, bacterial_wilt) :-
    crop(CaseID, cotton),
    weather(CaseID, dry),
    symptom(CaseID, wilting).

% ---------------- Treatment / Recommendation Rules ----------------
treatment(late_blight, 'Apply copper-based fungicide; remove and destroy infected leaves; avoid overhead irrigation; ensure field drainage.').
treatment(leaf_rust, 'Apply triazole-based fungicide; use rust-resistant wheat varieties; practise field sanitation and crop rotation.').
treatment(bacterial_leaf_blight, 'Use resistant rice varieties; apply copper-based bactericide; avoid excess nitrogen fertilisation.').
treatment(root_rot, 'Improve field drainage; avoid waterlogging; apply Trichoderma-based bio-fungicide to the root zone.').
treatment(aphid_infestation, 'Apply neem oil or insecticidal soap; introduce natural predators such as ladybirds; remove heavily infested leaves.').
treatment(powdery_mildew, 'Apply sulfur-based fungicide; increase plant spacing to improve air circulation; avoid excess nitrogen.').
treatment(nitrogen_deficiency, 'Apply nitrogen-rich fertiliser (urea / ammonium sulfate); conduct a soil nutrient test; consider split fertiliser doses.').
treatment(bacterial_wilt, 'Practise crop rotation with non-host crops; ensure consistent irrigation; remove and destroy infected plants.').

% ---------------- Backward-Chaining Interface ----------------
diagnose(CaseID, Disease, Treatment) :-
    disease(CaseID, Disease),
    treatment(Disease, Treatment).

% ---------------- Forward-Chaining Engine ----------------
forward_chain(CaseID) :-
    findall(D, disease(CaseID, D), Diseases),
    forall(member(D, Diseases),
           ( \+ derived_disease(CaseID, D)
           -> assertz(derived_disease(CaseID, D))
           ;  true )).

run_forward_chaining :-
    findall(C, crop(C, _), Cases0),
    sort(Cases0, Cases),
    forall(member(C, Cases), forward_chain(C)).

% ---------------- Explanation Facility ----------------
why(CaseID, Disease) :-
    disease(CaseID, Disease),
    format("~w diagnosed with ~w because:~n", [CaseID, Disease]),
    ( crop(CaseID, Crop) -> format(" - Crop: ~w~n", [Crop]) ; true ),
    ( weather(CaseID, W) -> format(" - Weather: ~w~n", [W]) ; true ),
    forall(symptom(CaseID, S), format(" - Symptom observed: ~w~n", [S])).
