import webapp

formulario = """
    <p>URL a acortar:</p>
    <form action="/" method="POST">
      <input name="resource" type="text" />
    <input type="submit" value="Submit" />
    </form>
"""

redirect_body = """
<head>
<meta http-equiv="Refresh" content="0; URL={}">
</head>
"""

url_pinchable = """
<html>
    <body>
        <p>Pincha aqui para ser redirigido:
            <a href={}>{}</a>.
        </p>
        <p>Pincha aqui para ser redirigido:
            <a href={}>{}</a>.
        </p>
    </body>
</html>

"""


def create_entradas(content):
    entradas_html = ""
    for k, v in content.items():
        entradas_html += '<p>' + k + ': ' + v + '</p>\n'
    return entradas_html


class contentApp (webapp.webApp):
    """Simple web application for managing content.

    Content is stored in a dictionary, which is intialized
    with the web content."""

    # Declare and initialize content
    short_url = {}
    long_url = {}

    def parse(self, request):
        """Return the resource name (including /)"""
        request = request.replace("%2F", '/').replace("%3A", ':')
        method = request.split(' ', 1)[0]
        resource = request.split(' ', 2)[1]
        if method == "POST":
            body = request.splitlines()[-1]
        else:
            body = None

        return (method, resource, body)

    def process(self, parsedRequest):
        """Process the relevant elements of the request.
sudo apt install python-pip

        Finds the HTML text corresponding to the resource name,
        ignoring requests for resources not in the dictionary.
        """
        method, resource, body = parsedRequest

        if method == 'GET':
            if resource == '/':
                httpCode = "200 OK"
                entradas_html = create_entradas(self.short_url)
                htmlBody = "<html><body>" + formulario + entradas_html \
                    + "</body></html>"
            elif resource in self.short_url:
                httpCode = "302 Redirect"
                htmlBody = \
                    redirect_body.format("http://" + self.short_url[resource])
            else:
                httpCode = "404 Not Found"
                htmlBody = "Not Found"
        elif method == "POST":

            try:
                resource_request = body.split('=')[1]
            except IndexError:
                httpCode = "404 Not Found"
                htmlBody = "<html><body>Peticion invalida</body></html>"
                return (httpCode, htmlBody)

            httpCode = "200 OK"

            if not(resource_request.startswith('http://') or
                    resource_request.startswith('https://')):
                requested_item = resource_request
                resource_request = 'http://' + resource_request
            else:
                requested_item = \
                    resource_request[resource_request.index('/') + 2:]
            if requested_item not in self.long_url:
                self.long_url[requested_item] = "/" + str(len(self.short_url))
                self.short_url["/" + str(len(self.short_url))] = requested_item

            htmlBody = url_pinchable.format(self.long_url[requested_item],
                                            self.long_url[requested_item],
                                            resource_request, requested_item)

        return (httpCode, htmlBody)


if __name__ == "__main__":
    testWebApp = contentApp("localhost", 1235)
