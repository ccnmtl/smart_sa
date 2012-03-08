from django import template

register = template.Library()

class GetParticipantStatus(template.Node):
    def __init__(self,participant,obj,var_name=None):
        self.participant = template.Variable(participant)
        self.obj = template.Variable(obj)
        self.var_name = var_name

    def render(self,context):
        p = self.participant.resolve(context)
        o = self.obj.resolve(context)
        status = o.get_participant_status(p)
        if self.var_name:
            context[self.var_name] = status
            return ''
        else:
            return status

@register.tag('get_participant_status')
def get_participant_status(parser, token):
    participant = token.split_contents()[1:][0]
    obj = token.split_contents()[1:][1]
    var_name = None
    if len(token.split_contents()[1:]) > 2:
        # handle "as some_var"
        var_name = token.split_contents()[1:][3]
    return GetParticipantStatus(participant,obj,var_name)


        
