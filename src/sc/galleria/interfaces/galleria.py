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

class IGalleriaSettings(Interface):
    """
     Option informations: http://galleria.io/docs/1.2/options/
    """
    autoplay = schema.Bool(title=u"Auto Play.",
                           description=u"Sets Galleria to play slidehow when initialized.",
                           default=True)

    showInf = schema.Bool(title=u"Show informations",
                          description=u"Toggles the caption.",
                          default=True)

    transitions = schema.Choice(title=u"Transitions",
                          description=u"Defines what transition to use.",
                          default='fade',
                          vocabulary=transitions)

    transitionSpeed = schema.Int(title=u"Transition Speed", 
                                 description=u"Defines the speed of the transition.",
                                 default=400)

    lightbox = schema.Bool(title=u"Enabel lightbox",
                               default=False)

    image_width = schema.Int(title=u"Image width",
                             description=u"Manually set a gallery width.",
                             default=500)

    image_height = schema.Int(title=u"Image height",
                              description=u"Manually set a gallery height.",
                              default=500)

    showCounting = schema.Bool(title=u"Show counting",
                               description=u"Toggles the counter.",
                               default=True)

    debug = schema.Bool(title=u"Enable debug mode",
                        description=u"Set this to false to prevent debug messages.",
                        default=False)
