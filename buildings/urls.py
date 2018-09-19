from django.urls import path

from buildings import views

urlpatterns = [
    path('company/<str:id>/buildings', views.get_company_buildings),

    path('buildings', views.Building.as_view()),
    path('buildings/<str:id>', views.Building.as_view()),
    path('buildings/<str:id>/houses', views.get_building_houses),

    path('houses', views.House.as_view()),
    path('houses/<str:id>', views.House.as_view()),

    path('houses/<str:id>/flats-schemas', views.get_house_ftats_schemas),

    path('flats-schemas', views.FlatSchema.as_view()),
    path('flats-schemas/<str:id>', views.FlatSchema.as_view()),

    path('houses/<str:id>/floor-types', views.get_house_floor_types),

    path('floor-types', views.FloorType.as_view()),
    path('floor-types/<str:id>', views.FloorType.as_view()),

    path('floor-type/<str:id>/flat-types', views.get_floor_type_flat_types),

    path('flat-types', views.FlatType.as_view()),
    path('flat-types/<str:id>', views.FlatType.as_view()),

    path('flats/numbering', views.numbering_flats),
    path('houses/<str:id>/flats', views.get_house_flats),
    # path('flats', views.Flat.as_view()),
    # path('flats/<str:id>', views.Flat.as_view()),
]

# http://127.0.0.1:8000/buildings/1/houses
# http://127.0.0.1:8000/houses
# http://127.0.0.1:8000/houses/1
