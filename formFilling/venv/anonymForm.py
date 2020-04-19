#!/usr/bin/env python3

# fill_by_overlay.py
import pdfrw
import sys
import json
#import pypdftk
from reportlab.pdfgen import canvas

def error_exit(message):
    sys.stderr.write(message)
    sys.exit(1)

def create_overlay(json_data):
    """
    Create the data that will be overlayed on top
    of the form that we want to fill
    """
    # Get the data values from the JSON string to json_data
    # In terms of the PDF in question we will only be addressing the "Charge Information" Section
    # All other sections should be pre-filled!
    try:

        arrestData = json.loads(json_data)

        # Pertinent Data
        mail_record_to = arrestData['mail_record_to']
        date_report = arrestData['date_report']
        time_report = arrestData['time_report']
        date_crime = arrestData['date_crime']
        location_crime = arrestData['location_crime']
        time_crime = arrestData['time_crime']
        crime_description = arrestData['crime_description']
        suspect_description = arrestData['suspect_description']

    except Exception as e:
        error_exit("Invalid JSON data: ")
        print(e)

    c = canvas.Canvas('simple_form_overlay.pdf')

    c.setFont("Courier", 18)
    c.drawString(40, 700, date_report) # Date of Report x 1
    c.setFont("Courier", 9)
    c.drawString(240, 535, date_report) # Date of Report x 2
    c.drawString(515, 535, date_report)  # Date of Report x 2
    c.setFont("Courier", 18)
    c.drawString(180, 700, time_report) # Time of Report
    c.setFont("Courier", 12)
    c.drawString(40, 824, mail_record_to) # Mail To
    c.drawString(40, 740, location_crime) # Location of Crime
    c.drawString(148, 630, date_crime) # Date of Crime
    c.drawString(240, 630, time_crime) # Time of Crime
    c.drawString(40, 608, crime_description)  # Description of Crime
    c.drawString(40, 597, suspect_description)  # Description of Suspect

    c.save()
    return


def merge_pdfs(form_pdf, overlay_pdf, output):
    """
    Merge the specified fillable form PDF with the
    overlay PDF and save the output
    """
    form = pdfrw.PdfReader(form_pdf)
    olay = pdfrw.PdfReader(overlay_pdf)

    for form_page, overlay_page in zip(form.pages, olay.pages):
        merge_obj = pdfrw.PageMerge()
        overlay = merge_obj.add(overlay_page)[0]
        pdfrw.PageMerge(form_page).add(overlay).render()

    writer = pdfrw.PdfWriter()
    writer.write(output, form)

def testJSONtoPDF():
    fil = open('answers_ANONYM.txt')
    lis = fil.readlines()
    data = {\
        'lines' : lis, \
        'mail_record_to' : '12 Bedford Ave, Brooklyn, NY, 11203', \
        'date_report' : '10/26/1997', \
        'time_report': '11:25PM', \
        'date_crime' : '10/20/1997', \
        'location_crime' : '99 glenwood rd, Englewood, NJ, 07631', \
        'time_crime' : '12:08PM', \
        'crime_description' : 'Stabbing', \
        'suspect_description' : 'Middle-aged, red sweatshirt, face tattoo of a chair, big booty' \
        }

    json_data = json.dumps(data)
    return json_data


if __name__ == '__main__':

    ## Comment below out when we figure this shit out
    json_data = testJSONtoPDF()

    create_overlay(json_data)
    merge_pdfs('policeReport.pdf',
               'simple_form_overlay.pdf',
               'merged_form.pdf')
    #pypdftk.fill_form('merged_form.pdf', out_file='merged_form_final.pdf', flatten=True)