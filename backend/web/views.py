from django.core.paginator import Paginator
from django.shortcuts import render

from communities.models import Community


def home_view(request):
    return render(request, "web/home.html")


def community_list_view(request):
    communities = Community.objects.filter(
        privacy="public"
    ).order_by("name")

    paginator = Paginator(communities, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }

    return render(
        request,
        "web/community_list.html",
        context,
    )
def community_create(request):
    return render(request, "web/community_create.html")