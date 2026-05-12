from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse

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
    summary="Get Site Information",
    description="Returns the main site information like name, email, phone, address and logo.",
    responses={
        200: SiteInfoSerializer,
        404: OpenApiResponse(description="Site info not found"),
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
def site_info(request):
    obj = SiteInfo.objects.first()
    if not obj:
        return Response(
            {"detail": "Site info not found."}, status=status.HTTP_404_NOT_FOUND
        )
    return Response(SiteInfoSerializer(obj).data)


@extend_schema(
    summary="Get Social Media Links",
    description="Returns all social media links including Facebook, X, Instagram and LinkedIn.",
    responses={
        200: SocialMediaLinksSerializer,
        404: OpenApiResponse(description="Social media links not found"),
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
def social_media_links(request):
    obj = SocialMediaLinks.objects.first()
    if not obj:
        return Response(
            {"detail": "Social media links not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    return Response(SocialMediaLinksSerializer(obj).data)


@extend_schema(
    summary="Get All Sliders",
    description="Returns a list of all homepage sliders with title, subtitle, description and image.",
    responses={200: SliderSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def sliders(request):
    return Response(SliderSerializer(Slider.objects.all(), many=True).data)


@extend_schema(
    summary="Get Active Testimonials",
    description="Returns all active client testimonials with name, designation, feedback, rating and image.",
    responses={200: TestimonialSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def testimonials(request):
    return Response(
        TestimonialSerializer(
            Testimonial.objects.filter(is_active=True), many=True
        ).data
    )


@extend_schema(
    summary="Get Active Team Members",
    description="Returns all active team members with name, designation, bio, image and social links.",
    responses={200: TeamMemberSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def team_members(request):
    return Response(
        TeamMemberSerializer(TeamMember.objects.filter(is_active=True), many=True).data
    )


@extend_schema(
    summary="Get Gallery Images",
    description="Returns all gallery images ordered by upload date.",
    responses={200: GalleryImageSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def gallery_images(request):
    return Response(GalleryImageSerializer(GalleryImage.objects.all(), many=True).data)


@extend_schema(
    summary="Get About Us",
    description="Returns About Us information including title, description, years of experience, happy visitors and awards.",
    responses={
        200: AboutUsSerializer,
        404: OpenApiResponse(description="About Us not found"),
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
def about_us(request):
    obj = AboutUs.objects.first()
    if not obj:
        return Response(
            {"detail": "About Us not found."}, status=status.HTTP_404_NOT_FOUND
        )
    return Response(AboutUsSerializer(obj).data)
