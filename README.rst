===============
sc.galleria.support
===============

.. contents:: Table of Contents
   :depth: 2


Overview
--------

**sc.galleria.support** is a Plone package (add-on) providing simple gallery integration for Plone.

Requirements
------------

    - Plone 4.1.x (http://plone.org/products/plone)
    - Plone 4.0.x (http://plone.org/products/plone)
    - Plone 3.3.x (http://plone.org/products/plone)

Installation
------------

To enable this product, on a buildout based installation:

    1. Edit your buildout.cfg and add ``sc.galleria.support``
       to the list of eggs to install ::

        [buildout]

        #If Plone 3.3.x, uncomment this line
        #extends =
        #    http://good-py.appspot.com/release/plone.app.registry/1.0b2?plone=3.3.6

        ...
        eggs = 
            sc.galleria.support



.. note:: Since Plone 3.3 is not is necessary to explictly inform 
          plone.recipe.zope2instance recipe to install the ZCML slug

After updating the configuration you need to run the ''bin/buildout'',
which will take care of updating your system.

Using in a Plone Site
----------------------

Step 1: Activate it
^^^^^^^^^^^^^^^^^^^^

Go to the 'Site Setup' page in the Plone interface and click on the
'Add/Remove Products' link.

Choose the product **sc.galleria.support** (check checkbox at its left side)
and click the 'Activate' button.


Uninstall
-------------

Go to the 'Site Setup' page in the Plone interface and click on the
'Add/Remove Products' link.

Choose the product **sc.galleria.support**, which should be under *Activated
add-ons*, (check checkbox at its left side) and click the 'Deactivate' button.

.. note:: You may have to empty your browser cache and save your resource 
          registries in order to see the effects of the product installation.

Credits
-------
    
    * Cleber Santos (cleber at simplesconsultoria dot com dot br) - Idea and 
      implementation.

    * Aino (http://galleria.aino.se) - JavaScript galleria
