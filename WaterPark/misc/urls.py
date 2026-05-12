from django.urls import path
from . import views

urlpatterns = [
    path("site-info/", views.site_info, name="site-info"),
    path("social-media/", views.social_media_links, name="social-media"),
    path("sliders/", views.sliders, name="sliders"),
    path("testimonials/", views.testimonials, name="testimonials"),
    path("team/", views.team_members, name="team"),
    path("gallery/", views.gallery_images, name="gallery"),
    path("about/", views.about_us, name="about"),
]
