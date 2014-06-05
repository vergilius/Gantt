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


def _get_var(var):
    try:
        if var[0] == var[1] and var[0] in ('"', "'"):
            return var[1,-1]
    except IndexError:
        pass

    return Variable(var)


class DayNode(Node):

    def __init__(self, day_span, day_number):
        self.day_span = _get_var(day_span)
        self.day_number = _get_var(day_number)

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


@register.tag
def progress(parser, token):
    try:
        tag_name, prog = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError('Wrong arguments!')

    nodelist = parser.parse(('end{}'.format(tag_name),))
    parser.delete_first_token()
    return ProgressNode(nodelist, prog)


class ProgressNode(Node):

    def __init__(self, nodelist, prog):
        self.nodelist = nodelist
        self.prog = _get_var(prog)

    def render(self, context):
        output = self.nodelist.render(context)

        if isinstance(self.prog, Variable):
            prog = self.prog.resolve(context)
        else:
            prog = prog

        prog = min(max(prog, 0), 100)
        out_len = len(output)
        done = int(round(prog / 100.0 * out_len))

        if prog < 100 and done == out_len:
            done = done - 1

        result = '<span class="bg-success">' + output[:done] + '</span>' + output[done:]

        return result
