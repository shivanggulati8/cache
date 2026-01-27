*** Settings ***
Library    ./code.py
Library    BuiltIn

*** Test Cases ***
Addition With User Input
    ${result}=    Add    ${a}    ${b}
    Log    Result is ${result}
    Log To Console    Result is ${result}