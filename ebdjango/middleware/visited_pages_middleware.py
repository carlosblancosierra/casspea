class VisitedPagesMiddleware:
    excluded_keywords = ['/media/', '/static']
    excluded_extensions = ['.jpg', '.jpeg', '.png', '.webp']

    def __init__(self, get_response):
        self.get_response = get_response

    def should_exclude(self, url):
        url_lower = url.lower()

        return any(keyword in url_lower for keyword in self.excluded_keywords) or url_lower.endswith(
            tuple(ext.lower() for ext in self.excluded_extensions))

    def __call__(self, request):
        max_visited_pages = 50

        # Retrieve the current list of visited pages from the session
        visited_pages = request.session.get('visited_pages', [])

        # Get the current page URL
        current_page = request.path

        # Check if the current page should be included based on the criteria
        if not visited_pages or (current_page != visited_pages[-1] and not self.should_exclude(current_page)):
            visited_pages.append(current_page)

            # Truncate the list if it exceeds the maximum length
            if len(visited_pages) > max_visited_pages:
                visited_pages = visited_pages[-max_visited_pages:]

        # Update the session with the modified visited pages list
        request.session['visited_pages'] = visited_pages

        response = self.get_response(request)
        return response
