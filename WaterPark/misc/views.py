from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import (
    SiteInfo,
    SocialMediaLinks,
    Slider,
    Testimonial,
    TeamMember,
    GalleryImage,
    AboutUs,
)

from .serializers import (
    SiteInfoSerializer,
    SocialMediaLinksSerializer,
    SliderSerializer,
    TestimonialSerializer,
    TeamMemberSerializer,
    GalleryImageSerializer,
    AboutUsSerializer,
)


@extend_schema(
    operation_id="get_site_info",
    summary="Get site information",
    responses={200: SiteInfoSerializer},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def site_info(request):
    obj = SiteInfo.objects.first()

    if not obj:
        raise NotFound("Site info not found.")

    serializer = SiteInfoSerializer(obj)

    return Response(serializer.data)


@extend_schema(
    operation_id="get_social_media_links",
    summary="Get social media links",
    responses={200: SocialMediaLinksSerializer},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def social_media_links(request):
    obj = SocialMediaLinks.objects.first()

    if not obj:
        raise NotFound("Social media links not found.")

    serializer = SocialMediaLinksSerializer(obj)

    return Response(serializer.data)


@extend_schema(
    operation_id="list_sliders",
    summary="Get all sliders",
    responses={200: SliderSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def sliders(request):
    queryset = Slider.objects.all()

    serializer = SliderSerializer(queryset, many=True)

    return Response(serializer.data)


@extend_schema(
    operation_id="list_testimonials",
    summary="Get active testimonials",
    responses={200: TestimonialSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def testimonials(request):
    queryset = Testimonial.objects.filter(is_active=True)

    serializer = TestimonialSerializer(queryset, many=True)

    return Response(serializer.data)


@extend_schema(
    operation_id="list_team_members",
    summary="Get active team members",
    responses={200: TeamMemberSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def team_members(request):
    queryset = TeamMember.objects.filter(is_active=True)

    serializer = TeamMemberSerializer(queryset, many=True)

    return Response(serializer.data)


@extend_schema(
    operation_id="list_gallery_images",
    summary="Get gallery images",
    responses={200: GalleryImageSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def gallery_images(request):
    queryset = GalleryImage.objects.all()

    serializer = GalleryImageSerializer(queryset, many=True)

    return Response(serializer.data)


@extend_schema(
    operation_id="get_about_us",
    summary="Get about us",
    responses={200: AboutUsSerializer},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def about_us(request):
    obj = AboutUs.objects.first()

    if not obj:
        raise NotFound("About Us not found.")

    serializer = AboutUsSerializer(obj)

    return Response(serializer.data)
