from zope.interface import Interface
from zope import schema

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from sc.galleria import MessageFactory as _

from plone.app.imaging.utils import getAllowedSizes

try:
    from Products.CMFPlone.migrations import v3_0
except ImportError:
    HAS_PLONE30 = False
else:
    HAS_PLONE30 = True
   
try:
    from plone.app.upgrade import v40
    HAS_PLONE4 = True
except:
    HAS_PLONE4 = False


transitionsvoc = SimpleVocabulary(
    [SimpleTerm(value='fade', title=_(u'Fade')),
     SimpleTerm(value='flash', title=_(u'Flash')),
     SimpleTerm(value='pulse', title=_(u'Pulse')),
     SimpleTerm(value='slide', title=_(u'Slide')),
     SimpleTerm(value='fadeslide', title=_(u'FadeSlide')), ]
    )

thumbnailsvoc = SimpleVocabulary(
    [SimpleTerm(value='show', title=_(u"Show thumbnails")),
     SimpleTerm(value='empty', title=_(u"Don't show thumbnails")),]
    )

if HAS_PLONE30:
   selectorPlone = u'#content'
elif HAS_PLONE4:
   selectorPlone = u'#content-core'


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

    gallery_width = schema.Int(title=u"Gallery width",
                             description=u"Manually set a gallery width.",
                             default=500,
                             required=True,)

    gallery_height = schema.Int(title=u"Gallery height",
                              description=u"Manually set a gallery height.",
                              default=500,
                              required=True,)

    imagePosition = schema.TextLine(title=u"Image css position",
                                    description=u"Eg. 'top right' or '20% 100%'",
                                    default=u'center',
                                    required=True,)

    lightbox = schema.Bool(title=u"Enable lightbox",
                               default=False,
                               required=True,)


    showCounting = schema.Bool(title=u"Show counting",
                               description=u"Toggles the counter.",
                               default=True,
                               required=True,)

    transitions = schema.Choice(title=u"Transitions",
                          description=u"Defines what transition to use.",
                          default=u'fade',
                          vocabulary=transitionsvoc,
                          required=True,)

    transitionSpeed = schema.Int(title=u"Transition Speed", 
                                 description=u"Defines the speed of the transition.",
                                 default=400,
                                 required=True,)

    showimagenav = schema.Bool(title=u"show image navigation",
                               description=u"toggles the image navigation arrows.",
                               default=True,
                               required=True,)

    swipe = schema.Bool(title=u"swipe",
                               description=u"Enables a swipe movement for flicking through images on touch devices.",
                               default=True,
                               required=True,)

    selector = schema.TextLine(title=u"Selector jQuery",
                                    description=u"Eg. '#content-core' or '#content' or '.galleria'. Do not change if you do not know what I mean.",
                                    default=selectorPlone,
                                    required=True,)

    thumbnails = schema.Choice(title=u"Show Thumbnails",
                               description=u"Sets the creation of thumbnails",
                               default=u'show',
                               vocabulary=thumbnailsvoc,
                               required=True,)

    debug = schema.Bool(title=u"Enable debug mode",
                        description=u"Set this to false to prevent debug messages.",
                        default=False,
                        required=True,)
