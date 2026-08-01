% Facts
man(marcus).
pompeian(marcus).
ruler(caesar).
tried_to_assassinate(marcus, caesar).

% Rules
roman(X) :-
    pompeian(X).

person(X) :-
    man(X).

% Everyone is loyal to someone
loyal(X, someone) :-
    person(X).

% A person who tried to assassinate a ruler is not loyal
not_loyal(X,Y) :-
    tried_to_assassinate(X,Y),
    ruler(Y).

% Romans who are not loyal hate Caesar
hates(X, caesar) :-
    roman(X),
    not_loyal(X, caesar).