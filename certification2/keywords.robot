*** Settings ***

Library        RPA.Tables
Library        RPA.Browser.Selenium    auto_close=${FALSE}       
Library        RPA.HTTP
Library        RPA.PDF
Library        RPA.Archive
Library        RPA.FileSystem
Library        RPA.Robocorp.Vault
Library        Dialogs


*** Keywords ***

Input form dialog
    
    ${getCSV}=    Get Value From User    Type URL for CSV      https://robotsparebinindustries.com/orders.csv
    [Return]    ${getCSV}       


Open browser
    [Arguments]    ${url}
    Open Available Browser    ${url}

# Buttons
Press OK
    #Press OK 
    Wait Until Element Is Visible    class:alert-buttons
    Click Button    OK


Preview robot
    Click Button    id:preview
    Wait Until Element Is Visible    id:robot-preview-image
Submit order
    #Wait Until Element Is Visible    id:robot-preview-image
    Click Button    id:order
    Wait Until Element Is Visible    id:receipt    1s
Get orders
    [Arguments]    ${url_csv}
    Download       ${url_csv}    overwrite=True
    ${order}=    Read table from CSV    orders.csv    header=TRUE
    [Return]    ${order}

Fill the form
    [Arguments]    ${row}
    Select From List By Value    id:head    ${row}[Head]
    Select Radio Button    body     ${row}[Body]
    Input Text    xpath://input[@placeholder="Enter the part number for the legs"]    ${row}[Legs]
    Input Text    id:address    ${row}[Address]

Store the receipt as a PDF file
    [Arguments]    ${order_num}
    ${file}=    Join Path    ${CURDIR}    output    ${order_num}.pdf
    Wait Until Element Is Visible   id:receipt   
    ${sales_results_html}=    Get Element Attribute    id:receipt    innerHTML
    Html To Pdf    ${sales_results_html}    ${file}
    [Return]    ${file}

Take a screenshot of the robot
    [Arguments]    ${order_num}
    ${file_pdf}=    Join Path    ${CURDIR}    output    ${order_num}.png
    Screenshot    id:robot-preview-image    ${file_pdf}
    [Return]    ${file_pdf} 

Embed the robot screenshot to the receipt PDF file    
    
    [Arguments]    ${screenshot}    ${pdf}
    ${files}=    Create List    ${screenshot}
    Add Files To Pdf     ${files}    ${pdf}    TRUE  

Log out and close the browser
    Close Browser    


Go to order another robot
    #Press the button "Another Robot" 
    Wait Until Element Is Visible   id:receipt
    Click Button    id:order-another

Archive Output PDF Files to ZIP

    ${outputFolder} =    Join Path    ${CURDIR}    output
    ${archiveFolder} =     Join Path    ${CURDIR}    output    output.zip
    Archive Folder With Zip    ${outputFolder}    ${archiveFolder}


Order robots and save receipts
    ${url_csv}=    Input form dialog 
    
    ${orders}=    Get orders    ${url_csv}

    FOR    ${rows}    IN    @{orders} 
        Press OK
        Log    ${rows}
        Fill the form    ${rows}
        Preview robot
        Wait Until Keyword Succeeds    5x    0.5s    Submit order
        ${pdf}=    Store the receipt as a PDF file  ${rows}[Order number]
        ${screenshot}=    Take a screenshot of the robot    ${rows}[Order number]      
        Embed the robot screenshot to the receipt PDF file    ${screenshot}    ${pdf}       
        Go to order another robot
    END
