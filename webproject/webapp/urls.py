from django.urls import path

from . import views
from .views import *

app_name = 'table'

urlpatterns = [
    # =====================================================================================>
    # ============================= HOME ==================================================>
    # =====================================================================================>
    path('', views.home, name='home'),
    # =====================================================================================>
    # ============================= Entry Form ============================================>
    # =====================================================================================>
    path('display/', views.displayfunction, name='displayfunction'),
    path('entry_form/', views.entry_form, name='entry_form'),
    # =====================================================================================>
    # ============================= Present Admin =========================================>
    # =====================================================================================>
    path('signin/', views.signin, name='signin'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('register/', views.register, name='register'),
    path('registration/', views.registration, name='registration'),
    path('collapsefunction/', views.collapsefunction, name='collapsefunction'),
    path('table/', views.table, name='table'),
    path('table_edit/', views.table_edit, name='table_edit'),
    path('edit_value/', views.edit_value, name='edit_value'),
    path('pdf/', views.pdf, name='pdf'),
    path('csv_file/', views.csv_file, name='csv_file'),
    # =====================================================================================>
    # ============================= Ex. Admin =============================================>
    # =====================================================================================>
    path('exadmin_signin/', views.exadmin_signin, name='exadmin_signin'),
    path('exadmin_login/', views.exadmin_login, name='exadmin_login'),
    path('exadmin_logout/', views.exadmin_logout, name='exadmin_logout'),
    path('exadmin_display/', views.exadmin_display, name='exadmin_display'),
    path('exadmin_table/', views.exadmin_table, name='exadmin_table'),
    # =====================================================================================>
    # ============================= Recycle Bin ===========================================>
    # =====================================================================================>
    path('recycle_signin/', views.recycle_signin, name='recycle_signin'),
    path('recycle_login/', views.recycle_login, name='recycle_login'),
    path('recycle_logout/', views.recycle_logout, name='recycle_logout'),
    path('recycle/', views.recycle, name='recycle'),
    path('recycle_bin/', views.recycle_bin, name='recycle_bin'),
    path('recycle_data/', views.recycle_data, name='recycle_data'),
    path('recycle_pdf/', views.recycle_pdf, name='recycle_pdf'),
    path('recycle_csv/', views.recycle_csv, name='recycle_csv'),


]
