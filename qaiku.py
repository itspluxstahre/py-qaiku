# vim: ai ts=4 sts=4 et sw=4

"""
A python interface against qaiku.com (via JSON)

Requires:
    * Python 2.6 or later
    * HTTPLib2 
    * Json
    * Markdown
    * urllib

This is a library to work with the Qaiku API,
it will map everything to python objects to make
things easier when embedding this into other applications.

Basic Usage:
    from qaiku import Qaiku

    qc = Qaiku(api_key="your_uniqe_api_key", source="Your Application Name")
    message = qc.PostUpdate("Posting messages to qaiku with python is cool!")
    print message.id

Object Comparison:
    All objects have function like __eq__() and __ne__() to allow easy compares 
    between two objects.

    Ex: print User1 == User2

Object __init__:
    All objects except the main Qaiku object can be called in three diffrent
    ways to init them.

    1. As any other object:
        * MyMessage = QaikuMessage(id="312312asfa2" ... )
    
    2. With a valid json string:
        * MyMessage = QaikuMessage.fromJson("{id: "231231232" ... ")
    
    3. With a valid python dict()
        * MyMessage = QaikuMessage.fromDict(" ... )

Todo:
    * Fix a small "bug" with QaikuGeo (Floating points...)
    * Add markdown support.

License:
    Copyright (C) 2009 Mattias Stahre <mattias@plux.se>

    This program is free software; you can redistribute it and/or modify it
    under the terms of the GNU Lesser General Public License as published
    by the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    You should have received a copy of the GNU General Public License
    long with this program; if not-> write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

__AUTHOR__ = "Mattias Stahre <mattias@plux.se>"
__VERSION__ = "0.1"
__LIBNAME__ = "py-qaiku"
__MESSAGELIMIT__ = 139
__DATALIMIT__ = 240
__BASEAPIURL__ = "http://www.qaiku.com/api"

# Please leave USERAGENT alone.
# If you want to show off your application name
# use the source arg in Qaiku instead. :)
__USERAGENT__ = __LIBNAME__ + "/" + __VERSION__

import json
import urllib
import httplib2
import urllib2

class QaikuUser:
    """
    QaikuUser - A simple object to represent a single Qaiku user.

    The User object will always be returned when we are dealing
    with information about users.
    """

    def __init__(self,
                 id = None,
                 name = None,
                 screen_name = None,
                 location = None,
                 description = None,
                 profile_image_url = None,
                 url = None,
                 geo_enabled = None,
                 protected = None,
                 followers_count = None,
                 status = None,
                 languages = None,
                 created_at = None):
        """
        Init the user object, all variables are
        optional as we migt want to set these later.
        """

        self.id = id
        self.name = name
        self.screen_name = screen_name
        self.location = location
        self.description = description
        self.profile_image_url = profile_image_url
        self.url = url
        self.geo_enabled = geo_enabled
        self.protected = protected
        self.followers_count = followers_count
        self.status = status
        self.languages = languages
        self.created_at = created_at

    def __str__(self):
        """
        Converts the string to a printable string (JSON).
        """
        return self.asJsonString()

    def __ne__(self, other):
        """
        Checks if two user objects is not identical.

        Usage:
            if (User1 != User2):
                do_some_thing()

        Return:
            True if not identical.
            False if identical.
        """
        return not self.__eq__(other)

    def __eq__(self, other):
        """
        Checks if two user objects are identical.

        Usage:
            if (User1 == User2):
                do_some_thing()

        Return:
            True if identical.
            False if not.
        """
        if self.id == other.id and \
           self.name == other.name and \
           self.screen_name == other.screen_name and \
           self.location == other.location and \
           self.description == other.description and \
           self.profile_image_url == other.profile_image_url and \
           self.url == other.url and \
           self.geo_enabled == other.geo_enabled and \
           self.protected == other.protected and \
           self.followers_count == other.followers_count and \
           self.status == other.status and \
           self.languages == other.languages and \
           self.created_at == other.created_at:
            return True
        else:
            return False

    def asJsonString(self):
        """
        Dumps a QaikuUser object as a JsonString.

        Usage:
            print MyUser.asJson()

        Return:
            The object as a valid jsonstring.
        """
        return json.dumps(self.asDict(), sort_keys=True)

    def asDict(self):
        """
        Dumps a QaikuUser object as a DictObject.

        Usage:
            print MyUser.asDict()

        Return:
            A dict representation of the QaikuUser Object.
        """

        datadict = {}
        if self.id:
            datadict['id'] = self.id
        
        if self.name:
            datadict['name'] = self.name
        
        if self.screen_name:
            datadict['screen_name'] = self.screen_name
        
        if self.location:
            datadict['location'] = self.location
        
        if self.description:
            datadict['description'] = self.description
            
        if self.profile_image_url:
            datadict['profile_image_url'] = self.profile_image_url
            
        if self.url:
            datadict['url'] = self.url
            
        if self.geo_enabled:
            datadict['geo_enabled'] = self.geo_enabled
        
        if self.protected:
            datadict['protected'] = self.protected
            
        if self.followers_count:
            datadict['followers_count'] = self.followers_count

        if self.status:
            datadict['status'] = self.status
            
        if self.languages:
            datadtict['languages'] = self.languages
        
        if self.created_at:
            datadict['created_at'] = self.created_at
            
        return datadict

    @staticmethod
    def fromDict(datadict):
        """
        Creates a new QaikuUser object from a Dict Object.

        Usage:
            MyUser = QaikuUser.fromDict(YourUserDict)

        Return:
            A new QaikuUser object with the values from
            the provided dict.
        """
        if 'status' in datadict:
            status = QaikuMessage.fromDict(datadict['status'])
        else:
            status = None
            
        return QaikuUser(id=datadict.get('id', None),
                         name=datadict.get('name', None),
                         screen_name=datadict.get('screen_name', None),
                         location=datadict.get('location', None),
                         description=datadict.get('description', None),
                         profile_image_url=datadict.get('profile_image_url', None),
                         url=datadict.get('url', None),
                         geo_enabled=datadict.get('geo_enabled', None),
                         protected=datadict.get('protected', None),
                         followers_count=datadict.get('followers_count', None),
                         status=status,
                         languages=datadict.get('languages', None),
                         created_at=datadict.get('created_at', None)
                        )

    @staticmethod
    def fromJsonString(json_string):
        """
        Create a new QaikuUser object from a Json String.

        Usage:
            MyUser = QaikuUser.fromJsonString("your_valid_json_string))

        Return:
            A new QaikuUser object with the data from the Json String.
        """
        return QaikuUser.fromDict(json.loads(json_string))


class QaikuGeo:
    """
    A representation of a geo point.

    Usage:
        MyGeo = QaikuGeo(type="Point", coordinates=(323.32, 15.21))

    Return:
        A new QaikuGeo object.
    """

    def __init__(self, type=None, coordinates=None):
        self.type = type
        self.coordinates = coordinates

    def __str__(self):
        """Return as a JSON-string"""
        return self.asJsonString()

    def __eq__(self, other):
        if self.type == other.type and \
                        self.coordinates == other.coordinates:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def asDict(self):
        datadict = {}
        if self.type:
            datadict['type'] = self.type
            if self.coordinates:
                datadict['coordinates'] = coordinates

        return datadict

    def asJsonString(self):
        """Encode the userobject to a JSON string."""
        return json.dumps(self.asDict(), sort_keys=True)

    @staticmethod
    def fromDict(datadict):
        return QaikuGeo(type=datadict.get('Type', None), coordinates=datadict.get('coordinates', None))

    @staticmethod
    def fromJsonString(json_string):
        return QaikuGeo.fromDict(json.loads(json_string))

class QaikuMessage:
    """
    A representation of a Single Qaiku Message.

    Usage:
        MyMessage = QaikuMessage(id="314214...)

    Return:
        A new QaikuMessage object.
    """
    
    def __init__(self,
                 created_at = None,
                 id = None,
                 text = None,
                 html = None,
                 source = None,
                 lang = None,
                 data = None,
                 external_url = None,
                 truncated = None,
                 in_reply_to_status_id = None,
                 in_reply_to_user_id = None,
                 favorited = None,
                 geo = None,
                 user = None,
                 channel = None,
                 status=None):
        
        self.created_at = created_at
        self.id = id
        self.text = text
        self.html = html
        self.source = source
        self.lang = lang
        self.data = data
        self.external_url = external_url
        self.truncated = truncated
        self.in_reply_to_status_id = in_reply_to_status_id
        self.in_reply_to_user_id = in_reply_to_user_id
        self.favorited = favorited
        self.geo = geo
        self.user = user
        self.channel = channel
        self.status = status

    def __eq__(self, other):
        if self.created_at == other.created_at and \
           self.id == other.id and \
           self.text == other.text and \
           self.html == other.html and \
           self.source == other.source and \
           self.lang == other.lang and \
           self.data == other.data and \
           self.external_url == other.external_url and \
           self.truncated == other.truncated and \
           self.in_reply_to_status_id == other.in_reply_to_status_id and \
           self.in_reply_to_user_id == other.in_reply_to_user_id and \
           self.favorited == other.favorited and \
           self.geo == other.geo and \
           self.user == other.user and \
           self.channel == other.channel and \
           self.status == other.status:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.asJsonString()

    def asDict(self):
        datadict = {}
        if self.created_at:
            datadict['created_at'] = self.created_at
        if self.id:
            datadict['id'] = self.id
        if self.text:
            datadict['text'] = self.text
        if self.html:
            datadict['html'] = self.html
        if self.source:
            datadict['source'] = self.source
        if self.lang:
            datadict['lang'] = self.lang
        if self.data:
            datadict['data'] = self.data
        if self.truncated:
            datadict['truncated'] = self.truncated
        if self.in_reply_to_status_id:
            datadict['in_reply_to_status_id'] = self.in_reply_to_status_id
        if self.in_reply_to_user_id:
            datadict['in_reply_to_user_id'] = self.in_reply_to_user_id
        if self.favorited:
            datadict['favorited'] = self.favorited
        if self.geo:
            datadict['geo'] = self.geo.asDict()
        if self.user:
            datadict['user'] = self.user.asDict()
        if self.channel:
            datadict['channel'] = self.channel
        if self.status:
            datadict['status'] = self.status

        return datadict

    def asJsonString(self):
        return json.dumps(self.asDict(), sort_keys=True)

    @staticmethod
    def fromJsonString(json_string):
        return QaikuMessage.fromDict(json.loads(json_string))

    @staticmethod
    def fromDict(datadict):
        if 'user' in datadict:
            user = QaikuUser.fromDict(datadict['user'])
        else:
            user = None

        if 'geo' in datadict:
            geo = QaikuGeo.fromDict(datadict['geo'])
        else:
            geo = None

        return QaikuMessage(created_at=datadict.get('created_at', None),
                                        id=datadict.get('id', None),
                                        text=datadict.get('text', None),
                                        html=datadict.get('html', None),
                                        source=datadict.get('source', None),
                                        lang=datadict.get('lang', None),
                                        data=datadict.get('data', None),
                                        truncated=datadict.get('truncated', None),
                                        in_reply_to_status_id=datadict.get('in_reply_to_status_id', None),
                                        in_reply_to_user_id=datadict.get('in_reply_to_user_id', None),
                                        favorited=datadict.get('favorited', None),
                                        geo=geo,
                                        user=user,
                                        channel=datadict.get('channel', None),
                                        status=datadict.get('status', None)
                                        )

class Qaiku:
    """This is the object that you will use to communicate with qaiku.com"""

    def __init__(self, api_key, source=__LIBNAME__):
        """You will always use a apikey to communicate with qaiku.
         If you are embedding this lib into something you might want to provide
         your own sourcename."""

        self.api_key = api_key
        self.source = source


    def PostUpdate(self,
                   status,
                   lang="en",
                   in_reply_to_status_id=None,
                   external_url=None,
                   data = None,
                   channel=None):
        """
        Post a new status update.
        
        This will post an update to the logged in users timeline.
        
        Args:
            status: string The status message.
            lang: string Two character lang code ex: en,sv,fi
            in_repy_to_status_id: string If the message is a reply to a another message.
            external_url: string A external URL to link this item to.
            channel: string Post the message to a chennel instead of the main user stream.
                Note: If the message starts with #channel the message will be posted into that channel.

        Returns:
                A message object with the created message.
        """

        message = QaikuMessage()

        if in_reply_to_status_id:
            message.status = status
            message.in_reply_to_status_id = in_reply_to_status_id
        else:
            message.status = status[0:__MESSAGELIMIT__]

        message.lang = lang

        if external_url:
            message.external_url = external_url
        if data:
            message.data = data[0:__DATALIMIT__]
        if channel:
            message.channel = channel

        try:
            post_data = message.asDict()
            post_data['source'] = self.source
            post_data = urllib.urlencode(post_data)
            api_url = "http://www.qaiku.com/api/statuses/update.json?apikey=" + self.api_key
            h = httplib2.Http()
            headers = {'Content-type': 'application/x-www-form-urlencoded',
                       'User-Agent': 'py-qaiku 0.1'}
            resp,content = h.request(uri=api_url, method='POST', body=post_data, headers=headers)
        except httplib2.ServerNotFoundError:
            raise QaikuException(404, "Server not found")
            return None
        except httplib2.RedirectLimit:
            raise QaikuException(0, "Maximum redirects reached")
            return None
        except httplib2.RedirectMissingLocation:
            raise QaikuException(0, "A 3xx redirect response code was provided but no Location: header was provided to point to the new location.")
            return None
        except httplib2.RelativeURIError:
            raise QaikuException(0, "A relative, as opposed to an absolute URI was passed into request().")
            return None
        except httplib2.FailedToDecompressContent:
            raise QaikuException(0, "The headers claimed that the content of the response was compressed but the decompression algorithm applied to the content failed.")
            return None
        except httplib2.HttpLib2Error:
            raise QaikuException(0, "Something went wrong!")
            return None
        else:
            return QaikuMessage.fromJsonString(content)

    def ShowMessage(self, id):
        """
        Show a single message.

        Args:
            id: string The full id of the message.
            
        Returns:
                A message object with the message.
        """
        try:
            api_url = "http://www.qaiku.com/api/statuses/show/" + id + ".json?apikey=" + self.api_key
            h = httplib2.Http()
            headers = {'User-Agent': __USERAGENT__ }
            resp,content = h.request(uri=api_url, method='GET', headers=headers)
        except httplib2.ServerNotFoundError:
            raise QaikuException(404, "Server not found")
            return None
        except httplib2.RedirectLimit:
            raise QaikuException(0, "Maximum redirects reached")
            return None
        except httplib2.RedirectMissingLocation:
            raise QaikuException(0, "A 3xx redirect response code was provided but no Location: header was provided to point to the new location.")
            return None
        except httplib2.RelativeURIError:
            raise QaikuException(0, "A relative, as opposed to an absolute URI was passed into request().")
            return None
        except httplib2.FailedToDecompressContent:
            raise QaikuException(0, "The headers claimed that the content of the response was compressed but the decompression algorithm applied to the content failed.")
            return None
        except httplib2.HttpLib2Error:
            raise QaikuException(0, "Something went wrong!")
            return None
        else:
            return QaikuMessage.fromJsonString(content)

    def GetReplies(self, id):
        pass
        
    def GetRepliesByUrl(self, url)
        pass
        
    def GetFriendsTimeLine(self,
                           user_id=None,
                           screen_name=None,
                           since=None,
                           page=None,
                           lang=None):
        pass

    def GetUserTimeLine(self,
                        user_id=None,
                        screen_name=None,
                        since=None,
                        page=None,
                        lang=None):
        pass

    def GetChannelTimeLine(self,
                           since=None,
                           page=None,
                           lang=None):
        pass
    
    def GetPublicTimeLine(self,
                          since=None,
                          page=None,
                          lange=None):
        pass

    def GetMentions(self,
                    since=None,
                    page=None,
                    lang=None):
        pass

    def GetFriends(self,
                   user_id=None,
                   screen_name=None):
        pass

    def GetFollowers(self,
                     user_id=None,
                     screen_name=None):
        pass

    def Search(self,
               q,
               since=None,
               page=None,
               lang=None):
        pass
    def DestroyMessage(self, id):
        """
        Removes a message from qaiku
        
        TODO:
            Implement, broken at qaiku.com

        Returns:
                A message object with the deleted message.
        """
        return None

    def _HttpClient(self,
                    action,
                    id = None,
                    data=None):
        """
        The internal HTTP-client, forked out to make it easier to change
        the impleementation if it's neeed.
        """ 
                    
        try:
            h = httlib2.Http()
            if action == "PostUpdate":
                api_url = __BASEAPIURL__ + "/statuses/update.json?apikey=" + self.api_key
                        
                headers = {'User-Agent': __USERAGENT__,
                           'Content-Type': 'application/x-www-form-urlencoded'}
            
                method = 'POST'
                
                if data:
                    post_data = urllib.urlencode(data)
                else:
                    raise QaikuHttpException(0, "You must provide data to post.")
                    
            if action == "ShowMessage":
                api_url = __BASEAPIURL__ + "/statuses/show/" + id + ".json?apikey=" + self.api_key
                headers = {'User-Agent': __USERAGENT__}
                method = 'GET'
            
            if action == "GetReplies":
                pass
            
            if action == "GetRepliesByUrl":
                pass
                
             if action == "GetFriendsTimeLine":
                pass
                
             if action == "GetUserTimeLine":
                pass
                
             if action == "GetChannelTimeLine":
                pass
                
             if action == "GetPublicTimeline":
                pass
                
             if action == "GetMentions":
                pass
                
             if action == "GetFriends":
                pass
             
             if action == "GetFollowers":
                pass
                
             if action == "Search":
                pass
             
            
            resp,content = h.request(uri=api_url, method=method, body=post_data, headers=headers)
        except httplib2.ServerNotFoundError:
            raise QaikuException(404, "Server not found")
            return None
        except httplib2.RedirectLimit:
            raise QaikuException(0, "Maximum redirects reached")
            return None
        except httplib2.RedirectMissingLocation:
            raise QaikuException(0, "A 3xx redirect response code was provided but no Location: header was provided to point to the new location.")
            return None
        except httplib2.RelativeURIError:
            raise QaikuException(0, "A relative, as opposed to an absolute URI was passed into request().")
            return None
        except httplib2.FailedToDecompressContent:
            raise QaikuException(0, "The headers claimed that the content of the response was compressed but the decompression algorithm applied to the content failed.")
            return None
        except httplib2.HttpLib2Error:
            raise QaikuException(0, "Something went wrong!")
            return None
        else:
        

class QaikuHttpException(Exception):

    def __init__(self, code, message=None):
        self.code = code
        self.message = message

