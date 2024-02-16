from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.indexfood,name="indexfood"),
    path('market', views.indexmarket,name="indexmarket"),
    path('users',views.indexusers,name="indexusers"),
    path('users2',views.indexusers2,name="indexusers2"),
    path('recipe',views.recipe,name="recipe"),
    path('delIngredients/<int:uid>',views.delIngredients, name ="delIngredients"),
    path('add', views.add,name="add"),
    path('add2', views.add2,name="add2"),
    path('filter', views.filter,name="filter"),
    path('details/<int:uid>', views.details, name="details"),
    path('recipe2',views.recipe2,name="recipe2"),
    path('details2/<int:uid>', views.details2, name="details2"),
    path('dologin', views.dologin,name="dologin"),
    path('logout', views.logout,name="logout"),
    path('dologin2', views.dologin2,name="dologin2"),
    path('details3', views.details3,name="details3"),
    path('insertusers', views.insertusers,name="insertusers"),
    path('recipe3', views.recipe3,name="recipe3"),
    #配置users信息操作路由
  
]