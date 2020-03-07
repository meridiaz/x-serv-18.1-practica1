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

num = 0

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
    short_url = {'/page': 'google.com',
               '/meri': 'a meri'
               }
    long_url= {'google.com': 'http://localhost:1234/page'}

    def parse(self, request):
        """Return the resource name (including /)"""
        method = request.split(' ', 1)[0]
        resource = request.split(' ', 2)[1]
        if method == "POST":
            body = request.splitlines()[-1]
        else:
            body = None

        return (method, resource, body)

    def process(self, parsedRequest):
        """Process the relevant elements of the request.

        Finds the HTML text corresponding to the resource name,
        ignoring requests for resources not in the dictionary.
        """
        method, resource, body = parsedRequest

        #if method == 'PUT':
         #   page, content = body.split('&')
          #  resource_request = page.split('=')[1]
           # content = content.split('=')[1]
            #self.content["/"+resource_request] = content
        if method == 'GET': 
            if resource == '/':
                httpCode = "200 OK"
                entradas_html = create_entradas(self.short_url)
                htmlBody = "<html><body>" + formulario+ entradas_html +"</body></html>"
            elif resource in self.short_url:
                httpCode = "302 Redirect"
                htmlBody = redirect_body.format(self.short_url[resource])
            else:
                httpCode = "404 Not Found"
                htmlBody = "Not Found"
        elif method == "POST":
            httpCode = "200 OK"
            resource_request = body.split('=')[1]
            if not(resource_request.startswith('http://') or resource_request.startswith('https://')):
                requested_item = resource_request
                resource_request = 'http://' + resource_request
            else:
                requested_item = resource_request[resource_request.index('/') + 2:]
            if requested_item in self.long_url:
                htmlBody = "<html><body><p><a href="+self.long_url[requested_item] + ">pincha aqui para ser redirigido"+self.long_url[requested_item] + "</a>.</p></body></html>"
            else:
                self.long_url[requested_item] = "/"+ num
                self.short_url["/"+num] = requested_item
                num = num + 1
                htmlBody = "<html><body>" + "eres una pichume" +"</body></html>"
            
        return (httpCode, htmlBody)


if __name__ == "__main__":
    testWebApp = contentApp("localhost", 1234)
