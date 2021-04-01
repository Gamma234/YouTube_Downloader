
from pytube import YouTube, Playlist
import ffmpeg
import re
import os
import shutil

class URL_Information() :

    def __init__( self, url ) :

        self.url_info_dict = {
            'url' :         url,   ## ( str )
            'yt' :          None,  ## ( YouTube )
            'title' :       None,  ## | str
            'views' :       None,  ## | int 
            'length' :      None,  ## | int
            'rating' :      None,  ## | float
            'captions' :    None,  ## | { code : caption, ... } ( str : caption )
            'streams' :     None,  ## | { itag : stream, ... } ( int : stream )
            'only audio' :  None,  ## | { itag : stream, ... } ( int : stream )
            'only video' :  None,  ## | { itag : stream, ... } ( int : stream )
            'progressive' : None,  ## | { itag : stream, ... } ( int : stream )
            'information' : ''     ## ( str )
        }

        self.stream_dict = ['streams', 'only audio', 'only video', 'progressive']

    def get_streams_itag( self, target_key=None ) :

        try :
            stream_box = None

            if target_key != None and target_key in self.stream_dict :
                stream_box = [target_key]
            else :
                stream_box = ( ['streams'] if self.url_info_dict['streams'] != None
                                else ['only audio','only video','progressive'] )

            ret_itag = [] ## [int, int, ...]

            for stream_name in stream_box :
                if self.url_info_dict[stream_name] != None :
                    for key in self.url_info_dict[stream_name].keys() :
                        ret_itag.append( key )

            if len( ret_itag ) != 0 :
                return ret_itag
            else :
                return []
        except Exception as e :
            raise e

    def get_captions_code( self ) :

        try :
            if self.url_info_dict['captions'] != None :

                ret_code = [] ## [str, str, ...]

                for key in self.url_info_dict['captions'].keys() :
                    ret_code.append( key )

                return ret_code
            else :
                return []
        except Exception as e :
            raise e

    def get_stream_by_itag( self, itag ) :

        try :
            return self.url_info_dict['yt'].streams.get_by_itag( itag )
        except Exception as e :
            raise e

    def get_caption_by_code( self, code ) :

        try :
           return self.url_info_dict['yt'].captions.get_by_language_code( code )
        except Exception as e :
            raise e

    def __getitem__( self, key ):

        try :
            return self.url_info_dict[key]
        except Exception as e :
            raise e

    def __setitem__( self, key, value ):

        try :
            if key in self.url_info_dict.keys() :
                self.url_info_dict[key] = value
            else :
                raise Exception( 'Key error !' )
        except Exception as e :
            raise e

    def __repr__( self ) :

        try :
            return self.url_info_dict['information']
        except Exception as e :
            raise e

class YouTube_Downloader() :

    def __init__( self ) :
        pass

    @staticmethod
    def get_url_information( url, show_dict={}, show_default=False ) :

        ## show_dict
        ##
        ## { 
        ##   'show details' :     True | False,
        ##   'show captions' :    True | False,
        ##   'show streams' :     True | False,
        ##   'only audio' :       True | False,
        ##   'only video' :       True | False,
        ##   'show progressive' : True | False
        ## }

        for key in ['show details', 'show captions', 'show streams', 'only audio', 'only video', 'show progressive'] :
            if not ( key in show_dict.keys() ) :
                show_dict[key] = show_default

        url_info = URL_Information( url=url )

        try :
            url_info['yt'] = YouTube( url )

            if show_dict['show details'] : ## Showing details
                
                url_info['information'] = ( url_info['information'] + '------details--------------------\n' +
                                            'Title: ' + url_info['yt'].title + '\n' +
                                            'Number of views: ' + str( url_info['yt'].views ) + '\n' +
                                            'Length of video: ' + str( url_info['yt'].length ) + '\n' +
                                            'Rating of video: ' + str( url_info['yt'].rating ) + '\n' +
                                            '---------------------------------\n\n' )
                
                url_info['title'] = url_info['yt'].title
                url_info['views'] = url_info['yt'].views
                url_info['length'] = url_info['yt'].length
                url_info['rating'] = url_info['yt'].rating

            if show_dict['show captions'] : ## printing all Subtitle/Caption
                
                url_info['captions'] = {}

                url_info['information'] = url_info['information'] + '------captions-------------------\n'
                for cap in url_info['yt'].captions.all() :
                    url_info['information'] = url_info['information'] + str( cap ) + '\n'
                    url_info['captions'][cap.code] = cap
                url_info['information'] = url_info['information'] + '---------------------------------\n\n'

            if show_dict['show streams'] : ## printing all the available streams
                
                url_info['streams'] = {}

                url_info['information'] = url_info['information'] + '------streams--------------------\n'
                for strm in url_info['yt'].streams :
                    url_info['information'] = url_info['information'] + str( strm ) + '\n'
                    url_info['streams'][strm.itag] = strm
                url_info['information'] = url_info['information'] + '---------------------------------\n\n'
                
            if show_dict['only audio'] : ## filter out audio-only streams
                
                url_info['only audio'] = {}

                url_info['information'] = url_info['information'] + '------streams (only_audio)-------\n'
                for strm in url_info['yt'].streams.filter( only_audio=True ) :
                    url_info['information'] = url_info['information'] + str( strm ) + '\n'
                    url_info['only audio'][strm.itag] = strm
                url_info['information'] = url_info['information'] + '---------------------------------\n\n'

            if show_dict['only video'] : ## filter out video-only streams
                
                url_info['only video'] = {}

                url_info['information'] = url_info['information'] + '------streams (only_video)-------\n'
                for strm in url_info['yt'].streams.filter (only_video=True ) :
                    url_info['information'] = url_info['information'] + str( strm ) + '\n'
                    url_info['only video'][strm.itag] = strm
                url_info['information'] = url_info['information'] + '---------------------------------\n\n'

            if show_dict['show progressive'] : ## filter out progressive streams
                
                url_info['progressive'] = {}

                url_info['information'] = url_info['information'] + '------streams (progressive)------\n'
                for strm in url_info['yt'].streams.filter( progressive=True ) :
                    url_info['information'] = url_info['information'] + str( strm ) + '\n'
                    url_info['progressive'][strm.itag] = strm
                url_info['information'] = url_info['information'] + '---------------------------------\n\n'

            return url_info
        except Exception as e :
            raise e

    @staticmethod
    def download_stream( strm, save_path=None, download=True ) :

        try :
            if download :
                strm.download( save_path ) if save_path != None else strm.download()
        except Exception as e :
            raise e

    @staticmethod
    def download_caption( cap, title='caption', save_path=None, download=True,
                          title_adjust='[\\\/:*?"<>|\[\]\(\)\【\】]' ) :

        try :
            if download :
                cap = cap.generate_srt_captions() ## convert to the srt format

                if title_adjust != None :
                    title = re.sub( title_adjust, '_', title )

                caption_file = open( ( ( title + '.srt' ) if ( save_path == None ) 
                                       else ( save_path + '\\' + title + '.srt' ) ),
                                     'w', encoding='utf-8' )

                caption_file.write( cap )
                caption_file.close()
        except Exception as e :
            raise e

    @staticmethod
    def get_stream_by_filter( url, filter_dict={ 'highest' : True }, key_default=None ) :

        ## filter_dict
        ##
        ## {
        ##   'itag' :        None | int
        ##   'highest' :     None | True | False
        ##   'type' :        None | 'video' | 'audio'
        ##   'subtype' :     None | 'mp4' | ...
        ##   'res' :         None | '1080p' | '720p' | ...
        ##   'abr' :         None | '128kbps' | '50kbps' | ...        
        ##   'only_audio' :  None | True | False
        ##   'only_video' :  None | True | False
        ##   'progressive' : None | True | False
        ## }

        for key in ['itag', 'highest', 'type', 'subtype', 'res',
                    'abr', 'only_audio', 'only_video', 'progressive'] :
            if not ( key in filter_dict.keys() ) :
                filter_dict[key] = key_default

        try :
            yt = YouTube( url )

            if filter_dict['itag'] != None :
                return yt.streams.get_by_itag( filter_dict['itag'] )
            elif ( filter_dict['highest'] == True ) or ( all( v == None for v in filter_dict.values() ) ) :
                return yt.streams.filter( progressive=True ).get_highest_resolution()
            else :
                return yt.streams.filter( type = filter_dict['type'],
                                          subtype = filter_dict['subtype'],
                                          res = filter_dict['res'],
                                          abr = filter_dict['abr'],
                                          only_audio = filter_dict['only_audio'],
                                          only_video = filter_dict['only_video'],
                                          progressive = filter_dict['progressive'] )[0]
        except Exception as e :
            raise e

    @staticmethod
    def get_caption_by_code( url, code ) :

        try :
            return YouTube( url ).captions.get_by_language_code( code )
        except Exception as e :
            raise e

    @staticmethod
    def get_playlist_urls( playlist_url ) :
        
        try :
            playlist = Playlist( playlist_url )
            ret_list = []

            ## this fixes the empty playlist.videos list
            playlist._video_regex = re.compile( r"\"url\":\"(/watch\?v=[\w-]*)" )

            for url in playlist.video_urls :
                ret_list.append( url )
            
            return ret_list
        except Exception as e :
            raise e

    @staticmethod
    def create_ip_file( playlist_url, save_path=None, file_name='ip_file.txt' ) :

        try :
            ip_file = open( ( file_name if ( save_path == None ) 
                              else ( save_path + '\\' + file_name ) ), 'w' )

            url_list = YouTube_Downloader.get_playlist_urls( playlist_url )

            for i in range( len( url_list ) ) :
                ip_file.write( url_list[i] )
                if i != len( url_list ) - 1 :
                    ip_file.write( '\n' )

            ip_file.close()

            return len( url_list )
        except Exception as e :
            raise e

class Audio_Video_Handler() :

    def __init__( self ) :
        pass

    @staticmethod
    def combine_audio_video( audio_strm, video_strm, title='Combine', save_path=None, download=True,
                             title_adjust='[\\\/:*?"<>|\[\]\(\)\【\】]' ) :

        ## title : str (without extension)

        try :
            if os.path.exists( 'combine_temp_workplace' ) :
                 shutil.rmtree( 'combine_temp_workplace' )

            os.mkdir( 'combine_temp_workplace' )
            os.mkdir( 'combine_temp_workplace\\audio' )
            os.mkdir( 'combine_temp_workplace\\video' )

            audio_strm.download( 'combine_temp_workplace\\audio' ) 
            video_strm.download( 'combine_temp_workplace\\video' ) 
            
            audio_name = 'combine_temp_workplace\\audio\\' + os.listdir( 'combine_temp_workplace\\audio' )[0]
            video_name = 'combine_temp_workplace\\video\\' + os.listdir( 'combine_temp_workplace\\video' )[0]

            input_audio = ffmpeg.input( audio_name )
            input_video = ffmpeg.input( video_name )

            if title_adjust != None :
                title = re.sub( title_adjust, '_', title )

            if save_path == None :
                save_path = title + '.mp4'
            else :
                save_path = save_path + '\\' + title + '.mp4'

            ffmpeg.concat( input_video, input_audio, v=1, a=1 ).output( save_path ).run( overwrite_output=True )

            shutil.rmtree( 'combine_temp_workplace' )

        except Exception as e :
            if os.path.exists( 'combine_temp_workplace' ) :
                 shutil.rmtree( 'combine_temp_workplace' )
            raise e

    @staticmethod
    def combine_audio_video_file( video_file_name, audio_file_name, title=None, save_path=None,
                                  title_adjust='[\\\/:*?"<>|\[\]\(\)\【\】]' ) :

        ## video_file_name : str (with extension)
        ## audio_file_name : str (with extension)
        ## title : str (without extension)

        try :
            input_video = ffmpeg.input( video_file_name )
            input_audio = ffmpeg.input( audio_file_name )

            if title == None :
                title = 'Combine.mp4'
            else :
                title = title + '.mp4'

            if title_adjust != None :
                title = re.sub( title_adjust, '_', title )

            if save_path != None :
                title = save_path + '\\' + title

            ffmpeg.concat( input_video, input_audio, v=1, a=1 ).output( title ).run( overwrite_output=True )

        except Exception as e :
            raise e

    @staticmethod
    def combine_multi_audio_video_files( video_files_path, audio_files_path, save_path=None,
                                         title_adjust='[\\\/:*?"<>|\[\]\(\)\【\】]' ) :
        try :
            video_files_list = os.listdir( video_files_path )
            audio_files_list = os.listdir( audio_files_path )

            if len( video_files_list ) == len( audio_files_list ) :
                if all( video_files_list[i].split( '.' )[0] == audio_files_list[i].split( '.' )[0]
                        for i in range( len( video_files_list ) ) ) :

                    for i in range( len( video_files_list ) ) :

                        input_video = ffmpeg.input( video_files_path + '\\' + video_files_list[i] )
                        input_audio = ffmpeg.input( audio_files_path + '\\' + audio_files_list[i] )

                        title = video_files_list[i]

                        if title_adjust != None :
                            title = re.sub( title_adjust, '_', title )

                        if save_path != None :
                            title = save_path + '\\' + title

                        ffmpeg.concat( input_video, input_audio, v=1, a=1 ).output( title ).run( overwrite_output=True )

                else :
                    raise Exception( 'Without own extension, some file names are not equal !' )
            else :
                raise Exception( 'File numbers are not equal !' )
        except Exception as e :
            raise e




