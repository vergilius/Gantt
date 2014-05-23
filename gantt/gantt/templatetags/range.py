from django.template import Library, Node

register = Library()


@register.filter
def get_range(value):
    return range(value)


@register.filter
def inc(value):
    return value + 1


@register.tag
def nowhite(parser, token):
    nodelist = parser.parse(('endnowhite',))
    parser.delete_first_token()
    return NoWhiteNode(nodelist)


class NoWhiteNode(Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        return output.replace(' ', '').replace('\n', '')
