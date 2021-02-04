
from pytube import YouTube, Playlist
import ffmpeg
import re
import os
import shutil

class YouTube_Downloader() :

    def __init__( self, save_path='' ) :
        self.save_path = save_path
        self.caption_title_adjust = '[\\\/:*?"<>|\[\]\(\)\【\】]'

        if os.path.exists( 'combine_temp_workplace' ) :
             shutil.rmtree( 'combine_temp_workplace' )

    def print_information( self, url, show_details=True, show_subtitle=True, show_stream=True,
                           only_audio=True, only_video=True, show_progressive=True ) :
        try :
            yt = YouTube( url )

            if show_details :
                ## Showing details
                print( '------details--------------------' )
                print( "Title: ", yt.title )
                print( "Number of views: ", yt.views )
                print( "Length of video: ", yt.length )
                print( "Rating of video: ", yt.rating )
                print( '---------------------------------', end='\n\n' )

            if show_subtitle :
                ## printing all Subtitle/Caption
                print( '------captions-------------------' )
                for caption in yt.captions.all() :
                    print( caption ) ## name, code
                print( '---------------------------------', end='\n\n' )

            if show_stream :
                ## printing all the available streams
                print( '------streams--------------------' )
                for stream in yt.streams :
                    print( stream )
                print( '---------------------------------', end='\n\n' )

            if only_audio :
                ## filter out audio-only streams
                print( '------streams (only_audio)-------' )
                for stream in yt.streams.filter(only_audio=True) :
                    print( stream )
                print( '---------------------------------', end='\n\n' )

            if only_video :
                ## filter out video-only streams
                print( '------streams (only_video)-------' )
                for stream in yt.streams.filter(only_video=True) :
                    print( stream )
                print( '---------------------------------', end='\n\n' )
        
            if show_progressive :
                ## filter out progressive streams
                print( '------streams (progressive)------' )
                for stream in yt.streams.filter(progressive=True) :
                    print( stream )
                print( '---------------------------------', end='\n\n' )

        except Exception as e :
            print( str( e ), end='\n\n' )

    def single_download( self, url, itag=None, download=True, language_code=None, filter_dic=None ) :

        ## filter_dic
        ##
        ## type = None | "video" | "audio"
        ## subtype = None | "mp4" | ...
        ## res = None | "1080p" | "720p" | ...
        ## fps = None | "30fps" | ...
        ## abr = None | "128kbps" | "50kbps" | ...        
        ## only_audio = None | True | False
        ## only_video = None | True | False
        ## progressive = None | True | False

        try :
            yt = YouTube( url )

            if download :
                
                ys = None

                if itag != None :
                    ys = yt.streams.get_by_itag( itag )
                elif filter_dic != None :
                    ys =  yt.streams.filter( type = filter_dic['type'],
                                             subtype = filter_dic['subtype'],
                                             res = filter_dic['res'],
                                             fps = filter_dic['fps'],
                                             abr = filter_dic['abr'],
                                             only_audio = filter_dic['only_audio'],
                                             only_video = filter_dic['only_video'],
                                             progressive = filter_dic['progressive'] )
                    ys = ys[0]
                else :
                    ys = yt.streams.filter( progressive=True ).get_highest_resolution()
                    
                print( '------target stream--------------' )
                print( ys )
                print( '---------------------------------', end='\n\n' )

                ys.download( self.save_path ) if self.save_path != None else ys.download()
            
            if language_code != None : 
                ## download captions
                self.captions_download( url, language_code )

            print( 'Done' if download else 'Done ( no download )', end='\n\n' )
        except Exception as e :
            print( str( e ), end='\n\n' )

    def captions_download( self, url, language_code ) :
        try :
            yt = YouTube( url )

            caption = yt.captions.get_by_language_code( language_code )
            caption = caption.generate_srt_captions() ## convert to the srt format

            title = yt.title 

            if self.caption_title_adjust != None :
                title = re.sub( self.caption_title_adjust, '_', yt.title )

            caption_file = None

            if self.save_path == None :
                caption_file = open( ( title + ".srt" ), "w", encoding="utf-8" )
            else :
                caption_file = open( ( self.save_path + "\\" + title + ".srt" ), "w", encoding="utf-8" )

            caption_file.write( caption )
            caption_file.close()

            print( 'Successfully download captions :', title + ".srt", end='\n\n' )
        except Exception as e :
            print( str( e ), end='\n\n' )

    def create_ip_file( self, playlist_url, file_name='ip_file.txt' ) :
        try :
            ip_file = None

            if self.save_path == None :
                ip_file = open( file_name, 'w' )
            else :
                ip_file = open( ( self.save_path + '\\' + file_name ), 'w' )

            playlist = Playlist( playlist_url )

            ## this fixes the empty playlist.videos list
            playlist._video_regex = re.compile( r"\"url\":\"(/watch\?v=[\w-]*)" )

            total = len( playlist.video_urls )
            print( 'video num :', total, end='\n\n' )

            num = 1

            for url in playlist.video_urls:

                print( num, '/', total, ':', url, end='\n\n' )            
                ip_file.write( url )

                if num != total :
                    ip_file.write( '\n' )

                num += 1

            print( 'Create : ' + file_name, end='\n\n' )

            ip_file.close()
        except Exception as e :
            print( str( e ), end='\n\n' )

    def download_from_file( self, file_name, download=True, language_code=None, filter_dic=None ) :
        try :
            ip_file = open( file_name, 'r' )
            num = 1

            for url in ip_file.readlines() :
                print( num )    
                print( url.strip(), end='\n\n' ) ## delete the '\n' at last
                self.single_download( url=url, 
                                      download=download, 
                                      language_code=language_code,
                                      filter_dic=filter_dic )
                num += 1

            ip_file.close()

            print( 'All Done', end='\n\n' )
        except Exception as e :
            print( str( e ), end='\n\n' )

    def playlist_download( self, playlist_url, download=True, language_code=None, filter_dic=None,
                           limit_num=None ) :
        try :
            playlist = Playlist( playlist_url )

            ## this fixes the empty playlist.videos list
            playlist._video_regex = re.compile( r"\"url\":\"(/watch\?v=[\w-]*)" )

            total = len( playlist.video_urls )
            print( 'video num :', total, end='\n\n' )

            num = 1

            for url in playlist.video_urls:
                print( num, '/', total, ':', url, end='\n\n' )                
                self.single_download( url=url, 
                                      download=download, 
                                      language_code=language_code,
                                      filter_dic=filter_dic )
                if ( limit_num != None ) and ( num == limit_num ) :
                    print( 'Reach limit_num ! (', limit_num, ')', end='\n\n' )
                    break
                num += 1

            print( 'All Done', end='\n\n' )
        except Exception as e :
            print( str( e ), end='\n\n' )

    def download_single_video_audio_combine( self, url, audio_itag, video_itag, download=True, language_code=None ) :
        try :
            yt = YouTube( url )

            if download :

                audio_ys = yt.streams.get_by_itag( audio_itag )
                video_ys = yt.streams.get_by_itag( video_itag )
                    
                print( '------combine target streams--------------' )
                print( audio_ys )
                print( video_ys )
                print( '---------------------------------', end='\n\n' )

                if os.path.exists( 'combine_temp_workplace' ) :
                     shutil.rmtree( 'combine_temp_workplace' )

                os.mkdir( 'combine_temp_workplace' )
                os.mkdir( 'combine_temp_workplace\\audio' )
                os.mkdir( 'combine_temp_workplace\\video' )

                audio_ys.download( 'combine_temp_workplace\\audio' ) 
                video_ys.download( 'combine_temp_workplace\\video' ) 

                audio_name = 'combine_temp_workplace\\audio\\' + os.listdir( 'combine_temp_workplace\\audio' )[0]
                video_name = 'combine_temp_workplace\\video\\' + os.listdir( 'combine_temp_workplace\\video' )[0]

                input_audio = ffmpeg.input( audio_name )
                input_video = ffmpeg.input( video_name )

                title = yt.title 

                if self.caption_title_adjust != None :
                    title = re.sub( self.caption_title_adjust, '_', yt.title )
                
                ffmpeg.concat( input_video, input_audio, v=1, a=1 ).output( self.save_path + '\\' + title + '.mp4' ).run( overwrite_output=True )
                # .run( overwrite_output=True, capture_stdout=True, capture_stderr=True )

                print()

                shutil.rmtree( 'combine_temp_workplace' )
            
            if language_code != None : 
                ## download captions
                self.captions_download( url, language_code )

            print( 'Done' if download else 'Done ( no download )', end='\n\n' )

        # except ffmpeg.Error as e :
            # print( e.stdout, end='\n\n' )
            # print( e.stderr, end='\n\n' )
        except Exception as e :
            print( str( e ), end='\n\n' )

    def multi_video_audio_combine( self, video_files_path, audio_files_path ) :
        try :
            video_files_list = os.listdir( video_files_path )
            audio_files_list = os.listdir( audio_files_path )

            print( '------video files----------------' )
            print( video_files_list )
            print( '---------------------------------', end='\n\n' )

            print( '------audio files----------------' )
            print( audio_files_list )
            print( '---------------------------------', end='\n\n' )

            if len( video_files_list ) == len( audio_files_list ) :

                if all( video_files_list[i].split( '.' )[0] == audio_files_list[i].split( '.' )[0]
                        for i in range( len( video_files_list ) ) ) :

                    total = len( video_files_list )
                    num = 1

                    for i in range( len( video_files_list ) ) :
                        print( num, '/', total, end='\n\n' )

                        input_video = ffmpeg.input( video_files_path + '\\' + video_files_list[i] )
                        input_audio = ffmpeg.input( audio_files_path + '\\' + audio_files_list[i] )
                    
                        title = video_files_list[i]

                        if self.caption_title_adjust != None :
                            title = re.sub( self.caption_title_adjust, '_', title )

                        ffmpeg.concat( input_video, input_audio, v=1, a=1 ).output( self.save_path + '\\' + title ).run( overwrite_output=True )
                        # .run( overwrite_output=True, capture_stdout=True, capture_stderr=True )

                        print()
                        num += 1

                else :
                    print( 'ERROR : Without own extension, some file names are not equal !', end='\n\n' )

            else :
                print( 'ERROR : File numbers are not equal !', end='\n\n' )

            print( 'All Done', end='\n\n' )

        # except ffmpeg.Error as e :
            # print( e.stdout, end='\n\n' )
            # print( e.stderr, end='\n\n' )
        except Exception as e :
            print( str( e ), end='\n\n' )


