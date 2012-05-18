===================
sc.galleria.support
===================

.. contents:: Table of Contents
   :depth: 2


Overview
--------

**sc.galleria.support** is a Plone package (add-on) providing simple gallery integration for Plone.

Using in a Plone Site
----------------------

Step 1: Activate it
^^^^^^^^^^^^^^^^^^^^

Go to the 'Site Setup' page in the Plone interface and click on the
'Add/Remove Products' link.

Choose the product **sc.galleria.support** (check checkbox at its left side)
and click the 'Activate' button.

Step 2: Setting preferences
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In 'Site setup' below on 'Add-on Configuration' click on 'Galleria' option. In
this section you can see several options wich are categorized in different
types. Each type is visualized in a tab. You have options for 'Default',
'Flickr Plugin', 'Picasa Plugin' and 'History Plugin'. To know how to setup this
preferences in a way to go better to your needs see `Functionality`_ section.

Step 3: Seeing it in action
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Galleria will be rendered through a set of the display action in a container
content type. For example, if you have a folder named "My folder" and you are
standing there, click on "Display" (you need permissions for the edit bar) and then in "Galleria".
Of course, this will only have an effect if you have images inside that folder. If you do, you will
see the images render with the Galleria plugin.

For the case that you want to fetch pictures located in flickr or picasa see
`Flickr & Picasa Plugins`_. To activate Galleria in the Link just follow
the same procedure with the display action.

Functionality
--------------

The next explanations about different options must be applied in the control panel of Galleria
add-on. See `Step 2: Setting preferences`_.

Default options
^^^^^^^^^^^^^^^

In this section you have all the basic options to set how the layout of your
galleria will look like.


**Auto play:**
    This will start playing the slideshow with 5 seconds interval.

**Show informations:**
    Displays the caption.

**Gallery width:**
    You can use this option to set a gallery width manually. Default is 500 px.

**Gallery height:**
    You can use this option to set a gallery height manually. Default is 500 px.

**Image css position:**
    Positions the main image inside the stage container. Works like the CSS background-position 
    property, f.ex ‘top right’ or ‘20% 100%’. You can use keywords, percents or pixels. The first
    value is the horizontal position and the second is the vertical.

     - Read more about positioning at http://www.w3.org/TR/REC-CSS1/#background-position

**Enable lightbox:**
    This option acts as a helper for attaching a lightbox when the user clicks on an image. If you
    have a link defined for the image, the link will take precedence.

**Show counting:**
    Displays the counter.

**Transitions:**
    The transition that is used when displaying the images. There are different transitions in Galleria.

    Flavors are:
         - *fade* - crossfade betweens images.
         - *flash* - fades into background color between images.
         - *pulse* - quickly removes the image into background color, then fades the next image.
         - *slide* - slides the images depending on image position.
         - *fadeslide* - fade between images and slide slightly at the same time.

**Transition Speed:**
    The milliseconds used in the animation when applying the transition. The higher number, the slower transition.

**Wait:**
    Sets how long Galleria should wait when trying to extract measurements, before throwing an error. Default is 5000

**Show image navigation:**
    Displays the image navigation (next/prev arrows).

**Swipe:**
    Enables a swipe movement for flicking through images on touch devices.

**Selector jQuery:**
    Eg. '#content-core' or '#content' or '.galleria'. Do not change if you do not know what I mean.

**Show Thumbnails:**
    Sets the creation of thumbnails.

**Enable debug mode:**
    This option is for turning debug on/off. By default, Galleria displays errors by printing them out in the
    gallery container and sometimes throw exceptions. For deployment you can turn debug off to generate a more generic
    error message if a fatal error is raised.


YouTube, Vimeo & DailyMotion supported
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To use this supports you have to create a 'Link' content type and in the 'url'
field set the movie url.

 - **YouTube:** Sets options for the YouTube player.

 - **Vimeo:** Sets options for the Vimeo player.

 - **DailyMotion** Adds player options for the Daliymotion video player.

Flickr & Picasa Plugins
^^^^^^^^^^^^^^^^^^^^^^^

To use this plugins you have to create a 'Link' content type and in the 'url'
field set the galleria url that looks something like:

 - **Flickr:** 'http://www.flickr.com/photos/user_id/sets/galleria_id/'

 - **Picasa:** 'https://picasaweb.google.com/user_id/galleria_id'

**Enable plugin:** activate this function.

**Maximum number of photos:** you can set the maximum of photos to show.

**Show description:** Fetch the description. The plugin fetches the title per
default.

History Plugin
^^^^^^^^^^^^^^

The Galleria History plugin is a simple extension to create Galleria add hash
tags for permalinks and back button functionality enabled. This is useful on
fullscreen views and other use cases. The plugin simply adds a #/[id] hash to
the URL and then applies the necessary code for all browsers to enable the back
button. It also makes permalinks possible by simply bookmarking f.ex
http://mygalleria.com/#/4 and the user will be shown the 5th image in the
gallery (index starts at 0).

Browser support includes Firefox 2+, IE6+, Ipad, Opera and Chrome.

You enable it with the **Enable history plugin** option.
