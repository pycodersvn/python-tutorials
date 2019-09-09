import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# PDF Kit example
import pdfkit, os
from django.template.loader import render_to_string
from django_slugify_processor.text import slugify
from pytz import timezone

tz = timezone('EST')

def index(request):
    template = loader.get_template('export/index.html')
    context = {
        'msg': 'Test export PDF use PDF kit',
    }
    return HttpResponse(template.render(context, request))

def render(request):

    filename = 'demo-export'
    user_data = None
    options = {
        'header': False,
        'content': False,
        'footer': False,
        'data': {
            'title': 'PyCoders',
            'created_at': datetime.datetime.now(tz).strftime('%B %d, %Y @ %H:%M%p %Z')
        }
    }
    
    # Handle request options
    data = request.GET

    options['header'] = data.get('header') in ['true','1']
    options['content'] = data.get('content') in ['true','1']
    options['footer'] = data.get('footer') in ['true','1']

    # Generate PDF 
    template_path = 'export/pdf-templates/index.html'
    html = render_to_string(template_path, options)
    filename = slugify("%s-%s" % (filename, datetime.datetime.now(tz).strftime('%B %d, %Y @ %H:%M%p %Z')))
    pdf_output = "static/%s.pdf" % filename
    pdfkit.from_string(html, pdf_output)

    # Read file content and force download as PDF file 
    with open(pdf_output, 'rb') as f:
        pdf = f.read()
        f.close()
    
    response = HttpResponse(pdf, content_type='application/pdf')  
    response['Content-Disposition'] = 'attachment; filename=%s.pdf' % filename
    return response

    # Test
    # http://localhost:8100/export/render?header=1
    # http://localhost:8100/export/render?header=1&content=1
    # http://localhost:8100/export/render?header=1&content=1&footer    

def test(request):

    # Data is the context data that is sent to the html file to render the output.
    # Renders the template with the context data.
    data = {'foo': 'bar'}
    html_rendered = render_to_string('export/output_pdf.html', data)

    # Generate PDF from template file
    pdfkit.from_string(html_rendered, 'out.pdf')
    
    # Open generated PDF file and generates the response as pdf response.
    with open("out.pdf", 'rb') as f:
        pdf = f.read()
        f.close()
    
    response = HttpResponse(pdf, content_type='application/pdf')  
    response['Content-Disposition'] = 'attachment; filename=output.pdf'

    # Remove the locally created pdf file.
    os.remove("out.pdf") 
    
    # Returns the response.
    return response  

