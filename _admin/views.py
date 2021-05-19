from django.shortcuts import render, get_object_or_404, redirect
from _db import models, utils, auth
from django import forms
from django.contrib.auth import authenticate, login, logout
from . import forms
from django.db.models import Count
from django.forms import modelformset_factory
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseNotFound
from django.forms import inlineformset_factory


def index_view(request):
    username = None
    if request.user.is_authenticated:
        username = f'{request.user.first_name} {request.user.last_name}'
    return render(request, 'admin/index.html', {'user': username})


def test_view(request):
    return render(request, 'admin/test.html')


def update_me_view(request):
    return render(request, 'admin/update-me.html')


def login_view(request):
    alerts = []
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        print(form.data)
        print(form.is_valid())
        if form.is_valid():
            user = auth.EmailAuthBackend.authenticate(email=form.cleaned_data['email'],
                                                      password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('admin_index')
                else:
                    alerts.append('User is not active')
            else:
                alerts.append('User does not exist')
        else:
            alerts.append('Data is incorrect')
    else:
        alerts.append('Please, Sign in')
    return render(request, 'admin/login.html', {'form': forms.LoginForm(), 'alerts': alerts})


def logout_view(request):
    logout(request)
    return redirect('public_index')


def account_transaction_view(request):
    accounts = models.Transfer.objects.all()
    return render(request, 'admin/account-transaction/index.html', {'accounts': accounts})


def account_transaction_detail_view(request, pk):
    transaction = models.Transfer.objects.filter(id=pk)
    return render(request, 'admin/account-transaction/detail.html', {'transaction': transaction})


def account_transaction_create_in_view(request):
    form = forms.AccountTransactionForm(request.POST)
    alerts = []
    if request.method == 'POST' and form.is_valid():
        form.transfer_type = 1
        form.save()
        alerts.append('Запись была успешно добавлена!')

    return render(request, 'admin/account-transaction/create_in.html', {'form': form,
                                                                        'alerts': alerts,
                                                                        })


def account_transaction_create_out_view(request):
    form = forms.AccountTransactionForm(request.POST)
    form.transfer_type = 0

    alerts = []
    if request.method == 'POST' and form.is_valid():
        form.type = 0

        form.save()
        alerts.append('Запись была успешно добавлена!')

    return render(request, 'admin/account-transaction/create_out.html', {'form': form,
                                                                         'alerts': alerts,
                                                                         })


def account_transaction_change_view(request, pk):
    alerts = []
    form = forms.AccountTransactionForm(request.POST or None, instance=get_object_or_404(models.Transfer, id=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно редактирована!')
    transfer = get_object_or_404(models.Transfer, id=pk)
    if transfer.transfer_type.status == 'Приход':
        return render(request, 'admin/account-transaction/create_in.html', {'form': form,
                                                                            'alerts': alerts,

                                                                            })
    else:
        return render(request, 'admin/account-transaction/create_out.html', {'form': form,
                                                                             'alerts': alerts,
                                                                             })


def account_transaction_delete_view(request, pk):
    account_transaction = get_object_or_404(models.Transfer, id=pk)

    account_transaction.delete()
    return redirect('admin_account-transaction')


def invoice_view(request):
    return render(request, 'admin/invoice/index.html')


def invoice_create_view(request):
    form = forms.InvoiceForm(request.POST or None)

    context = {
        'form': form
    }
    return render(request, 'admin/invoice/change.html', context)


def invoice_copy_view(request):
    return render(request, 'admin/invoice/copy.html')


def invoice_change_view(request):
    return render(request, 'admin/invoice/change.html')


def invoice_delete_view(request):
    return render(request, 'admin/invoice/delete.html')


def account_view(request):
    account = models.Account.objects.all()
    return render(request, 'admin/account/index.html', {'account': account})


def account_detail(request, pk):
    account = models.Account.objects.filter(id=pk)
    return render(request, 'admin/account/detail.html', {'account': account})


def account_create_view(request):
    form = forms.AccountForm(request.POST)
    alerts = []
    if request.method == 'POST' and form.is_valid():
        form.save()
        alerts.append('Запись была успешно добавлена!')

    return render(request, 'admin/account/create.html', {'form': form,
                                                         'alerts': alerts
                                                         })


def account_change_view(request, pk):
    alerts = []
    form = forms.AccountForm(request.POST or None, instance=get_object_or_404(models.Account, id=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно редактирована!')
    return render(request, 'admin/account/create.html', {'form': form,
                                                         'alerts': alerts})


def account_delete_view(request, pk):
    account = get_object_or_404(models.Account, id=pk)
    account.delete()
    return render(request, 'admin/account/delete.html')


def apartment_view(request):
    apartment = models.Apartment.objects.all()
    return render(request, 'admin/apartment/index.html',{'apartment': apartment})


def apartment_detail_view(request, pk):
    apartment = get_object_or_404(models.Apartment, id=pk)
    account = models.Account.objects.filter(apartment=apartment)
    return render(request, 'admin/apartment/detail.html', {'apartment': apartment,
                                                           'account': account})


def apartment_create_view(request):
    form = forms.ApartmentForm(request.POST)
    alerts = []
    if request.method == 'POST' and form.is_valid():
        form.save()
        alerts.append('Запись была успешно добавлена!')

    return render(request, 'admin/apartment/create.html', {'form': form,
                                                           'alerts': alerts})


def apartment_change_view(request, pk):
    alerts = []
    form = forms.ApartmentForm(request.POST or None, instance=get_object_or_404(models.Apartment, id=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно редактирована!')
    return render(request, 'admin/apartment/create.html', {'form': form,
                                                           'alerts': alerts})


def apartment_delete_view(request, pk):
    alert = []
    apartment = get_object_or_404(models.Apartment, id=pk)
    apartment.delete()
    alert.append('Запись успешно удалена')
    return render(request, 'admin/apartment/delete.html',)


def user_view(request):
    users = models.User.objects.filter(is_superuser=0)
    return render(request, 'admin/user/index.html', {'users': users})


def user_create_view(request):
    form = forms.UserForm(request.POST, request.FILES)
    alerts = []
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно добавлена!')
        else:
            alerts.append('Неуспешно')

    return render(request, 'admin/user/create.html', {'form': form,
                                                      'alerts': alerts
                                                      })


def user_detail_view(request, pk):
    user = get_object_or_404(models.User, id=pk)
    return render(request, 'admin/user/detail.html', {'user': user})


def user_change_view(request, pk):
    alerts = []
    form = forms.UserForm(request.POST or None, instance=get_object_or_404(models.User, id=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Успех')
        else:
            alerts.append('Неуспешно')
    return render(request, 'admin/user/create.html', {'form': form,
                                                      'alerts': alerts})


def user_delete_view(request, pk):
    user = get_object_or_404(models.User, id=pk)
    user.delete()
    return redirect('admin_user')


def house_view(request):
    houses = models.House.objects.all()
    return render(request, 'admin/house/index.html', {'houses': houses})


def house_edit_view(request, pk):
    house = models.House.objects.get(id=pk)
    floor = models.Floor.objects.filter(section__house=house)
    FloorFormset = modelformset_factory(
        model=models.Floor,
        form=forms.FloorForm,
        max_num=floor.count() if floor.count() > 0 else 1
    )
    UserFormset = inlineformset_factory(
        parent_model=models.House,
        model=models.UserHouse,
        form=forms.UserHouseForm,
        max_num=1
    )
    SectionFormset = inlineformset_factory(
        parent_model=models.House,
        model=models.Section,
        form=forms.SectionForm,
        max_num=1
    )
    aletrs = []
    if request.method == 'POST':

        floor_formset = FloorFormset(request.POST, prefix='floor_form', queryset=models.Floor.objects.filter(section__house=house))
        user_house_formset = UserFormset(request.POST, prefix='user_form', instance=house)
        house_form = forms.HouseForm(request.POST, request.FILES, prefix='house_form', instance=house)
        section_formset = SectionFormset(request.POST, prefix='section_form', instance=house)
        if house_form.is_valid() and section_formset.is_valid() and user_house_formset.is_valid() and floor_formset.is_valid():
            house = house_form.save()
            section_queryset = section_formset.save(commit=False)
            user_house_queryset = user_house_formset.save(commit=False)

            for section in section_queryset:
                section.house.id = house.id
                section.save()

            for user_form in user_house_queryset:
                user_form.house.id = house.id
                user_form.save()

            if utils.forms_save([
                floor_formset
            ]):

                aletrs = ['Формы сохранены']

    else:
        floor_formset = FloorFormset(prefix='floor_form', queryset=models.Floor.objects.filter(section__house=house))
        house_form = forms.HouseForm(prefix='house_form', instance=house)
        section_formset = SectionFormset(prefix='section_form', instance=house)
        user_house_formset = UserFormset(prefix='user_form', instance=house)

    return render(
        request, 'admin/house/edit.html',
        context={
            'floor_formset': floor_formset,
            'user_house_formset': user_house_formset,
            'house_form': house_form,
            'section_formset': section_formset,
            'alerts': aletrs
        }
    )


def house_create_view(request):
    SectionFormset = inlineformset_factory(
        parent_model=models.House,
        model=models.Section,
        fields=('name',),
        form=forms.SectionForm,
        max_num=1
    )
    aletrs = []
    if request.method == 'POST':
        house_form = forms.HouseForm(request.POST, request.FILES, prefix='house_form')
        section_formset = SectionFormset(request.POST, prefix='section_form')
        if house_form.is_valid() and section_formset.is_valid():
            house = house_form.save()
            section_queryset = section_formset.save(commit=False)

            for section in section_queryset:
                section.house.id = house.id
                section.save()

            aletrs = ['Формы сохранены']

    else:
        house_form = forms.HouseForm(prefix='house_form')
        section_formset = SectionFormset(prefix='section_form')

    return render(
        request, 'admin/house/create.html',
        context={
            'house_form': house_form,
            'section_formset': section_formset,
            'alerts': aletrs
        }
    )


def section_delete_view(request, pk):
    section = get_object_or_404(models.Section, id=pk)
    section.delete()
    return HttpResponse()


def user_house_delete_view(request, pk):
    user = get_object_or_404(models.UserHouse, id=pk)
    user.delete()
    return HttpResponse()


def floor_delete_view(request, pk):
    floor = get_object_or_404(models.Floor, id=pk)
    floor.delete()
    return HttpResponse()


def house_delete_view(request, pk):
    house = get_object_or_404(models.House, id=pk)
    house.delete()
    return redirect('admin_house')


def message_view(request):
    messages = models.Message.objects.all()
    return render(request, 'admin/message/index.html', {'messages': messages})


def message_create_view(request):
    alerts = []
    if request.method == 'POST':
        form = forms.MessageCreateForm(request.POST)
        if form.is_valid():
            form.save()
            alerts.append('Сообщение отправлено')
        else:
            alerts.append('Произошла ошибка')
    form = forms.MessageCreateForm()
    return render(request, 'admin/message/create.html', {'form': form,
                                                         'alerts': alerts})


def message_detail_view(request, pk):
    message = get_object_or_404(models.Message, id=pk)
    return render(request, 'admin/message/detail.html', {'message': message})


def message_delete_view(request, pk):
    message = get_object_or_404(models.Message, id=pk)
    message.delete()
    return redirect('admin_message')


def master_request_view(request):
    requests = models.MasterRequest.objects.all()
    return render(request, 'admin/master-request/index.html', {'requests': requests})


def master_request_create_view(request):
    form = forms.MasterRequestForm(request.POST)
    alerts = []
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Заявка создана')
        else:
            alerts.append('Произошла ошибка')
    return render(request, 'admin/master-request/create.html', {'form': form,
                                                                'alerts': alerts})


def master_request_change_view(request, pk):
    alerts = []
    form = forms.MasterRequestForm(request.POST or None, instance=get_object_or_404(models.MasterRequest, id=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно редактирована!')
    return render(request, 'admin/master-request/create.html', {'form': form,
                                                                'alerts': alerts})


def master_request_delete_view(request, pk):
    request = get_object_or_404(models.MasterRequest, id=pk)
    request.delete()
    return redirect('admin_master-request')


def counters_view(request):
    counters = models.Meter.objects.all()  # .order_by('service__name').distinct('service__name') POSTGRES
    print(counters)
    return render(request, 'admin/meter-data/counters.html', {'counters': counters})


def counter_house_view(request, pk):
    counters = models.Meter.objects.filter(apartment_id=pk)
    apartment = models.Apartment.objects.get(id=pk)
    print(counters)
    return render(request, 'admin/meter-data/apartment_detail.html', {'counters': counters,
                                                                      'apartment': apartment})


def meter_data_create_view(request):
    form = forms.CounterForm(request.POST)
    alerts = []
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно добавлена!')
        else:
            alerts.append('Неуспешно')
    return render(request, 'admin/meter-data/create.html', {'form': form,
                                                            'alerts': alerts})


def meter_data_change_view(request, pk):
    alerts = []
    form = forms.CounterForm(request.POST or None, instance=get_object_or_404(models.Meter, id=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно редактирована!')
    return render(request, 'admin/meter-data/create.html', {'form': form,
                                                            'alerts': alerts})


def meter_data_detail_view(request, pk):
    meter = models.Meter.objects.get(id=pk)
    return render(request, 'admin/meter-data/detail.html', {'meter': meter})


def meter_data_delete_view(request, pk):
    meter = get_object_or_404(models.Meter, id=pk)
    meter.delete()
    return redirect('admin_counters-view')


def website_main_page_view(request):

    alerts = []
    MainPageBlockFormset = modelformset_factory(
        model=models.WebsiteMainPageBlocks,
        form=forms.WebsiteMainPageBlocksForm,
        max_num=6,
        min_num=6
    )

    if request.method == 'POST':

        main_page_form = forms.WebsiteMainPageForm(
            request.POST, request.FILES,
            prefix='main_page_form',
        )
        main_page_block_formset = MainPageBlockFormset(
            request.POST, request.FILES,
            prefix='main_page_block_form',
        )
        main_page_seo_form = forms.SEOForm(
            request.POST,
            prefix='main_page_seo_form',
        )

        if utils.forms_save([
            main_page_form,
            main_page_seo_form,
            main_page_block_formset,
        ]):
            alerts.append('Данные сохранены успешно!')

    else:
        main_page: models.WebsiteMainPage = models.WebsiteMainPage.get_solo()
        if not main_page.seo:
            main_page.seo = models.SEO.objects.create()
            main_page.save()

        main_page_form = forms.WebsiteMainPageForm(
            instance=main_page,
            prefix='main_page_form',
        )

        main_page_block_formset = MainPageBlockFormset(
            prefix='main_page_block_form',
        )

        main_page_seo_form = forms.SEOForm(
            instance=main_page.seo,
            prefix='main_page_seo_form',
        )

    context = {
        'alerts': alerts,
        'main_page_form': main_page_form,
        'main_page_block_formset': main_page_block_formset,
        'main_page_seo_form': main_page_seo_form,
    }
    return render(request, 'admin/website/main-page.html', context)


def website_about_gallery_delete_view(request, pk):
    entry = models.WebsiteAboutGallery.objects.get(id=pk)
    entry.delete()
    return HttpResponse()


def website_about_view(request):

    alerts = []
    about_gallery_count = models.WebsiteAboutGallery.objects.count()
    WebsiteAboutGalleryFormset = modelformset_factory(
        model=models.WebsiteAboutGallery,
        form=forms.WebsiteAboutGalleryForm,
        max_num=about_gallery_count if about_gallery_count > 0 else 1,
    )

    if request.method == 'POST':

        about_form = forms.WebsiteAboutForm(
            request.POST, request.FILES,
            prefix='about_form',
        )
        about_gallery_formset = WebsiteAboutGalleryFormset(
            request.POST, request.FILES,
            prefix='about_gallery_form',
        )
        about_seo_form = forms.SEOForm(
            request.POST,
            prefix='about_seo_form',
        )

        if utils.forms_save([
            about_form,
            about_seo_form,
            about_gallery_formset,
        ]):
            alerts.append('Данные сохранены успешно!')

    else:
        about: models.WebsiteAbout = models.WebsiteAbout.get_solo()
        if not about.seo:
            about.seo = models.SEO.objects.create()
            about.save()

        about_form = forms.WebsiteAboutForm(
            instance=about,
            prefix='about_form',
        )

        about_gallery_formset = WebsiteAboutGalleryFormset(
            prefix='about_gallery_form',
        )

        about_seo_form = forms.SEOForm(
            instance=about.seo,
            prefix='about_seo_form',
        )

    context = {
        'alerts': alerts,
        'about_form': about_form,
        'about_gallery_formset': about_gallery_formset,
        'about_seo_form': about_seo_form,
    }
    return render(request, 'admin/website/about.html', context)


def website_services_blocks_delete_view(request, pk):
    entry = models.WebsiteServiceBlocks.objects.get(id=pk)
    entry.delete()
    return HttpResponse()


def website_services_view(request):
    service_count = models.WebsiteServiceBlocks.objects.count()
    MainPageServiceBlocksFormset = modelformset_factory(
        model=models.WebsiteServiceBlocks,
        form=forms.WebsiteServiceBlocksForm,
        fields=('image', 'name', 'description'),
        max_num=service_count if service_count > 0 else 1,
    )

    alerts = []
    if request.method == "POST":
        service_formset = MainPageServiceBlocksFormset(
            request.POST, request.FILES,
            prefix='service')
        utils.form_save(service_formset)
        seo_form = forms.SEOForm(request.POST, prefix='SEO')
        alerts.append('Услуги сохранены успешно!')

    else:
        service_formset = MainPageServiceBlocksFormset(prefix='service')
        service_instance = models.WebsiteService.get_solo()
        if not service_instance.seo:
            service_instance.seo = models.SEO.objects.create()
            service_instance.save()
        seo_form = forms.SEOForm(instance=service_instance.seo, prefix='SEO')

    context = {
        'formset': service_formset,
        'seo_form': seo_form,
        'alerts': alerts,
    }
    return render(
        request, 'admin/website/services.html', context)


def website_tariffs_blocks_delete_view(request, pk):
    entry = models.WebsiteTariffBlocks.objects.get(id=pk)
    entry.delete()
    return HttpResponse()


def website_tariffs_view(request):
    tariffs_count = models.WebsiteTariffBlocks.objects.count()
    TariffsBlockFormset = modelformset_factory(
        model=models.WebsiteTariffBlocks,
        form=forms.WebsiteTariffsBlocksForm,
        max_num=tariffs_count if tariffs_count > 0 else 1,
    )

    alerts = []
    if request.method == 'POST':

        tariffs_form = forms.WebsiteTariffsForm(
            request.POST, request.FILES,
            prefix='tariffs_form',
        )
        tariffs_block_formset = TariffsBlockFormset(
            request.POST, request.FILES,
            prefix='tariffs_block_form',
        )
        tariffs_seo_form = forms.SEOForm(
            request.POST,
            prefix='tariffs_seo_form',
        )

        if utils.forms_save([
            tariffs_form,
            tariffs_block_formset,
            tariffs_seo_form,
        ]):
            alerts.append('Данные сохранены успешно!')

    else:
        tariffs: models.WebsiteTariffs = models.WebsiteTariffs.get_solo()

        if not tariffs.seo:
            tariffs.seo = models.SEO.objects.create()
            tariffs.save()

        tariffs_form = forms.WebsiteTariffsForm(
            instance=tariffs,
            prefix='tariffs_form',
        )

        tariffs_block_formset = TariffsBlockFormset(
            prefix='tariffs_block_form',
        )

        tariffs_seo_form = forms.SEOForm(
            instance=tariffs.seo,
            prefix='tariffs_seo_form',
        )

    context = {
        'alerts': alerts,
        'tariffs_form': tariffs_form,
        'tariffs_block_formset': tariffs_block_formset,
        'tariffs_seo_form': tariffs_seo_form,
    }
    return render(request, 'admin/website/tariffs.html', context)


def website_contact_view(request):

    alerts = []
    if request.method == "POST":
        contact_form = forms.WebsiteContactsForm(request.POST, prefix='contacts')
        contact_seo_form = forms.SEOForm(request.POST, prefix='SEO')
        if utils.forms_save([
            contact_form,
            contact_seo_form,
        ]):
            alerts.append('Данные сохранены успешно!')

    else:
        contacts: models.WebsiteContacts = models.WebsiteContacts.get_solo()
        if not contacts.seo:
            contacts.seo = models.SEO.objects.create()
            contacts.save()
        contact_form = forms.WebsiteContactsForm(
            instance=contacts,
            prefix='contacts',
        )
        contact_seo_form = forms.SEOForm(
            instance=contacts.seo,
            prefix='SEO',
        )
    context = {
        'contact_form': contact_form,
        'contact_seo_form': contact_seo_form,
        'alerts': alerts,
    }
    return render(request, 'admin/website/contact.html', context)


def services_view(request):
    alerts = []
    service_count = models.Service.objects.all().count()
    measure_count = models.Measure.objects.all().count()
    ServiceFormset = modelformset_factory(
        model=models.Service,
        form=forms.ServiceForm,
        max_num=service_count if service_count > 0 else 1,

    )
    MeasureFormset = modelformset_factory(
        model=models.Measure,
        form=forms.MeasureForm,
        max_num=measure_count if measure_count > 0 else 1,
    )

    if request.method == 'POST':

        service_formset = ServiceFormset(
            request.POST,
            prefix='service_form',
        )
        measure_formset = MeasureFormset(
            request.POST,
            prefix='measure_form'
        )

        if utils.forms_save([
            measure_formset,
            service_formset,
        ]):
            alerts.append('Данные сохранены успешно!')
        return redirect('admin_services')

    else:
        service_formset = ServiceFormset(
            prefix='service_form',
        )
        measure_formset = MeasureFormset(
            prefix='measure_form'
        )

    context = {
        'alerts': alerts,
        'service_formset': service_formset,
        'measure_formset': measure_formset,
    }
    return render(request, 'admin/services/services.html', context)


def services_del_view(request, pk):
    entry = models.Service.objects.get(id=pk)
    entry.delete()
    return HttpResponse()


def measure_del_view(request, pk):
    entry = models.Measure.objects.get(id=pk)
    entry.delete()
    return HttpResponse()


def tariffs_view(request):
    context = {
        'tariff': models.Tariff.objects.all(),
    }
    return render(request, 'admin/tariffs/index.html', context)


def tariffs_create_view(request):
    TariffServiceFormset = inlineformset_factory(
        parent_model=models.Tariff,
        model=models.TariffService,
        fields=('price', 'service'),
        widgets={
            'price': forms.TextInput(attrs={
                'placeholder': 'Введите цену',
                'type': 'text',
                'class': 'form-control',
                'style': 'margin: 0.25rem 0',
            }),

        },
        form=forms.TariffServiceForm,
        max_num=1
    )
    aletrs = []
    if request.method == 'POST':
        tariff_form = forms.TariffCreateForm(request.POST, prefix='tariff_form')
        tariff_service_formset = TariffServiceFormset(request.POST, prefix='tariff_service_form')
        if tariff_form.is_valid() and tariff_service_formset.is_valid():
            tariff = tariff_form.save()
            tariff_service_queryset = tariff_service_formset.save(commit=False)

            for tariff_section_form in tariff_service_queryset:
                tariff_section_form.tariff.id = tariff.id
                tariff_section_form.save()

            aletrs = ['Формы сохранены']

    else:
        tariff_form = forms.TariffCreateForm(prefix='tariff_form')
        tariff_service_formset = TariffServiceFormset(prefix='tariff_service_form')

    return render(
        request, 'admin/tariffs/create.html',
        context={
            'tariff_form': tariff_form,
            'tariff_service_formset': tariff_service_formset,
            'alerts': aletrs
        }
    )


def tariffs_change_view(request, pk=None):
    tariff = models.Tariff.objects.get(id=pk)
    tariff_service_count = models.TariffService.objects.filter(tariff=tariff).count()
    TariffServiceFormset = inlineformset_factory(
        parent_model=models.Tariff,
        model=models.TariffService,
        fields=('price', 'service'),
        widgets={
            'price': forms.TextInput(attrs={
                'placeholder': 'Введите цену',
                'type': 'text',
                'class': 'form-control',
                'style': 'margin: 0.25rem 0',
            }),

        },
        form=forms.TariffServiceForm,
        max_num=tariff_service_count if tariff_service_count > 0 else 1
    )
    aletrs = []
    if request.method == 'POST':
        tariff_form = forms.TariffCreateForm(request.POST, prefix='tariff_form', instance=tariff)
        tariff_service_formset = TariffServiceFormset(request.POST, prefix='tariff_service_form', instance=tariff)
        if tariff_form.is_valid() and tariff_service_formset.is_valid():
            tariff = tariff_form.save()
            tariff_service_queryset = tariff_service_formset.save(commit=False)

            for tariff_section_form in tariff_service_queryset:
                tariff_section_form.tariff.id = tariff.id
                tariff_section_form.save()

            aletrs = ['Формы сохранены']

    else:
        tariff_form = forms.TariffCreateForm(prefix='tariff_form', instance=tariff)
        tariff_service_formset = TariffServiceFormset(prefix='tariff_service_form', instance=tariff)

    return render(
        request, 'admin/tariffs/create.html',
        context={
            'tariff_form': tariff_form,
            'tariff_service_formset': tariff_service_formset,
            'alerts': aletrs
        }
    )


def tariffs_copy_view(request):
    return render(request, 'admin/tariffs/copy.html')


def tariff_detail_view(request, pk):
    tariff = models.Tariff.objects.get(id=pk)
    tariff_service = models.TariffService.objects.filter(tariff=tariff)
    print(tariff_service)
    return render(request, 'admin/tariffs/detail.html', {'tariff': tariff,
                                                         'tariff_service': tariff_service
                                                         })


def tariffs_delete_view(request, pk):
    entry = models.Tariff.objects.get(id=pk)
    entry.delete()
    return redirect('admin_tariffs')


def tariffs_service_delete_view(request, pk):
    entry = models.TariffService.objects.get(id=pk)
    entry.delete()
    return HttpResponse()

def user_admin_role_view(request):

    alerts = []
    UserRoleFormset = modelformset_factory(
        model=models.UserRole,
        form=forms.RoleForm,
        max_num=5,
        min_num=5
    )

    if request.method == 'POST':

        user_role_formset = UserRoleFormset(
            request.POST,
            prefix='user_role_form',
        )

        if utils.forms_save([
            user_role_formset,
        ]):
            alerts.append('Данные сохранены успешно!')
        return redirect('admin_user-admin-role')

    else:
        user_role_formset = UserRoleFormset(
            prefix='user_role_form',
        )

    context = {
        'alerts': alerts,
        'user_role_formset': user_role_formset
    }
    return render(request, 'admin/user-admin/role.html', context)


def user_admin_users_list(request):
    users_list = models.User.objects.filter(is_superuser=1)
    print(users_list)
    return render(request, 'admin/user-admin/list.html', {'users_list': users_list})


def user_admin_create_view(request):
    form = forms.UserCreateForm(request.POST or None)
    form.instance.is_superuser = 1
    if request.method == 'POST' and form.is_valid():
        form.instance.is_superuser = 1
        form.save()
        return redirect('admin_user-users-list')
    return render(request, 'admin/user-admin/create.html', {'form': form})


def user_admin_change_view(request, pk):
    user = models.User.objects.get(id=pk)
    alerts = []
    form = forms.UserCreateForm(request.POST or None, instance=user)
    print(form.is_valid())
    if request.method == 'POST' and form.is_valid():
        form.instance.is_superuser = 1
        form.save()
        alerts.append('Успех')
    return render(request, 'admin/user-admin/create.html', {'form': form,
                                                            'alerts': alerts})


def user_admin_detail_view(request, pk):
    user = models.User.objects.get(id=pk)
    return render(request, 'admin/user-admin/detail.html', {'user': user})


def user_admin_delete_view(request, pk):
    return redirect('admin_master-request')


def pay_company_view(request):
    form = forms.PaymentCompany(request.POST or None, instance=models.Requisites.get_solo())
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('admin_pay-company')
    return render(request, 'admin/pay-company.html', {'form': form})


def transaction_purpose_view(request):
    transfer_type = models.TransferType.objects.all()
    return render(request, 'admin/transaction-purpose/index.html', {'transfer_type': transfer_type})


def transaction_purpose_create_view(request):
    form = forms.TransactionPurposeForm(request.POST)
    alerts = []
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно добавлена!')
        else:
            alerts.append('Неуспешно')
    return render(request, 'admin/transaction-purpose/create.html', {'form': form,
                                                                     'alerts': alerts})


def transaction_purpose_change_view(request, pk):
    alerts = []
    form = forms.TransactionPurposeForm(request.POST or None, instance=get_object_or_404(models.TransferType, id=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Успех')
        else:
            alerts.append('Неуспешно')
    return render(request, 'admin/transaction-purpose/create.html', {'form': form,
                                                                     'alerts': alerts})


def transaction_purpose_delete_view(request, pk):
    transfer_type = get_object_or_404(models.TransferType, id=pk)
    transfer_type.delete()
    return redirect('admin_transaction-purpose')
