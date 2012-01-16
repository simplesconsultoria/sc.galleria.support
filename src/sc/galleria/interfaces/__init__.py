from galleria import IGalleriaLayer
from galleria import IGalleriaSettings
from galleria import IGalleria 

# dependencies
# Thanks: collective.gallery
try:
    #plone4
    from plone.app.folder.folder import IATUnifiedFolder as IFolder
    from Products.ATContentTypes.interfaces.link import IATLink as ILink
    from Products.ATContentTypes.interfaces.topic import IATTopic as ITopic
    from Products.ATContentTypes.interfaces.image import IATImage as IImage
    from Products.ZCatalog.interfaces import ICatalogBrain
except ImportError, e:
    from collective.gallery import logger
    logger.info('BBB: switch to plone3 %s'%e)
    #plone3
    from Products.ATContentTypes.interface import IATFolder as IFolder
    from Products.ATContentTypes.interface import IATLink   as ILink
    from Products.ATContentTypes.interface import IATTopic  as ITopic
    from Products.ATContentTypes.interface import IATImage  as IImage

    class ICatalogBrain(interface.Interface):
        pass
