*** Settings ***
Documentation     Orders robots from RobotSpareBin Industries Inc.
...               Saves the order HTML receipt as a PDF file.
...               Saves the screenshot of the ordechromered robot.
...               Embeds the screenshot of the robot to the PDF receipt.
...               Creates ZIP archive of the receipts and the images.

# Resources

Resource   keywords.robot
Library    RPA.Browser.Selenium    auto_close=${FALSE}       
Library    RPA.Robocorp.Vault


#####################################################################
*** Variables ***

${url_site}=    https://robotsparebinindustries.com/#/robot-order

#####################################################################
*** Tasks ***

Order robots from RobotSpareBin Industries Inc 
    ${secret}=    Get Secret    website
    Open browser        ${secret}[url]
    Order robots and save receipts
    Archive Output PDF Files to ZIP
    [Teardown]    Close Browser
