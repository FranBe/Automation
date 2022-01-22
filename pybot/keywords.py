'''*** Settings ***'''

import time
from RPA.Browser.Selenium import Selenium
from RPA.PDF import PDF
from RPA.HTTP import HTTP
from RPA.Archive import Archive
from RPA.Tables import Tables
from RPA.FileSystem import FileSystem
from RPA.Dialogs import Dialogs
from RPA.Desktop import Desktop

#--- Initialize objects ---

browser_lib = Selenium()
browser_lib.auto_close = False
http = HTTP()
table = Tables()
pdf = PDF()
fsis = FileSystem()
zip = Archive()
dial = Dialogs()
keys = Desktop()

#--- Variables ---


#def input_form_dialog():
url = 'https://robotsparebinindustries.com/#/robot-order'
urlCSV = 'https://robotsparebinindustries.com/orders.csv'

'''*** Keywords ***'''

#Open URL in browser
def open_website(site):
        browser_lib.open_available_browser(site)

#Press OK button on alert
def pressOK():
    browser_lib.wait_until_element_is_visible("class:alert-buttons")
    browser_lib.click_button("xpath://div[@class='alert-buttons']//button[text()='OK']")

#Preview order
def previewRobot():
    browser_lib.click_button("id:preview")
    browser_lib.wait_until_element_is_visible("id:robot-preview-image")

def submitOrder():

    browser_lib.click_button("id:order")
    time.sleep(1)
    #Check if the error in page exists
    while browser_lib.does_page_contain_element("xpath://div[@class='alert alert-danger']"):
        #if browser_lib.does_page_contain_element("xpath://div[@class='alert alert-danger']"):
        time.sleep(1)
        browser_lib.click_button("id:order")

#Go to order another robot
def getAnotherRobot():
    browser_lib.wait_until_element_is_visible("id:receipt")
    browser_lib.click_button("id:order-another")

#Get the CSV file with orders
def getOrders(site):

    try:
        http.download(site)
        order = table.read_table_from_csv('orders.csv', header=True)
        return order
    except:
        return None


#Fill the form with orders.csv info
def fillForm(row):
    #print(row['Head'])
    browser_lib.select_from_list_by_value("id:head", row['Head'])
    browser_lib.select_radio_button("body", row["Body"])
    browser_lib.input_text("xpath://input[@placeholder='Enter the part number for the legs']", row["Legs"])
    browser_lib.input_text("id:address", row["Address"])

#Store receipt as PDF
def storeAsPdf(order):

    file = fsis.join_path("output", f'{order["Order number"]}.pdf')
    browser_lib.wait_until_element_is_visible("id:receipt")
    #Get element atribute to pass to PDF converter
    html_content = browser_lib.get_element_attribute("id:receipt", attribute="innerHTML")
    pdf.html_to_pdf(html_content, file)
    return file

#Take a screenshot of robot image
def takeScreenshot(order):
    file = fsis.join_path("output", f'{order["Order number"]}.png')
    browser_lib.screenshot("id:robot-preview-image", file)
    return file

#Embed the robot screenshot to the receipt PDF file
def embedScreenToPdf(fpdf, fscreen):
    #print(fpdf)
    #print(fscreen)
    l = [fpdf, fscreen]
    pdf.add_files_to_pdf(files=l, target_document=fpdf)

#Archive Output PDF Files to ZIP
def archiveZip():
    #outputFolder = fsis.join_path("output", "output.zip")
    fileFolder = fsis.join_path("output", "output.zip")
    zip.archive_folder_with_zip("output", fileFolder)

def inputDialog():

    dial.add_heading('CSV URL')
    dial.add_text_input('url', label='https://robotsparebinindustries.com/orders.csv', placeholder='https://robotsparebinindustries.com/orders.csv')

    result = dial.run_dialog()
    return result.url

#Main function for order Robots. 'Order robots and save receipts'
def orderRobots():

    orders = getOrders(urlCSV)
    if orders == None:
        print('Dowload error!!Check your URL for CSV. You may want to use the URL on the dialog window...')
        browser_lib.close_browser()
    else:
        for row in orders:
            pressOK()
            fillForm(row)
            previewRobot()
            submitOrder()

            filePDF = storeAsPdf(row)
            fileScreen = takeScreenshot(row)

            embedScreenToPdf(filePDF, fileScreen)

            getAnotherRobot()

        archiveZip()
        browser_lib.close_browser()











#################################

#Programa

urlCSV = inputDialog()
open_website(url)
orderRobots()


