from django.template import Library, Node, TemplateSyntaxError, Variable

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


@register.tag
def day(parser, token):
    try:
        tag_name, day_span, day_number = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError('Wrong arguments!')

    return DayNode(day_span, day_number)


class DayNode(Node):

    def __init__(self, day_span, day_number):
        self.day_span = self._get_var(day_span)
        self.day_number = self._get_var(day_number)

    def _get_var(self, var):
        try:
            if var[0] == var[1] and var[0] in ('"', "'"):
                return var[1,-1]
        except IndexError:
            pass

        return Variable(var)

    def render(self, context):
        if isinstance(self.day_span, Variable):
            day_span = self.day_span.resolve(context)
        else:
            day_span = self.day_span

        if isinstance(self.day_number, Variable):
            day_number = self.day_number.resolve(context)
        else:
            day_number = self.day_number

        value = '|{: ^{}}'.format(day_number, day_span)
        return value.replace(' ', '&nbsp;')
