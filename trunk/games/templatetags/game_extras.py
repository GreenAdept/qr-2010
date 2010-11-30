from django import template

from qr import settings

register = template.Library()

@register.tag
def include_cat(parser, token):
    """ This tag is similar to the {% include %} tag,
        except instead of just taking a single string argument,
        it takes any number of sting and/or variable arguments.
        Strings should be including in quotations, variables should
        be values that will be converted to strings using str().
        The given arguments are concatenated, and the resulting
        string is used as the template name that is included.
    """
    try:
        strings = token.split_contents()
        tag_name = strings.pop(0)
        if (len(strings) < 1):
            raise ValueError
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires multiple arguments" % token.contents.split()[0]

    # go through the list of arguments,
    # converting any un-quoted strings to variables
    data = []
    for s in strings:
        if (s[0] == s[-1] and s[0] in ('"', "'")):
            data.append(s[1:-1])
        else:
            data.append(template.Variable(s))

    return IncludeCatNode(data)

class IncludeCatNode(template.Node):
    def __init__(self, data_list):
        ''' data_list should be a list of strings and/or Variables '''
        self.data = data_list

    def render(self, context):
        try:
            name = ''
            for d in self.data:
                if (isinstance(d, template.Variable)):
                    name += d.resolve(context)
                else:
                    name += d
            t = template.loader.get_template(name)
            return t.render(context)
        except:
            if settings.TEMPLATE_DEBUG:
                raise
            return ''

