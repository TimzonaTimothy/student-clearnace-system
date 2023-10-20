from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
import json
from django.shortcuts import get_object_or_404, redirect
# Create your views here.

@login_required(login_url='/sign_in')
def dashboard(request):
    return render(request, 'dashboard.html', {})

@login_required(login_url='/sign_in')
def make_payment_page(request):
    empty_fees = []
    if not request.user.year1_fee:
        empty_fees.append(('Year 1 Fee'))
    if not request.user.year2_fee:
        empty_fees.append(('Year 2 Fee'))
    if not request.user.year3_fee:
        empty_fees.append(('Year 3 Fee'))
    if not request.user.year4_fee:
         empty_fees.append(('Year 4 Fee'))
    if not request.user.year5_fee:
        empty_fees.append(('Year 5 Fee'))
    if request.method == 'POST':
        year = request.POST.get('year',False)
        # request.session['year'] = year
        selected_fee = request.POST.get('selected_fee')
        if selected_fee == 'School Fees':
            fee = SchoolFees.objects.filter(department=request.user.department).first()
            return render(request, 'make_payment.html',{'selected_fee':year,'fee':fee}) 
        elif selected_fee == 'Faculty Fee':
            fee = FacultyFees.objects.filter(department=request.user.department).first()
            status = request.user.department_fee
            return render(request, 'make_payment.html', {'selected_fee':selected_fee,'fee':fee,'status':status}) 
        elif selected_fee == 'Department Fee':
            fee = DepartmentFees.objects.filter(department=request.user.department).first()
            status = request.user.department_fee
            return render(request, 'make_payment.html', {'selected_fee':selected_fee,'fee':fee,'status':status}) 
        elif selected_fee == 'library Fee':
            fee = libraryFees.objects.filter(department=request.user.department).first()
            status = request.user.department_fee
            return render(request, 'make_payment.html', {'selected_fee':selected_fee,'fee':fee,'status':status}) 
        elif selected_fee == 'Medical Fee':
            fee = MedicalFees.objects.filter(department=request.user.department).first()
            status = request.user.department_fee
            return render(request, 'make_payment.html', {'selected_fee':selected_fee,'fee':fee,'status':status}) 
        
    
    return render(request, 'make_payment_page.html', {'empty_fees': empty_fees})

@login_required(login_url='login')
def deposit(request):
    
    user = request.user
    if request.is_ajax():
        amount = request.POST.get('amount', False)
        ref =  request.POST.get('ref', False)
        email = request.POST.get('email', False)
        service = request.POST.get('service',False)
        if request.user.is_authenticated:
            deposit = Userhistory.objects.create(user=user,amount=amount,ref=ref,email=email,service=service)
            deposit.confirm = True
            deposit.transaction = 'Paid'
            deposit.save();
            # if service == 'Year 1 Fee':
            #     user.year1_fee =amount
            #     user.save()
            # elif service == 'Year 2 Fee':
            #     user.year2_fee =amount
            #     user.save()
            # elif service == 'Year 3 Fee':
            #     user.year3_fee =amount
            #     user.save()
            # elif service == 'Year 4 Fee':
            #     user.year4_fee =amount
            #     user.save()
            # elif service == 'Year 5 Fee':
            #     user.year5_fee =amount
            #     user.save()
            # elif service == 'Faculty Fee':
            #     user.faculty_fee =amount
            #     user.save()
            # elif service == 'Department Fee':
            #     user.department_fee =amount
            #     user.save()
            # elif service == 'library Fee':
            #     user.library_fee =amount
            #     user.save()
            # elif service == 'Medical Fee':
            #     user.medical_fee =amount
            #     user.save()
            service_mapping = {
                'Year 1 Fee': 'year1_fee',
                'Year 2 Fee': 'year2_fee',
                'Year 3 Fee': 'year3_fee',
                'Year 4 Fee': 'year4_fee',
                'Year 5 Fee': 'year5_fee',
                'Faculty Fee': 'faculty_fee',
                'Department Fee': 'department_fee',
                'library Fee': 'library_fee',
                'Medical Fee': 'medical_fee',
            }
            if service in service_mapping:
                setattr(user, service_mapping[service], amount)
                user.save()

            deposited = True
            if deposited:
                messages.success(request, 'Deposit, Successful')
                return JsonResponse({'deposited':deposited})


# @login_required(login_url='/sign_in')
# def verify_payment(request, reference):
#     payment = get_object_or_404(Paystack, reference=reference)
#     verified = payment.verify_payment()
#     if verified:
#         messages.success(request, 'Successful Deposit')
#     else:
#         messages.error(request, 'Incomplete Deposit Transaction')
#     return redirect('/')
    

@login_required(login_url='/sign_in')
def deposit_complete(request):
    ref = request.GET.get('ref')
    try:
        paid = Userhistory.objects.get(ref=ref,user=request.user, confirm=True) 
        context={
            'paid':paid
        }
        return render(request, 'deposit_complete.html', context)
    except(Userhistory.DoesNotExist):
        return redirect('/')
    
@login_required(login_url='/sign_in')
def generate_pdf(request, ref):
    # Fetch the Userhistory instance
    paid = get_object_or_404(Userhistory, ref=ref, user=request.user)

    # Load the template for the PDF
    template = get_template('deposit_complete_pdf.html')
    context = {'paid': paid}

    # Render the template with context
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{ref}.pdf"'

    # Create the PDF
    pisaStatus = pisa.CreatePDF(html, dest=response)
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


@login_required(login_url='login')
def payment_history(request):
    payments = Userhistory.objects.all().filter(user=request.user, confirm=True)
    return render(request, 'payment_history.html',{'payments':payments})

@login_required(login_url='/sign_in')
def generate_payment_history_pdf(request):
    payments = Userhistory.objects.filter(user=request.user, confirm=True)
    user = request.user
    # Load the template for the PDF
    template = get_template('payment_history_pdf.html')
    context = {'payments': payments,'user':user}

    # Render the template with context
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="payment_history.pdf"'

    # Create the PDF
    pisaStatus = pisa.CreatePDF(html, dest=response)
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response