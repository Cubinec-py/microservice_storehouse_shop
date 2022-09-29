from django.http import JsonResponse
from django.template.loader import render_to_string
from contact_us.forms import ContactCreateForm

from contact_us.tasks import contactus


def save_contactus_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['text']
            from_email = form.cleaned_data['email']
            contactus(subject, message, from_email)
            # contactus.delay(subject, message, from_email)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def contact_us(request):
    if request.method == 'POST':
        form = ContactCreateForm(request.POST)
    else:
        form = ContactCreateForm()
    return save_contactus_form(request, form, 'contact_us/contactus_form.html')
