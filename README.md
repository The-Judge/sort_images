# About this project

The scope of these scripts is to help organizing a collection of photos from various sources.  
I have tons of photos from various sources. Including those ...

* I made with my smartphone, myself
* which were token with a good SLR camera
* others took with their whatever-devices, sending these by WhatsApp, Telegram or EMail
* I found online in any gallery, downloading them locally

In a modern family or partnership, multiply this mess by the count of persons involved, since nearly everybody has this (or even worse) digital mess. And often the one has photos the other has not or in a better quality or resolution.

These days, some of them are also (more or less) automatically synced to various cloud services, including [Google Photos][gphoto]/[Google Drive][gdrive], [Dropbox], ...  
But since I've already made some bad experiences in the past with services, reaching end of business or changing their reliability or the way they modify your pictures, silently. Two examples on this:

# The issues

## Cloud storage and communication services for photos

Nowadays, most of us use one or more cloud services to sync their photos to, for sure. So do I - but I also experienced issues with this already:

### Flickr

Not only had [Flickr] some serious security issues [between 2013 and 2017](https://thehackernews.com/2016/10/yahoo-email-hacking.html), they also found themselfes in a situation in which [they had to disable mobile photo uploads due to patent issues in Germany](https://www.flickr.com/help/forum/en-us/72157668329100100/) and not too long ago, I was hit by a default setting I was unaware of, to scale down images to a maximum; which was not what I wanted.

### Google Photos / Google Drive

The main issue with [Google Photos][gphoto]/[Google Drive][gdrive] is that I do not fully get it straight up until today:  
... so - you have somewhat of unlimited amount of storage for *some* pictures and videos, until they have no higher resolution than 16 MP for photos or 1.080p (HD) for video. For pictures, that should be something between 4536×3024 (14MP) and 4992×3328 (16,7 MP).

According to [the official help](https://support.google.com/photos/answer/6156103?hl=en) on [Photos][gphoto]/[Drive][gdrive] interaction, you can configure [Google Photos][gphoto] at the [settings][photo_settings] to sync photos, which you put into [Drive][gdrive], over to [Google Photos][gphoto], to see them there, but that still seems to drain your [Drive][gdrive] storage. So: How to keep track on what's comming from where and which one is draining your storage capacity and what not?

Also, if you forget to configure the quality used for uploads in any of many possible places (in the [settings of photos][photo_settings], in the [Fotos app](https://play.google.com/store/apps/details?id=com.google.android.apps.photos) upload settings, in your [Drive][gdrive] computer application, ...) you end up with a scaled version.

### WhatsApp

Being one of the most commonly used communication services in the world today, it is often used to exchange photos between users and groups.  
Did you ever compare the photos you receive by [WhatsApp] with the original ones on the senders device? You will find that they not only are scaled down to a way lower resolution by most senders, but also some mobile friendly lossy low bandwidth optimizations are applied to them.  
For important photos, this surely is sommething most want to prevent.

### General issues with external services

Even if there are no issues currently, cloud services are subject to be changed all the time. There is no gurantee that a service, which you evaluated and setup optimal in your syncing workflow will continue to work like that for the next years (or even decades).  
Also, there is no guarantee at all that a company, which runs a specific service, will be arround in a few years, still. If you do not believe this, take these two examples into account:

#### MySpace

Do you even remember it? ;)
Was once one of the first social networks (before Facebook) and for sure the biggest one.

#### Yahoo

* 1998: Yahoo was offered to buy Google for $1 million and refused.
* 2002: Yahoo realized that may has been a bad decision and offered $3 **b**illion. Google demanded $5 billion and Yahoo refused again.
* 2008: Microsoft offered to buy Yahoo for $40 billion dollars.
* 2016: Yahoo was sold to Verizon for $4.6 billion

If you remember: Formerly mentioned [Flickr] is one of Yahoo's services, too. So: How safe are your valuable memories when forecasting the next 10, 20 or even 80 years?

## Self-Storage (USB, Fileserver, NAS, ...)

To protect your really important photos from being lost, stolen, exposed, altered, messed up, ..., some have their own storage solution within the trustworthy walls of their own home, where everything is under your control and responsibility (RAID levels do not protect against fire or burglary).

Often, when you copy data from all the formerly mentioned sources to these Terrabyte sized storage solutions, most tent to copy **everything**; no matter if that is the 100th copy of an image or if they only differ in their resolution. *Save now, sort later* is an often applied pattern. But then, when you find yourself stuck in a mess of 500 GB, unsorted photo collections, you notice that it would have been a good idea to take some more care of sorting in the first place.

# The solution(s)

[sort_images] to the rescue! This is where the tools in this repo come in: They aim at helping you with this task in several ways. Each are documented in the following sections.


[gphoto]: https://photos.google.com/
[gdrive]: https://drive.google.com/
[Dropbox]: https://www.dropbox.com/
[photo_settings]: https://photos.google.com/settings
[Flickr]: https://www.flickr.com/
[WhatsApp]: https://www.whatsapp.com/
[sort_images]: https://github.com/The-Judge/sort_images
