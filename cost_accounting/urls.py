from django.urls import path, include
from .views import *


urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', AuthenticationView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('create-spending/', CreateNewSpending.as_view(), name='create-spending'),
    path('create-category/', CreateNewCategory.as_view(), name='create-category'),
    path('history/', SpendingsHistory.as_view(), name='history'),
    path('groups/', GroupsInfo.as_view(), name='groups'),
    path('groups/<int:id>/', CertainGroup.as_view(), name='certain-group'),
]
