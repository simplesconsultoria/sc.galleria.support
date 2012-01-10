===============
sc.galleria
===============

.. contents:: Table of Contents
   :depth: 2


Overview
--------

**sc.galleria** is a Plone package (add-on) providing simple gallery integration for Plone.

Requirements
------------

    - Plone 4.1.x (http://plone.org/products/plone)
    - Plone 4.0.x (http://plone.org/products/plone)
    - Plone 3.3.x (http://plone.org/products/plone)

Installation
------------

To enable this product, on a buildout based installation:

    1. Edit your buildout.cfg and add ``sc.galleria``
       to the list of eggs to install ::

        [buildout]
        ...
        eggs = 
            sc.galleria

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

Choose the product **sc.galleria** (check checkbox at its left side)
and click the 'Activate' button.


Uninstall
-------------

Go to the 'Site Setup' page in the Plone interface and click on the
'Add/Remove Products' link.

Choose the product **sc.galleria**, which should be under *Activated
add-ons*, (check checkbox at its left side) and click the 'Deactivate' button.

.. note:: You may have to empty your browser cache and save your resource 
          registries in order to see the effects of the product installation.

Credits
-------
    
    * Cleber Santos (cleber at simplesconsultoria dot com dot br) - Idea and 
      implementation.
