*** Settings ***
Library    ./code.py
Library    ./math_util.py

*** Test Cases ***
Test Adding One And Two
    ${result}=    add_one_and_two
    Should Be Equal As Integers    ${result}    3
