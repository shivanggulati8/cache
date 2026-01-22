*** Settings ***
Library    ./main.py    
Library    BuiltIn

*** Test Cases ***
Checking If Addition Works
    ${result}=  Add    1    2
    Should Be Equal As Integers    ${result}    3
Checking If Negative Addition Works
    ${result}=  Add    -1    -2
    Should Be Equal As Integers    ${result}    -3
