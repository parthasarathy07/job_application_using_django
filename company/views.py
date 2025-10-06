from django.shortcuts import render, redirect
from .forms import CompanyForm

def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_signup')
    else:
        form = CompanyForm()
    return render(request, 'company/company_form.html', {'form': form})