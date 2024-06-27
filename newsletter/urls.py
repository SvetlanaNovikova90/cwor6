from django.urls import path
from newsletter.views import ClientsListCreateView, mailing_panel, MailingCreateView, mailings_manage, MailingListView, \
    MailingDetailView, toggle_block_status, BlogListView, PartnerListView, PartnersDetailView

app_name = 'mailing'

urlpatterns = [
    path('', BlogListView.as_view(), name='main'),
    path('client_list_create/', ClientsListCreateView.as_view(), name='client_list_create'),
    path('mailing_management/', mailing_panel, name='mailing_panel'),
    path('mailing_form/', MailingCreateView.as_view(), name='mailing_form'),
    path('manage_mailing/', mailings_manage, name='mailings_manage'),
    path('mailings_list_manage/', MailingListView.as_view(), name='mailings_list_manage'),
    path('mailing_detail_manage/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail_manage'),
    path('toggle_block_status/<int:mailing_id>/', toggle_block_status, name='toggle_block_status'),
    path('partners_list_manage/', PartnerListView.as_view(), name='partners_list_manage'),
    path('partners_detail_manage/<int:pk>/', PartnersDetailView.as_view(), name='partners_detail_manage'),
]
