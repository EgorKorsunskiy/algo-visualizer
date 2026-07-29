##Parsing strategy
    Expressions - parsed using Pratt parser, utilising binding power.
    Statements - parsed recursively, made of building blocks  

    - if: Statement -> if(<expression>){<statement[]>} 
        [y] Logic
        [] Tests
    - if else: Statement -> if else(<expression>){<statement[]>}
        [y] Logic
        [] Tests
    - else: Statement -> else{<statement[]>}
        [y] Logic
        [] Tests
    - for: Statement -> for(<expression>;<expression>;<expression>){<statement[]>}
        [y] Logic
        [] Tests
    - while: Statement -> while(<expression>){<statemet[]>}
        [y] Logic
        [] Tests
    - function declaration: Statement -> <TYPE><IDENT>(<(<TYPE><IDENT>)[]>){statement[]}
        In fact, c++ allows assigning anonimous function to a variable, but it's out of supported syntaxis subset's scope
        [] Logic
        [] Tests
    - function call: Expression
        [] Logic
        [] Tests