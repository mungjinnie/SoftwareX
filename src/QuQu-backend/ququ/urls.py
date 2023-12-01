
from django.urls import path
from ququ import views

urlpatterns = [
    path('', views.index),
    # path('api/read/<id>',  views.read)
    path('start', views.username),
    path('cat-attr/<ys>/attr', views.getCatandAttr),
    path('cat-attr/url', views.getImageAttr),
    path('cluster', views.getClustering),
    path('naming', views.getStyle),
    path('naming/<ys>/save', views.saveStyle),
    path('ds', views.viewStyle),
    path('ds/url', views.improvement),
    path('ds/improvement/attribute', views.slectimprovement),
    path('ds/ImageGeneration/generate', views.randomgeneration),
    path('ds/ImageGeneration/imagegeneration', views.GANmodels),
    path('toggle', views.saveToggle),
    path('ds/improvement/style', views.saveClicks),
    path('ds/type', views.saveToggle)
]


