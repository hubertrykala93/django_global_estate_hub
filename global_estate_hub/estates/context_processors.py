def breadcrumbs_urls(request):
    return {
        'breadcrumbs_urls': request.path.split('/')[1:],
    }
