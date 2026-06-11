from django.urls import path
from contributions.views import(
    PagIbigDetailView,PagIbigListView,
    PhilHealthDetailView,PhilHealthListView,
    SSSContributionListView,SSSContributionDetailView,
    WithHoldingListView,WithHoldingDetailsView
)

urlpatterns = [
path('pag-ibig/',PagIbigListView.as_view()),
path('pag-ibig/<int:pk>/',PagIbigDetailView.as_view()),
path('phil-health/',PhilHealthListView.as_view()),
path('phil-health/<int:pk>/',PhilHealthDetailView.as_view()),
path('sss/',SSSContributionListView.as_view()),
path('sss/<int:pk>/',SSSContributionDetailView.as_view()),
path('with-holding-tax/',WithHoldingListView.as_view()),
path('with-holding-tax/<int:pk>/',WithHoldingDetailsView.as_view()),

]