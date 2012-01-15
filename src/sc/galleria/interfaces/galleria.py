from zope.interface import Interface
from zope import schema

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from sc.galleria import MessageFactory as _


transitions = SimpleVocabulary(
    [SimpleTerm(value='fade', title=_(u'fade')),
     SimpleTerm(value='flash', title=_(u'flash')),
     SimpleTerm(value='pulse', title=_(u'pulse')),
     SimpleTerm(value='slide', title=_(u'slide')),
     SimpleTerm(value='fadeslide', title=_(u'fadeslide')), ]
    )

class IGalleriaLayer(Interface):
    """
    Marker Default browser layer this product.
    """

class IGalleria(Interface):
    """
    """

    def __init__(self, context, request,*args,**kwargs):
        """ """

    def settings(self):
        """ """

    def get_theme(self):
        """ """

    def portal_url(self):
        """ """


class IGalleriaSettings(Interface):
    """
     Option informations: http://galleria.io/docs/1.2/options/
    """
    autoplay = schema.Bool(title=u"Auto Play.",
                           description=u"Sets Galleria to play slidehow when initialized.",
                           default=True,
                           required=True,)

    showInf = schema.Bool(title=u"Show informations",
                          description=u"Toggles the caption.",
                          default=True,
                          required=True,)

    image_width = schema.Int(title=u"Image width",
                             description=u"Manually set a gallery width.",
                             default=500,
                             required=True,)

    image_height = schema.Int(title=u"Image height",
                              description=u"Manually set a gallery height.",
                              default=500,
                              required=True,)

    imagePosition = schema.TextLine(title=u"Image css position",
                                    description="Eg. 'top right' or '20% 100%'",
                                    default='center',
                                    required=True,)

    lightbox = schema.Bool(title=u"Enabel lightbox",
                               default=False,
                               required=True,)


    showCounting = schema.Bool(title=u"Show counting",
                               description=u"Toggles the counter.",
                               default=True,
                               required=True,)

    transitions = schema.Choice(title=u"Transitions",
                          description=u"Defines what transition to use.",
                          default='fade',
                          vocabulary=transitions,
                          required=True,)

    transitionSpeed = schema.Int(title=u"Transition Speed", 
                                 description=u"Defines the speed of the transition.",
                                 default=400,
                                 required=True,)

    showimagenav = schema.bool(title=u"show image navigation",
                               description=u"toggles the image navigation arrows.",
                               default=True,
                               required=True,)

    swipe = schema.bool(title=u"swipe",
                               description=u"Enables a swipe movement for flicking through images on touch devices.",
                               default=True,
                               required=True,)

    debug = schema.Bool(title=u"Enable debug mode",
                        description=u"Set this to false to prevent debug messages.",
                        default=False,
                        required=True,)
