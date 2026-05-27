# Robot Framework Guide - Beginner to Pro

## Table of Contents

1. [Introduction](#1-introduction)
2. [Robot Framework Fundamentals](#2-robot-framework-fundamentals)
   - 2.1 [What is Robot Framework?](#21-what-is-robot-framework)
   - 2.2 [File Structure and Extensions](#22-file-structure-and-extensions)
   - 2.3 [Syntax Basics](#23-syntax-basics)
3. [The Four Main Sections](#3-the-four-main-sections)
   - 3.1 [Settings Section](#31-settings-section)
   - 3.2 [Variables Section](#32-variables-section)
   - 3.3 [Test Cases Section](#33-test-cases-section)
   - 3.4 [Keywords Section](#34-keywords-section)
4. [Library Management](#4-library-management)
5. [Resource Files](#5-resource-files)
6. [Variables Deep Dive](#6-variables-deep-dive)
7. [Control Structures](#7-control-structures)
8. [Advanced Keyword Concepts](#8-advanced-keyword-concepts)
9. [Test Setup and Teardown](#9-test-setup-and-teardown)
10. [Tags and Test Organization](#10-tags-and-test-organization)
11. [Data Structures](#11-data-structures)
12. [Logging and Debugging](#12-logging-and-debugging)
13. [Best Practices](#13-best-practices)
14. [Enterprise Project Structure](#14-enterprise-project-structure)
15. [Common Mistakes and Solutions](#15-common-mistakes-and-solutions)
16. [Tips and Tricks](#16-tips-and-tricks)

---

## 1. Introduction

Robot Framework is a generic open-source automation framework for acceptance testing, acceptance test-driven development (ATDD), and robotic process automation (RPA). It uses a keyword-driven testing approach that makes tests easy to create and maintain.

### Key Features:
- **Keyword-driven**: Tests use high-level keywords making them readable
- **Tabular syntax**: Easy to read and write
- **Extensible**: Python and Java libraries can be created
- **Platform-independent**: Works on Windows, macOS, Linux
- **Rich ecosystem**: Extensive library support

---

## 2. Robot Framework Fundamentals

### 2.1 What is Robot Framework?

Robot Framework uses a **keyword-driven** approach where:
- Test cases are built using keywords
- Keywords can be built-in, from libraries, or user-defined
- Tests are organized in test suites (files and directories)
- Results are generated in HTML/XML format

### 2.2 File Structure and Extensions

**File Extensions:**
- `.robot` - Standard Robot Framework files (recommended)
- `.txt` - Also supported but `.robot` is preferred
- `.resource` - Resource files (Robot Framework 6.0+)

**Basic File Structure:**
```robot
*** Settings ***
# Configuration, imports, setup/teardown

*** Variables ***
# Test data and variables

*** Test Cases ***
# Actual test cases

*** Keywords ***
# User-defined keywords
```

### 2.3 Syntax Basics

#### Spacing and Separation

**CRITICAL RULES:**
1. **Two or more spaces** separate columns (or tabs)
2. **Four spaces** for continuation lines
3. **Leading pipe + space** for pipe-separated format

```robot
# Space-separated format (most common)
Keyword Name    argument1    argument2    argument3

# Pipe-separated format
| Keyword Name | argument1 | argument2 | argument3 |

# Continuation with four spaces (...)
Long Keyword Name
...    argument1
...    argument2
...    argument3
```

#### Comments

```robot
# Single line comment

*** Test Cases ***
Test Example
    Keyword Call    # Inline comment after keyword
    # Full line comment
```

#### Common Syntax Mistakes from the Code

From the provided code, here's a critical mistake:

```robot
# WRONG - This creates an error
...    postAction:log.info('postAction script')  # Colon instead of =

# CORRECT
...    postAction=log.info('postAction script')
```

**In Robot Framework dictionaries, always use `=` for key-value pairs, not `:` (that's Python syntax).**

---

## 3. The Four Main Sections

### 3.1 Settings Section

The Settings section configures test suite behavior, imports, and metadata.

#### 3.1.1 Documentation

```robot
*** Settings ***
Documentation    This is suite-level documentation
...             Can span multiple lines using ...
...             Provides context about the test suite
```

**From the code:**
```robot
Documentation   Suite for SDW Custom Action Test Cases
```

#### 3.1.2 Library Imports

**Basic Syntax:**
```robot
Library    LibraryName
Library    LibraryName    arg1    arg2
Library    LibraryName    WITH NAME    alias
```

**Examples from the code:**
```robot
# Simple import
Library  Collections
Library  DateTime

# Import with arguments
Library  Library/CHAI/Features/KShareMigration/KShareFunctionality.py  
...      ${domainnameArg}  
...      ${AccessClients}  
...      WITH NAME  kf

# Import with alias
Library  Library/CHAI/Features/DeepAnalytics/WorkFlow.py    WITH NAME    wf
```

**Why Use WITH NAME?**
```robot
# Without alias - would conflict if two libraries have same keyword
Library    MyLibrary

# With alias - clear namespace
Library    MyLibrary    WITH NAME    ml
ml.Keyword Name    # Explicit library call
```

#### 3.1.3 Resource Imports

```robot
Resource    path/to/resource.robot
Resource    ../relative/path.robot
Resource    ${VARIABLE}/dynamic/path.robot
```

**From the code:**
```robot
Resource  Library/CHAI/Environment/Setup.robot
Resource  All_Keywords.robot
```

#### 3.1.4 Suite Setup and Teardown

```robot
*** Settings ***
Suite Setup       Keyword Run Before All Tests
Suite Teardown    Keyword Run After All Tests
Test Setup        Keyword Run Before Each Test
Test Teardown     Keyword Run After Each Test
```

**From the code:**
```robot
Suite Setup  init sdw suite
```

**Key Difference:**
- **Suite Setup/Teardown**: Runs ONCE per test suite (file)
- **Test Setup/Teardown**: Runs before/after EACH test case

#### 3.1.5 Other Settings

```robot
*** Settings ***
Force Tags         tag1    tag2              # All tests get these tags
Default Tags       default_tag                # Tests get these unless overridden
Test Timeout       5 minutes                  # Default timeout for all tests
Metadata           Version    1.0             # Suite metadata
```

### 3.2 Variables Section

```robot
*** Variables ***
${SCALAR}          value
@{LIST}            item1    item2    item3
&{DICT}            key1=value1    key2=value2
${NUMBER}          ${42}
${BOOLEAN}         ${True}
```

**Examples:**
```robot
*** Variables ***
${BASE_URL}        https://example.com
${TIMEOUT}         30s
@{USERS}           admin    user1    user2
&{CREDENTIALS}     username=admin    password=secret123
```

**Usage in Tests:**
```robot
*** Test Cases ***
Login Test
    Open Browser    ${BASE_URL}    chrome
    Input Text      username_field    ${CREDENTIALS}[username]
    Input Text      password_field    ${CREDENTIALS}[password]
```

### 3.3 Test Cases Section

#### Basic Structure

```robot
*** Test Cases ***
Test Case Name
    [Documentation]    Description of what this test does
    [Tags]            tag1    tag2
    [Setup]           Setup Keyword
    [Teardown]        Teardown Keyword
    Keyword 1
    Keyword 2    argument1    argument2
    ${result}=    Keyword That Returns Value
    Log    ${result}
```

#### Example from Code

```robot
Get Workflow Endpoint by WorkflowServiceID
    [Documentation]    Test GET /workflowService/{workflowServiceId} endpoint
    [Tags]    custom_action    KOMTEST-TC-22660
    
    ${accountA}=    Create Dictionary
    ...    userName=Shivang
    
    ${parameters}=    Create Dictionary
    ...    numPages=${40}
    ...    accountA=${accountA}
    
    ${workflow_payload}=    Create Dictionary
    ...    displayName=Shivang_Get_Test
    ...    workflowServiceClass=CUSTOM_ACTION
    ...    scriptName=set_metadata
    ...    parameters=${parameters}
    
    ${created_service}=    Create Workflow Service    ${workflow_payload}
    ${json_response}=    Get Workflow Service    ${created_service.id}
    
    Log    The Workflow Service JSON is: ${json_response}
    Log To Console    \nFetched JSON: ${json_response}
```

### 3.4 Keywords Section

User-defined keywords are the building blocks of reusable test logic.

#### Basic Structure

```robot
*** Keywords ***
Keyword Name
    [Documentation]    What this keyword does
    [Arguments]    ${arg1}    ${arg2}=${default}
    [Tags]         keyword_tag
    Keyword Call    ${arg1}
    ${result}=    Another Keyword    ${arg2}
    [Return]    ${result}
```

#### Example from Code

```robot
*** Keywords ***
Create Workflow Service
    [Arguments]    ${payload}
    ${workflow_service}=    Call Method     ${wf_factory}    create_workflow_service    ${payload}
    [Return]    ${workflow_service}

Get Workflow Service
    [Arguments]    ${wfsID}
    ${response}=    Call Method    ${wf_service}    get_workflow_service    ${wfsID}
    [Return]    ${response}
```

---

## 4. Library Management

### 4.1 Standard Libraries

Robot Framework comes with several built-in libraries:

```robot
*** Settings ***
Library    BuiltIn          # Automatically imported, always available
Library    Collections      # List and dictionary operations
Library    DateTime         # Date and time operations
Library    OperatingSystem  # File and directory operations
Library    Process          # Running processes
Library    String           # String manipulation
Library    XML              # XML processing
```

### 4.2 External Libraries

Popular external libraries:

```robot
Library    SeleniumLibrary              # Web testing
Library    RequestsLibrary             # REST API testing
Library    DatabaseLibrary             # Database testing
Library    SSHLibrary                  # SSH operations
Library    JSONLibrary                 # JSON operations
```

### 4.3 Custom Python Libraries

**Creating a Python Library:**

```python
# MyLibrary.py
class MyLibrary:
    def __init__(self, server_url, port=8080):
        """Library initialization with arguments"""
        self.server_url = server_url
        self.port = port
    
    def connect_to_server(self):
        """Connect to the server"""
        # Implementation
        return f"Connected to {self.server_url}:{self.port}"
    
    def get_user_data(self, user_id):
        """Get data for specific user
        
        Args:
            user_id: The ID of the user
            
        Returns:
            User data dictionary
        """
        # Implementation
        return {"id": user_id, "name": "John"}
```

**Using in Robot:**

```robot
*** Settings ***
Library    MyLibrary    https://api.example.com    port=9000    WITH NAME    api

*** Test Cases ***
Test API
    ${result}=    api.Connect To Server
    ${user}=      api.Get User Data    user_id=123
    Log    ${user}[name]
```

### 4.4 Library Instance Management

**From the code - this is a critical pattern:**

```robot
*** Keywords ***
init sdw suite
    create director and get site
    ${wf_factory} =   Get Library Instance   wf_factory
    Set Suite Variable    ${wf_factory}
    ${wf} =   Get Library Instance   wf
    Set Suite Variable  ${wf}
    ${wf_service} =   Get Library Instance   wf_service
    Set Suite Variable  ${wf_service}
```

**Why Get Library Instance?**

When you import a library with `WITH NAME`, you create an alias. But to call methods on the library object itself (not just its keywords), you need to get the instance:

```robot
# Import with alias
Library    MyLib    WITH NAME    ml

# Get the actual Python object
${lib_instance}=    Get Library Instance    ml

# Now you can call Python methods directly
${result}=    Call Method    ${lib_instance}    some_python_method    arg1
```

**Critical Mistake from the Code:**

The original error occurred because `${wf_service}` wasn't being set. The log showed those lines were missing from execution, likely due to:
1. File not saved properly
2. Wrong file being executed by Jenkins
3. Version control not updated

**Solution Pattern:**
```robot
# ALWAYS verify library instances are set
${lib}=    Get Library Instance    library_alias
Should Not Be Equal    ${lib}    ${None}    Library instance not found
Set Suite Variable    ${lib}
```

---

## 5. Resource Files

Resource files contain reusable keywords, variables, and settings (but no test cases).

### 5.1 Creating Resource Files

**common_keywords.robot:**
```robot
*** Settings ***
Library    SeleniumLibrary
Library    Collections

*** Variables ***
${LOGIN_URL}    https://example.com/login

*** Keywords ***
Login As User
    [Arguments]    ${username}    ${password}
    Open Browser    ${LOGIN_URL}    chrome
    Input Text      id=username    ${username}
    Input Text      id=password    ${password}
    Click Button    id=login_btn

Verify User Logged In
    [Arguments]    ${expected_user}
    ${actual}=    Get Text    id=username_display
    Should Be Equal    ${actual}    ${expected_user}
```

### 5.2 Using Resource Files

```robot
*** Settings ***
Resource    common_keywords.robot
Resource    ../resources/api_keywords.robot

*** Test Cases ***
User Login Test
    Login As User    admin    secret123
    Verify User Logged In    admin
```

### 5.3 Best Practices for Resource Files

1. **Organize by functionality:**
   ```
   resources/
   ├── ui_keywords.robot
   ├── api_keywords.robot
   ├── database_keywords.robot
   └── common_variables.robot
   ```

2. **Keep resources focused:**
   - Don't create mega resource files
   - Group related keywords together
   - Separate UI, API, and data operations

3. **Use relative paths:**
   ```robot
   Resource    ../resources/common.robot
   Resource    ${EXECDIR}/resources/common.robot
   ```

---

## 6. Variables Deep Dive

### 6.1 Variable Types

#### Scalar Variables (${})

```robot
${NAME}          John Doe
${AGE}           ${30}
${IS_ACTIVE}     ${True}
${PRICE}         ${19.99}
```

#### List Variables (@{})

```robot
@{COLORS}        red    green    blue
@{NUMBERS}       ${1}    ${2}    ${3}

# Accessing list items
${first}=        Get From List    ${COLORS}    0
${second}=       Set Variable    ${COLORS}[1]
```

#### Dictionary Variables (&{})

```robot
&{USER}          name=John    age=30    active=${True}

# Accessing dictionary values
${name}=         Set Variable    ${USER}[name]
${age}=          Get From Dictionary    ${USER}    age
```

### 6.2 Variable Scopes

#### Global Variables
```robot
*** Settings ***
Suite Setup    Set Global Variable    ${GLOBAL_VAR}    value

*** Keywords ***
Set Global Var
    Set Global Variable    ${NEW_GLOBAL}    another value
```

#### Suite Variables
```robot
*** Keywords ***
init sdw suite
    ${site}=    Create Site
    Set Suite Variable    ${site}
    Set Suite Variable    ${celeb_vol}    ${volume1}
```

**From the code - Suite Variable Pattern:**
```robot
Set Suite Variable    ${filer}
Set Suite Variable    ${celeb_vol}    ${volume1}
```

#### Test Variables
```robot
*** Keywords ***
Create Test Data
    ${test_data}=    Generate Data
    Set Test Variable    ${test_data}
```

#### Local Variables
```robot
*** Test Cases ***
Example
    ${local}=    Set Variable    This is local to this test
    ${another}=    Some Keyword
```

### 6.3 Variable Assignment

```robot
*** Test Cases ***
Variable Assignment Examples
    # Simple assignment
    ${name}=    Set Variable    John
    
    # From keyword return
    ${result}=    Some Keyword    arg1
    
    # Multiple return values
    ${status}    ${message}=    Login    user    pass
    
    # List unpacking
    ${first}    ${second}    @{rest}=    Create List    a    b    c    d
    # ${first} = a, ${second} = b, @{rest} = [c, d]
    
    # Dictionary creation
    ${dict}=    Create Dictionary    key1=value1    key2=value2
    
    # From dictionary - CRITICAL PATTERN
    ${accountA}=    Create Dictionary
    ...    userName=Shivang
    ...    email=shivang@example.com
```

### 6.4 Built-in Variables

```robot
${CURDIR}         # Directory where the test file is
${TEMPDIR}        # System temporary directory
${EXECDIR}        # Directory where execution started
${/}              # Path separator (\ on Windows, / elsewhere)
${:}              # Path separator in PATH (: on Unix, ; on Windows)
${SPACE}          # Space character
${EMPTY}          # Empty string
${True}           # Boolean True
${False}          # Boolean False
${None}           # Python None
${null}           # Same as ${None}
```

### 6.5 Variable Files

**variables.py:**
```python
# Simple variables
VARIABLE_NAME = "value"
NUMBER = 42

# Lists
LIST_VAR = ['item1', 'item2', 'item3']

# Dictionaries
DICT_VAR = {'key1': 'value1', 'key2': 'value2'}

# Dynamic variables (function)
def get_variables(arg1, arg2):
    return {
        'DYNAMIC_VAR': arg1 + arg2,
        'COMPUTED': int(arg1) * int(arg2)
    }
```

**Using variable files:**
```robot
*** Settings ***
Variables    variables.py
Variables    config.py    arg1_value    arg2_value
```

---

## 7. Control Structures

### 7.1 IF / ELSE Statements

**Modern Syntax (Robot Framework 5.0+):**

```robot
*** Test Cases ***
IF Example
    IF    ${value} > 10
        Log    Value is greater than 10
    ELSE IF    ${value} == 10
        Log    Value is exactly 10
    ELSE
        Log    Value is less than 10
    END
```

**Inline IF (Robot Framework 5.0+):**
```robot
${result}=    IF    ${condition}    value_if_true    ELSE    value_if_false
```

**Old Syntax (Pre-5.0):**
```robot
*** Test Cases ***
Old IF Example
    Run Keyword If    ${value} > 10    Log    Greater than 10
    ...    ELSE IF    ${value} == 10    Log    Exactly 10
    ...    ELSE    Log    Less than 10
```

### 7.2 FOR Loops

**Basic FOR Loop:**
```robot
*** Test Cases ***
FOR Loop Example
    FOR    ${item}    IN    @{LIST}
        Log    Processing ${item}
        Process Item    ${item}
    END
```

**FOR with Range:**
```robot
*** Test Cases ***
Range Loop
    FOR    ${i}    IN RANGE    10
        Log    Iteration ${i}
    END
    
    FOR    ${i}    IN RANGE    5    10
        Log    Numbers 5-9: ${i}
    END
    
    FOR    ${i}    IN RANGE    0    10    2
        Log    Even numbers: ${i}
    END
```

**FOR with Enumerate:**
```robot
*** Test Cases ***
Enumerate Example
    FOR    ${index}    ${value}    IN ENUMERATE    @{LIST}
        Log    Item ${index}: ${value}
    END
```

**FOR with ZIP:**
```robot
*** Test Cases ***
ZIP Example
    @{names}=    Create List    Alice    Bob    Charlie
    @{ages}=     Create List    25       30     35
    
    FOR    ${name}    ${age}    IN ZIP    ${names}    ${ages}
        Log    ${name} is ${age} years old
    END
```

**Nested FOR:**
```robot
*** Test Cases ***
Nested Loops
    FOR    ${i}    IN RANGE    3
        FOR    ${j}    IN RANGE    3
            Log    ${i} x ${j} = ${i*j}
        END
    END
```

**BREAK and CONTINUE:**
```robot
*** Test Cases ***
Loop Control
    FOR    ${item}    IN    @{LIST}
        IF    '${item}' == 'skip'
            CONTINUE
        END
        IF    '${item}' == 'stop'
            BREAK
        END
        Process Item    ${item}
    END
```

### 7.3 WHILE Loops (Robot Framework 5.0+)

```robot
*** Test Cases ***
WHILE Example
    ${count}=    Set Variable    0
    WHILE    ${count} < 10
        Log    Count: ${count}
        ${count}=    Evaluate    ${count} + 1
    END

WHILE with Limit
    ${retries}=    Set Variable    0
    WHILE    ${retries} < 5    limit=10 seconds
        ${status}=    Check Service Status
        IF    '${status}' == 'ready'
            BREAK
        END
        Sleep    1s
        ${retries}=    Evaluate    ${retries} + 1
    END
```

### 7.4 TRY / EXCEPT (Robot Framework 5.0+)

```robot
*** Test Cases ***
TRY EXCEPT Example
    TRY
        ${result}=    Risky Operation
        Log    Success: ${result}
    EXCEPT    TimeoutError
        Log    Operation timed out
    EXCEPT    ValueError    AS    ${err}
        Log    Value error occurred: ${err}
    EXCEPT
        Log    Unknown error occurred
    FINALLY
        Cleanup Operation
    END
```

**With Multiple Exceptions:**
```robot
*** Test Cases ***
Multiple Exceptions
    TRY
        Dangerous Operation
    EXCEPT    Error1    Error2    Error3
        Log    One of several errors occurred
    EXCEPT
        Log    Other error
    END
```

---

## 8. Advanced Keyword Concepts

### 8.1 Keyword Arguments

#### Positional Arguments
```robot
*** Keywords ***
Basic Keyword
    [Arguments]    ${arg1}    ${arg2}    ${arg3}
    Log    ${arg1}, ${arg2}, ${arg3}

*** Test Cases ***
Call Keyword
    Basic Keyword    value1    value2    value3
```

#### Default Arguments
```robot
*** Keywords ***
Keyword With Defaults
    [Arguments]    ${required}    ${optional}=default_value    ${another}=${42}
    Log    Required: ${required}
    Log    Optional: ${optional}
    Log    Another: ${another}

*** Test Cases ***
Examples
    Keyword With Defaults    must_provide
    Keyword With Defaults    must_provide    custom_value
    Keyword With Defaults    must_provide    optional=custom    another=${100}
```

#### Named Arguments
```robot
*** Test Cases ***
Named Arguments Example
    Create Dictionary    key1=value1    key2=value2    key3=value3
    Login    username=admin    password=secret
```

#### Variable Number of Arguments
```robot
*** Keywords ***
Keyword With Varargs
    [Arguments]    ${required}    @{varargs}    &{kwargs}
    Log    Required: ${required}
    Log    Varargs: @{varargs}
    Log    Kwargs: &{kwargs}

*** Test Cases ***
Call With Multiple Args
    Keyword With Varargs    req    extra1    extra2    key1=val1    key2=val2
    # ${required} = req
    # @{varargs} = [extra1, extra2]
    # &{kwargs} = {key1: val1, key2: val2}
```

### 8.2 Return Values

#### Single Return
```robot
*** Keywords ***
Get User Name
    ${name}=    Query Database    SELECT name FROM users WHERE id=1
    [Return]    ${name}
```

#### Multiple Returns
```robot
*** Keywords ***
Login And Get Status
    ${success}=    Perform Login    user    pass
    ${message}=    Get Status Message
    [Return]    ${success}    ${message}

*** Test Cases ***
Use Multiple Returns
    ${status}    ${msg}=    Login And Get Status
    Should Be True    ${status}
    Log    ${msg}
```

#### Returning Collections
```robot
*** Keywords ***
Get User Data
    ${data}=    Create Dictionary
    ...    id=123
    ...    name=John
    ...    active=${True}
    [Return]    ${data}

*** Test Cases ***
Use Dictionary Return
    ${user}=    Get User Data
    Log    User ID: ${user}[id]
    Log    User Name: ${user}[name]
```

### 8.3 Embedded Arguments

```robot
*** Keywords ***
User "${username}" Should Have Role "${role}"
    ${user_role}=    Get User Role    ${username}
    Should Be Equal    ${user_role}    ${role}

*** Test Cases ***
Readable Test
    User "admin" Should Have Role "administrator"
    User "guest" Should Have Role "viewer"
```

### 8.4 Private Keywords

```robot
*** Keywords ***
Public Keyword
    [Documentation]    This can be called from test cases
    _Private Helper Keyword    # Convention: prefix with _
    Another Public Keyword

_Private Helper Keyword
    [Documentation]    Internal use only, prefix with _
    Log    This is a helper keyword
```

---

## 9. Test Setup and Teardown

### 9.1 Suite Level

```robot
*** Settings ***
Suite Setup       Initialize Test Environment
Suite Teardown    Cleanup Test Environment

*** Keywords ***
Initialize Test Environment
    Connect To Database
    Clear Test Data
    Create Base Users

Cleanup Test Environment
    Close Database Connection
    Generate Reports
    Archive Logs
```

**From the code:**
```robot
Suite Setup  init sdw suite

*** Keywords ***
init sdw suite
    create director and get site
    ${wf_factory} =   Get Library Instance   wf_factory
    Set Suite Variable    ${wf_factory}
    ${wf} =   Get Library Instance   wf
    Set Suite Variable  ${wf}
    ${filer} =  call method  ${site}  ensure_filer_added  ${Filer_EMC_1}
    Set Suite Variable    ${filer}
    ${volume1} =  call method  ${filer}  add_volume_and_enable  ${auto_sdw_share1_dnd}
    Set Suite Variable  ${celeb_vol}  ${volume1}
```

### 9.2 Test Level

```robot
*** Settings ***
Test Setup        Prepare Test Case
Test Teardown     Cleanup Test Case

*** Keywords ***
Prepare Test Case
    Log    Starting new test
    ${test_id}=    Generate Test ID
    Set Test Variable    ${test_id}

Cleanup Test Case
    Capture Screenshot
    Close All Browsers
    Log    Test completed
```

### 9.3 Per Test Case

```robot
*** Test Cases ***
Special Test
    [Setup]    Custom Setup For This Test Only
    [Teardown]    Custom Teardown For This Test Only
    Test Steps Here

Custom Setup For This Test Only
    Log    Special setup
```

### 9.4 Teardown Execution

**Important: Teardowns ALWAYS run, even if tests fail!**

```robot
*** Keywords ***
Safe Teardown
    Run Keyword And Ignore Error    Close Browser
    Run Keyword And Ignore Error    Disconnect From Database
    Log    Teardown completed
```

---

## 10. Tags and Test Organization

### 10.1 Using Tags

```robot
*** Settings ***
Force Tags     regression    smoke
Default Tags   api

*** Test Cases ***
Critical Feature Test
    [Tags]    critical    feature_x
    Test Implementation

Database Test
    [Tags]    database    slow
    Database Operations

Quick Smoke Test
    [Tags]    smoke    fast    -slow
    Fast Test Operations
```

**From the code:**
```robot
Get Workflow Endpoint by WorkflowServiceID
    [Tags]    custom_action    KOMTEST-TC-22660
```

### 10.2 Running Tests by Tags

```bash
# Run tests with specific tag
robot --include smoke tests/

# Run tests with multiple tags (OR)
robot --include smokeORfast tests/

# Run tests with multiple tags (AND)
robot --include smokeANDfast tests/

# Exclude tests with tag
robot --exclude slow tests/

# Complex tag expressions
robot --include "smokeANDNOTslow" tests/
```

### 10.3 Tag Naming Conventions

**Good practices:**
```robot
[Tags]    feature_name    priority_high    type_api    env_staging
```

**Categories:**
- **Priority**: `priority_high`, `priority_medium`, `priority_low`
- **Type**: `type_ui`, `type_api`, `type_integration`
- **Feature**: `feature_login`, `feature_checkout`
- **Speed**: `speed_fast`, `speed_slow`
- **Environment**: `env_prod`, `env_staging`, `env_dev`
- **Issue**: `bug_JIRA-123`, `ticket_KOMTEST-TC-22660`

### 10.4 Dynamic Tagging

```robot
*** Keywords ***
Add Runtime Tag
    [Arguments]    ${tag}
    Set Tags    ${tag}
    Remove Tags    old_tag

*** Test Cases ***
Dynamic Test
    ${env}=    Get Environment
    Set Tags    env_${env}
```

---

## 11. Data Structures

### 11.1 Lists

#### Creating Lists

```robot
*** Variables ***
@{STATIC_LIST}    item1    item2    item3

*** Test Cases ***
List Operations
    # Create empty list
    @{empty}=    Create List
    
    # Create list with items
    @{items}=    Create List    a    b    c    d
    
    # From the code
    @{volume_ids} =  Create List  ${celeb_vol.id}
```

#### List Operations

```robot
*** Test Cases ***
List Manipulation
    @{list}=    Create List    a    b    c
    
    # Append
    Append To List    ${list}    d
    # list = [a, b, c, d]
    
    # Insert at position
    Insert Into List    ${list}    1    x
    # list = [a, x, b, c, d]
    
    # Remove
    Remove From List    ${list}    0
    # list = [x, b, c, d]
    
    # Get item
    ${first}=    Get From List    ${list}    0
    
    # Get length
    ${length}=    Get Length    ${list}
    
    # Check if contains
    List Should Contain Value    ${list}    b
    
    # Get index
    ${index}=    Get Index From List    ${list}    c
```

### 11.2 Dictionaries

#### Creating Dictionaries

```robot
*** Variables ***
&{STATIC_DICT}    key1=value1    key2=value2

*** Test Cases ***
Dictionary Operations
    # Create empty dictionary
    &{empty}=    Create Dictionary
    
    # Create with key-value pairs
    &{user}=    Create Dictionary
    ...    name=John
    ...    age=30
    ...    active=${True}
    
    # From the code - CRITICAL PATTERN
    ${accountA}=    Create Dictionary
    ...    userName=Shivang
    
    ${parameters}=    Create Dictionary
    ...    numPages=${40}
    ...    accountA=${accountA}
```

#### Dictionary Operations

```robot
*** Test Cases ***
Dictionary Manipulation
    &{dict}=    Create Dictionary    a=1    b=2    c=3
    
    # Get value
    ${value}=    Get From Dictionary    ${dict}    a
    
    # Set value
    Set To Dictionary    ${dict}    d=4    e=5
    
    # Remove
    Remove From Dictionary    ${dict}    b
    
    # Get keys
    ${keys}=    Get Dictionary Keys    ${dict}
    
    # Get values
    ${values}=    Get Dictionary Values    ${dict}
    
    # Check if key exists
    Dictionary Should Contain Key    ${dict}    a
    
    # Get with default
    ${val}=    Get Dictionary Value    ${dict}    nonexistent    default_value
```

#### Nested Dictionaries

**From the code - this is important:**

```robot
${accountA}=    Create Dictionary
...    userName=Shivang

${parameters}=    Create Dictionary
...    numPages=${40}
...    accountA=${accountA}

${workflow_payload}=    Create Dictionary
...    displayName=Shivang_Get_Test
...    workflowServiceClass=CUSTOM_ACTION
...    scriptName=set_metadata
...    parameters=${parameters}
```

**Accessing nested values:**
```robot
${username}=    Set Variable    ${workflow_payload}[parameters][accountA][userName]
```

### 11.3 Converting Between Types

```robot
*** Test Cases ***
Type Conversions
    # List to string
    @{list}=    Create List    a    b    c
    ${string}=    Catenate    SEPARATOR=,    @{list}
    # string = "a,b,c"
    
    # String to list
    ${string}=    Set Variable    x,y,z
    @{list}=    Split String    ${string}    ,
    
    # Dictionary to lists
    &{dict}=    Create Dictionary    a=1    b=2
    @{keys}=    Get Dictionary Keys    ${dict}
    @{values}=    Get Dictionary Values    ${dict}
```

---

## 12. Logging and Debugging

### 12.1 Log Levels

```robot
*** Test Cases ***
Logging Examples
    Log    This is an INFO message    INFO
    Log    This is a DEBUG message    DEBUG
    Log    This is a WARN message     WARN
    Log    This is an ERROR message   ERROR
    Log    No level specified defaults to INFO
```

### 12.2 Console Output

```robot
*** Test Cases ***
Console Logging
    Log To Console    This appears in console
    Log To Console    \nNewline at start
    
    # From the code
    Log To Console    \nFetched JSON: ${json_response}
```

### 12.3 HTML Logging

```robot
*** Test Cases ***
HTML Log
    Log    <b>Bold text</b>    HTML
    Log    <table><tr><td>Cell</td></tr></table>    HTML
```

### 12.4 Screenshots

```robot
*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Capture Evidence
    Capture Page Screenshot
    Capture Page Screenshot    custom_name.png
    Set Screenshot Directory    ${OUTPUT_DIR}/screenshots
```

### 12.5 Debug Keywords

```robot
*** Test Cases ***
Debug Example
    ${value}=    Some Operation
    Log Variables                    # Log all variables
    Log Many    ${var1}    ${var2}    ${var3}
    Log    ${value}    level=DEBUG
    Run Keyword If    ${DEBUG_MODE}    Pause Execution
```

### 12.6 Debugging Failed Tests

```robot
*** Keywords ***
Debug On Failure
    [Arguments]    ${keyword}    @{args}
    ${status}=    Run Keyword And Return Status    ${keyword}    @{args}
    Run Keyword If    not ${status}    Log Variables
    Run Keyword If    not ${status}    Capture Page Screenshot
    Should Be True    ${status}
```

### 12.7 Variable Inspection

```robot
*** Test Cases ***
Inspect Variables
    ${dict}=    Create Dictionary    key=value
    Log    ${dict}                              # Shows: {key: value}
    Log    ${dict}[key]                         # Shows: value
    ${json}=    Evaluate    json.dumps(${dict})    json
    Log    ${json}                              # Shows: {"key": "value"}
```

---

## 13. Best Practices

### 13.1 Naming Conventions

#### Test Cases
```robot
# GOOD - Descriptive, action-oriented
User Can Login With Valid Credentials
Verify Product Added To Cart
System Should Reject Invalid Email Format

# BAD - Vague, non-descriptive
Test1
Login Test
Check Email
```

#### Keywords
```robot
# GOOD - Verb + noun, clear action
Login As User
Verify Dashboard Displays Correctly
Create New Order With Items

# BAD - Unclear, generic
Do Login
Check Page
Create Thing
```

#### Variables
```robot
# GOOD - All caps for constants, descriptive
${BASE_URL}
${DEFAULT_TIMEOUT}
${EXPECTED_ERROR_MESSAGE}

# BAD - Unclear, inconsistent
${url}
${t}
${msg}
```

### 13.2 Keyword Design Principles

#### Single Responsibility
```robot
# GOOD - Each keyword does one thing
*** Keywords ***
Open Login Page
    Open Browser    ${LOGIN_URL}    chrome
    Maximize Browser Window

Enter Credentials
    [Arguments]    ${username}    ${password}
    Input Text    id=username    ${username}
    Input Text    id=password    ${password}

Click Login Button
    Click Button    id=login

Login As User
    [Arguments]    ${username}    ${password}
    Open Login Page
    Enter Credentials    ${username}    ${password}
    Click Login Button

# BAD - Too much in one keyword
Login And Navigate And Verify
    Open Browser    ${URL}    chrome
    Input Text    username    admin
    Input Text    password    pass
    Click Button    login
    Click Link    dashboard
    Element Should Be Visible    welcome
```

#### Abstraction Levels

```robot
# Level 1: Low-level UI interactions
*** Keywords ***
_Enter Text In Field
    [Arguments]    ${locator}    ${text}
    Wait Until Element Is Visible    ${locator}
    Input Text    ${locator}    ${text}

# Level 2: Page-level actions
Enter Username
    [Arguments]    ${username}
    _Enter Text In Field    id=username    ${username}

Enter Password
    [Arguments]    ${password}
    _Enter Text In Field    id=password    ${password}

# Level 3: Business logic
Complete Login
    [Arguments]    ${username}    ${password}
    Enter Username    ${username}
    Enter Password    ${password}
    Click Login Button

# Level 4: Test scenario
User Successfully Logs Into System
    [Arguments]    ${user_type}
    ${creds}=    Get Credentials For    ${user_type}
    Complete Login    ${creds}[username]    ${creds}[password]
    Verify User Is Logged In
```

### 13.3 Error Handling

```robot
*** Keywords ***
Safe Keyword Execution
    [Arguments]    ${keyword}    @{args}
    ${status}    ${result}=    Run Keyword And Ignore Error    ${keyword}    @{args}
    Run Keyword If    '${status}' == 'FAIL'    Log    Keyword failed: ${result}    WARN
    [Return]    ${status}    ${result}

Retry Keyword On Failure
    [Arguments]    ${keyword}    @{args}
    Wait Until Keyword Succeeds    3x    2s    ${keyword}    @{args}

Fail With Custom Message
    [Arguments]    ${condition}    ${message}
    Run Keyword If    ${condition}    Fail    ${message}
```

### 13.4 DRY (Don't Repeat Yourself)

```robot
# BAD - Repetition
*** Test Cases ***
Test User 1
    Open Browser    ${URL}    chrome
    Input Text    username    user1
    Input Text    password    pass1
    Click Button    login
    Element Should Be Visible    dashboard

Test User 2
    Open Browser    ${URL}    chrome
    Input Text    username    user2
    Input Text    password    pass2
    Click Button    login
    Element Should Be Visible    dashboard

# GOOD - Reusable keyword
*** Test Cases ***
Test User 1
    Login As User    user1    pass1
    Dashboard Should Be Visible

Test User 2
    Login As User    user2    pass2
    Dashboard Should Be Visible

*** Keywords ***
Login As User
    [Arguments]    ${username}    ${password}
    Open Browser    ${URL}    chrome
    Input Text    username    ${username}
    Input Text    password    ${password}
    Click Button    login

Dashboard Should Be Visible
    Element Should Be Visible    dashboard
```

### 13.5 Data-Driven Testing

```robot
*** Test Cases ***
Login With Multiple Users
    [Template]    Verify Login
    admin       admin123    success
    user1       pass123     success
    guest       guest456    success
    invalid     wrong       failure

*** Keywords ***
Verify Login
    [Arguments]    ${username}    ${password}    ${expected}
    Attempt Login    ${username}    ${password}
    Run Keyword If    '${expected}' == 'success'    
    ...    Verify Successful Login
    ...    ELSE    Verify Failed Login
```

### 13.6 Documentation

```robot
*** Settings ***
Documentation    This suite tests the user login functionality.
...              
...              Prerequisites:
...              - Application must be deployed
...              - Test users must exist in database
...
...              Test Coverage:
...              - Valid login scenarios
...              - Invalid credential handling
...              - Session management

*** Test Cases ***
User Login With Valid Credentials
    [Documentation]    Verifies that a user with valid credentials can
    ...                successfully log into the system and is redirected
    ...                to the dashboard page.
    ...
    ...                Test Steps:
    ...                1. Navigate to login page
    ...                2. Enter valid username and password
    ...                3. Click login button
    ...                4. Verify redirect to dashboard
    ...
    ...                Expected Result: User is logged in and sees dashboard
    [Tags]    smoke    login    positive
    Test Implementation

*** Keywords ***
Retry Until Success
    [Documentation]    Retries a keyword until it succeeds or max attempts reached.
    ...
    ...                Args:
    ...                    keyword: The keyword to retry
    ...                    max_attempts: Maximum number of retry attempts
    ...                    interval: Wait time between attempts
    ...
    ...                Returns:
    ...                    Result from the successful keyword execution
    ...
    ...                Example:
    ...                    ${result}=    Retry Until Success    Check Status    5    2s
    [Arguments]    ${keyword}    ${max_attempts}=3    ${interval}=1s
    Wait Until Keyword Succeeds    ${max_attempts}x    ${interval}    ${keyword}
```

---

## 14. Enterprise Project Structure

### 14.1 Recommended Directory Layout

```
project_root/
├── tests/
│   ├── ui/
│   │   ├── login/
│   │   │   ├── valid_login.robot
│   │   │   └── invalid_login.robot
│   │   ├── dashboard/
│   │   └── checkout/
│   ├── api/
│   │   ├── users/
│   │   ├── orders/
│   │   └── products/
│   └── integration/
├── resources/
│   ├── keywords/
│   │   ├── ui_keywords.robot
│   │   ├── api_keywords.robot
│   │   └── database_keywords.robot
│   ├── locators/
│   │   ├── login_page.robot
│   │   └── dashboard_page.robot
│   └── variables/
│       ├── environments.robot
│       └── test_data.robot
├── libraries/
│   ├── CustomLibrary.py
│   ├── APIClient.py
│   └── DatabaseHelper.py
├── data/
│   ├── users.csv
│   ├── products.json
│   └── test_config.yaml
├── results/
│   └── .gitkeep
├── scripts/
│   ├── run_tests.sh
│   └── generate_report.py
├── requirements.txt
├── README.md
└── robot.yaml
```

### 14.2 Configuration Management

**robot.yaml:**
```yaml
[General]
outputdir: results
loglevel: INFO
pythonpath:
  - libraries
  - resources

[Prod]
variable:
  - BASE_URL:https://prod.example.com
  - TIMEOUT:30

[Staging]
variable:
  - BASE_URL:https://staging.example.com
  - TIMEOUT:60
  - DEBUG:True
```

**Usage:**
```bash
robot --profile Staging tests/
```

### 14.3 Environment Variables

**environments.robot:**
```robot
*** Variables ***
# Development
${DEV_URL}      http://localhost:3000
${DEV_DB}       dev_database

# Staging
${STAGING_URL}  https://staging.example.com
${STAGING_DB}   staging_database

# Production
${PROD_URL}     https://example.com
${PROD_DB}      prod_database

*** Keywords ***
Get Environment Config
    [Arguments]    ${env}
    ${config}=    Run Keyword If    '${env}' == 'dev'      Get Dev Config
    ...           ELSE IF           '${env}' == 'staging'  Get Staging Config
    ...           ELSE                                     Get Prod Config
    [Return]    ${config}
```

### 14.4 Page Object Pattern

**login_page.robot:**
```robot
*** Variables ***
# Locators
${LOGIN_USERNAME}    id=username
${LOGIN_PASSWORD}    id=password
${LOGIN_BUTTON}      id=login_btn
${ERROR_MESSAGE}     css=.error-msg

*** Keywords ***
Open Login Page
    Go To    ${BASE_URL}/login
    Wait Until Page Contains Element    ${LOGIN_USERNAME}

Enter Login Credentials
    [Arguments]    ${username}    ${password}
    Input Text    ${LOGIN_USERNAME}    ${username}
    Input Text    ${LOGIN_PASSWORD}    ${password}

Submit Login
    Click Button    ${LOGIN_BUTTON}
    Sleep    1s    # Wait for processing

Get Error Message
    ${msg}=    Get Text    ${ERROR_MESSAGE}
    [Return]    ${msg}
```

### 14.5 Parallel Execution with Pabot

**Install:**
```bash
pip install robotframework-pabot
```

**Run in parallel:**
```bash
# Run with 4 parallel processes
pabot --processes 4 tests/

# Run specific tags in parallel
pabot --processes 4 --include smoke tests/

# Split by test suites
pabot --testlevelsplit tests/
```

**Pabot configuration:**
```robot
*** Settings ***
Library    pabot.PabotLib

*** Keywords ***
Acquire Lock For Resource
    [Arguments]    ${resource_name}
    Acquire Lock    ${resource_name}
    [Teardown]    Release Lock    ${resource_name}
```

### 14.6 CI/CD Integration

**Jenkins Pipeline:**
```groovy
pipeline {
    agent any
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'robot --outputdir results tests/'
            }
        }
        stage('Publish Results') {
            steps {
                robot outputPath: 'results',
                      passThreshold: 95.0,
                      unstableThreshold: 90.0
            }
        }
    }
}
```

**GitLab CI:**
```yaml
test:
  image: python:3.9
  before_script:
    - pip install -r requirements.txt
  script:
    - robot --outputdir results tests/
  artifacts:
    when: always
    paths:
      - results/
    reports:
      junit: results/xunit.xml
```

---

## 15. Common Mistakes and Solutions

### 15.1 Variable Scope Issues

**Problem from the code:**
```robot
# Variable ${wf_service} not found in keyword
Get Workflow Service
    [Arguments]    ${wfsID}
    ${response}=    Call Method    ${wf_service}    get_workflow_service    ${wfsID}
    [Return]    ${response}
```

**Root Cause:**
- Suite setup didn't complete
- Variable wasn't set as suite variable
- Wrong file being executed

**Solution:**
```robot
*** Keywords ***
init sdw suite
    ${wf_service}=    Get Library Instance    wf_service
    Should Not Be Equal    ${wf_service}    ${None}    wf_service not found
    Set Suite Variable    ${wf_service}
    Log    wf_service initialized: ${wf_service}    DEBUG
```

### 15.2 Dictionary Syntax Errors

**Problem from the code:**
```robot
# WRONG - Using colon instead of equals
${dict}=    Create Dictionary
...    postAction:log.info('script')  # WRONG!

# CORRECT
${dict}=    Create Dictionary
...    postAction=log.info('script')
```

**Remember:**
- Robot Framework uses `=` for key-value pairs
- Python uses `:` but you're in Robot Framework
- This is one of the most common mistakes

### 15.3 Object vs Dictionary Access

**Problem from the code:**
```robot
${workflow_service}=    Create Workflow Service    ${payload}
# If creation fails, workflow_service is a dictionary with 'errors' key
${id}=    Set Variable    ${workflow_service.id}  # FAILS!
```

**Solution:**
```robot
${workflow_service}=    Create Workflow Service    ${payload}

# Check if creation succeeded
${has_errors}=    Run Keyword And Return Status    
...    Dictionary Should Contain Key    ${workflow_service}    errors

Run Keyword If    ${has_errors}    
...    Fail    Workflow service creation failed: ${workflow_service}[errors]

# Now safe to access
${id}=    Set Variable    ${workflow_service.id}
```

### 15.4 Spacing Issues

**Problem:**
```robot
# WRONG - Only one space between columns
Keyword    arg1   arg2

# CORRECT - Two or more spaces
Keyword    arg1    arg2
```

### 15.5 Continuation Line Indentation

**Problem:**
```robot
# WRONG - Not enough indentation
${dict}=    Create Dictionary
..    key=value

# CORRECT - Four spaces before ...
${dict}=    Create Dictionary
...    key=value
```

### 15.6 Variable Not Assigned

**Problem:**
```robot
# WRONG - Forgetting to assign return value
Some Keyword That Returns Value
Log    ${result}  # ${result} doesn't exist!

# CORRECT
${result}=    Some Keyword That Returns Value
Log    ${result}
```

### 15.7 Incorrect List/Dict Access

**Problem:**
```robot
@{list}=    Create List    a    b    c
${first}=    ${list[0]}  # WRONG syntax

# CORRECT
${first}=    Set Variable    ${list}[0]
# OR
${first}=    Get From List    ${list}    0
```

### 15.8 Not Handling Test Failures in Setup

**Problem:**
```robot
Suite Setup    Complex Setup That Might Fail
# If this fails, no tests run but failure is unclear

# BETTER
Suite Setup    Run Keywords
...    Initialize System    AND
...    Verify System Ready    AND
...    Create Test Data
```

---

## 16. Tips and Tricks

### 16.1 Using Built-in Keywords Effectively

```robot
*** Test Cases ***
Conditional Execution
    # Run keyword only if condition is true
    Run Keyword If    ${condition}    Keyword To Run
    
    # Run keyword and continue even if it fails
    Run Keyword And Ignore Error    Might Fail Keyword
    
    # Run keyword and return status
    ${status}=    Run Keyword And Return Status    Check Something
    
    # Wait until keyword succeeds
    Wait Until Keyword Succeeds    10x    2s    Eventually Succeeds
```

### 16.2 Dynamic Keyword Execution

```robot
*** Test Cases ***
Dynamic Execution
    ${keyword_name}=    Set Variable    Get User Data
    ${result}=    Run Keyword    ${keyword_name}    user_id=123
    
    # With variable number of arguments
    @{args}=    Create List    arg1    arg2    arg3
    Run Keyword    Some Keyword    @{args}
```

### 16.3 Working with Time

```robot
*** Test Cases ***
Time Operations
    # Current time
    ${now}=    Get Current Date
    
    # Format time
    ${formatted}=    Get Current Date    result_format=%Y-%m-%d %H:%M:%S
    
    # Add/subtract time
    ${tomorrow}=    Add Time To Date    ${now}    1 day
    ${yesterday}=    Subtract Time From Date    ${now}    1 day
    
    # Compare dates
    ${diff}=    Subtract Date From Date    ${date1}    ${date2}
```

### 16.4 String Operations

```robot
*** Test Cases ***
String Tricks
    # Convert to lowercase/uppercase
    ${lower}=    Convert To Lowercase    TEXT
    ${upper}=    Convert To Uppercase    text
    
    # Replace string
    ${new}=    Replace String    hello world    world    Robot
    
    # Split and join
    @{parts}=    Split String    a,b,c    ,
    ${joined}=    Catenate    SEPARATOR=-    @{parts}
    
    # Check string content
    Should Contain    ${string}    expected
    Should Start With    ${string}    prefix
    Should End With    ${string}    suffix
```

### 16.5 Working with Collections Efficiently

```robot
*** Test Cases ***
Collection Tips
    # Create and populate in one go
    @{list}=    Evaluate    [i for i in range(10)]
    
    # Dictionary from two lists
    @{keys}=    Create List    a    b    c
    @{values}=    Create List    1    2    3
    &{dict}=    Create Dictionary
    FOR    ${key}    ${value}    IN ZIP    ${keys}    ${values}
        Set To Dictionary    ${dict}    ${key}    ${value}
    END
    
    # Filter list
    @{filtered}=    Evaluate    [x for x in ${list} if x > 5]
```

### 16.6 JSON Handling

```robot
*** Settings ***
Library    Collections

*** Test Cases ***
JSON Operations
    # Convert to JSON string
    &{data}=    Create Dictionary    name=John    age=30
    ${json}=    Evaluate    json.dumps(${data})    json
    
    # Parse JSON string
    ${json_str}=    Set Variable    {"name": "John", "age": 30}
    &{parsed}=    Evaluate    json.loads('''${json_str}''')    json
    
    # Pretty print JSON
    ${pretty}=    Evaluate    json.dumps(${data}, indent=2)    json
    Log    ${pretty}
```

### 16.7 File Operations

```robot
*** Settings ***
Library    OperatingSystem

*** Test Cases ***
File Tricks
    # Read entire file
    ${content}=    Get File    path/to/file.txt
    
    # Read as lines
    @{lines}=    Get File    path/to/file.txt    encoding=UTF-8
    
    # Write to file
    Create File    output.txt    content here
    Append To File    output.txt    more content
    
    # File existence
    File Should Exist    required.txt
    File Should Not Exist    should_not_be_here.txt
    
    # Directory operations
    Create Directory    new_folder
    Directory Should Exist    new_folder
    Remove Directory    old_folder    recursive=True
```

### 16.8 Regular Expressions

```robot
*** Test Cases ***
Regex Usage
    # Match pattern
    Should Match Regexp    test123    \\w+\\d+
    
    # Extract using regex
    ${number}=    Get Regexp Matches    Price: $123.45    \\$([\\d.]+)    1
    # ${number} = ['123.45']
    
    # Replace using regex
    ${cleaned}=    Regexp Replace    test_123_data    _\\d+_    _
```

### 16.9 Environment Variables

```robot
*** Test Cases ***
Environment Tricks
    # Get environment variable
    ${home}=    Get Environment Variable    HOME
    ${path}=    Get Environment Variable    PATH    default=/usr/bin
    
    # Set environment variable
    Set Environment Variable    MY_VAR    my_value
    
    # Check if exists
    ${exists}=    Run Keyword And Return Status    
    ...    Get Environment Variable    SOME_VAR
```

### 16.10 Debugging Tips

```robot
*** Keywords ***
Debug Checkpoint
    [Arguments]    ${message}    @{variables}
    Log    ========== DEBUG: ${message} ==========    WARN
    Log Many    @{variables}
    Log Variables
    # Uncomment when needed: Pause Execution

*** Test Cases ***
Complex Test With Debug Points
    ${data}=    Get Initial Data
    Debug Checkpoint    After getting initial data    ${data}
    
    ${processed}=    Process Data    ${data}
    Debug Checkpoint    After processing    ${processed}
    
    Verify Result    ${processed}
```

### 16.11 Performance Optimization

```robot
*** Test Cases ***
Optimized Test
    # Avoid unnecessary waits
    Set Selenium Implicit Wait    0.5 seconds  # Instead of 10s
    
    # Use explicit waits when needed
    Wait Until Element Is Visible    locator    timeout=5s
    
    # Batch operations
    ${results}=    Create List
    FOR    ${item}    IN    @{items}
        ${result}=    Quick Operation    ${item}
        Append To List    ${results}    ${result}
    END
    # Instead of multiple slow operations
```

### 16.12 Test Data Management

```robot
*** Variables ***
${DATA_FILE}    ${EXECDIR}/data/users.csv

*** Keywords ***
Load Test Users
    ${users}=    Read CSV    ${DATA_FILE}
    [Return]    ${users}

Read CSV
    [Arguments]    ${file_path}
    ${content}=    Get File    ${file_path}
    @{lines}=    Split String    ${content}    \n
    @{users}=    Create List
    FOR    ${line}    IN    @{lines}
        @{fields}=    Split String    ${line}    ,
        &{user}=    Create Dictionary    
        ...    name=${fields}[0]
        ...    email=${fields}[1]
        Append To List    ${users}    ${user}
    END
    [Return]    ${users}
```

### 16.13 Reusable Test Templates

```robot
*** Test Cases ***
Test Login With Different Users
    [Template]    Login Should Succeed
    admin        admin123
    user1        pass123
    manager      manager456

Test Invalid Logins
    [Template]    Login Should Fail
    invalid      wrong_pass
    nonexistent  any_pass
    admin        wrong_pass

*** Keywords ***
Login Should Succeed
    [Arguments]    ${username}    ${password}
    Attempt Login    ${username}    ${password}
    User Should Be Logged In

Login Should Fail
    [Arguments]    ${username}    ${password}
    Attempt Login    ${username}    ${password}
    Error Message Should Be Displayed
```

### 16.14 Custom Reporting

```robot
*** Keywords ***
Log Test Summary
    [Arguments]    ${test_name}    ${status}    ${duration}
    ${summary}=    Catenate    SEPARATOR=\n
    ...    ==========================================
    ...    Test: ${test_name}
    ...    Status: ${status}
    ...    Duration: ${duration}
    ...    ==========================================
    Log    ${summary}    console=True
    
*** Test Cases ***
Example Test
    ${start}=    Get Current Date
    Test Implementation
    ${end}=    Get Current Date
    ${duration}=    Subtract Date From Date    ${end}    ${start}
    Log Test Summary    Example Test    PASS    ${duration}
```

---

## Conclusion

This guide covers Robot Framework from basics to advanced enterprise patterns. Key takeaways:

1. **Always use proper spacing** - Two spaces minimum between columns
2. **Manage variable scope carefully** - Use `Set Suite Variable` for shared state
3. **Use `=` for dictionary key-value pairs**, not `:`
4. **Verify objects exist before accessing properties**
5. **Structure projects for maintainability**
6. **Follow naming conventions consistently**
7. **Document your tests and keywords**
8. **Handle errors gracefully**
9. **Use appropriate abstraction levels**
10. **Leverage parallel execution for faster feedback**

Remember: Robot Framework is powerful because it's **readable**. Keep your tests clean, your keywords focused, and your structure logical. Happy automating!