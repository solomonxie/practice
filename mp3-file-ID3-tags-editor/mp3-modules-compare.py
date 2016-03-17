# coding:utf-8

########################### ID3 ################################
# 需要在文件夹中包含ID3包, 以供此处引用
# from ID3 import *
# filename = 'song2.mp3'
# id3info = ID3(filename)
# print id3info
# id3info.title = "标题啊标题"
# id3info.artist = "作家作家"
# for k, v in id3info.items(): print k, ":", v

########################### eyeD3 ################################
# 需要pip install eyed3. 
# 另外注意,final版本是0.7, 用法和网上很多的0.6的API用法极其不同
# import eyed3
# mp3 = eyed3.load("song2.mp3")
# mp3.tag.artist = u"Nobbybbb"
# mp3.tag.album = u"Love Visions"
# mp3.tag.album_artist = u"Various Artists"
# mp3.tag.title = u"I Am a Girlfriend"
# mp3.tag.track_num = 4
# mp3.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding='utf-8')
 
# ==> 成功 (更改/显示歌曲信息, 添加/删除歌曲封面图, 并能在windows资源管理器中显示)
# import eyed3
# mp3file = eyed3.load('song2.mp3')
# # print mp3file.path
# tag = mp3file.tag
# tag.artist = u'你好啊;我不好'
# tag.track_num = 4
# tag.save()\
# print "  version=[%s]" % eyed3.id3.versionToString(tag.version)
# print "  title=[%s]" % tag.title
# print "  artist=[%s]" % tag.artist
# print "  album=[%s]" % tag.album
# print "  genre=[%s]" % tag.genre
# print "  disc_num=[%s]" % str(tag.disc_num)
# print "  track_num=[%s]" % str(tag.track_num)
# print "  year=[%s]" % str(tag.best_release_date)
# # print len(tag.images)
# for image in tag.images:
#     print "%s" % image
#     print "image.id=" + image.id
#     print "image.picture_type=" + eyed3.mp3.id3.frames.ImageFrame.picTypeToString(image.picture_type)
#     print "image.mime_type=" + image.mime_type
#     print "image.description=" + image.description
#     print "image.image_data=" + str(len(image.image_data)) + " bytes"
# # # 曲线救国 通过0.6版本控制图片(0.7版本太困难了 也没有相关文档)
# import eyeD3
# mp3 = eyeD3.Tag()
# mp3.link('song2.mp3')
# mp3.removeImages() #如果不删除以前的则无法更新现在的
# mp3.addImage(3, 'artwork1.jpg', u'')
# mp3.update()

# ==> 成功
# import eyeD3 # eyeD3 v0.6 与0.7用法很不同
# trackInfo = eyeD3.Mp3AudioFile('song2.mp3')
# tag = trackInfo.getTag()
# tag.link('song2.mp3')
# print "Artist: %s" % tag.getArtist()
# print "Album: %s" % tag.getAlbum()
# print "Track: %s" % tag.getTitle()
# print "Track Length: %s" % trackInfo.getPlayTimeString()
# print "Release Year: %s" % tag.getYear()
# tag.setArtist(u'你好啊')
# tag.update()
# print "Artist: %s" % tag.getArtist()

# ==> 成功
# import eyeD3 # eyeD3 v0.6 与0.7用法很不同
# mp3 = eyeD3.Tag()
# mp3.link('song2.mp3')
# print mp3.getArtist().encode('utf-8')
# print mp3.getAlbum().encode('utf-8')
# print mp3.getTitle().encode('utf-8')
# print '\n\n'
# mp3.setArtist('AAAAA')
# mp3.setAlbum('ALBBBBum')
# mp3.setTitle('TTTTTT')
# # mp3.removeImages() #如果不删除以前的则无法更新现在的
# # mp3.addImage(1, 'artwork.jpg', u'')
# mp3.update()
# print mp3.getArtist().encode('utf-8')
# print mp3.getAlbum().encode('utf-8')
# print mp3.getTitle().encode('utf-8')


########################### mutagen ################################
# 歌曲ID3v2的常用帧标识
# 用四个字符标识一个帧,说明一个帧的内容含义(具体查百科),常用的对照如下:
# APIC: -> 图片数据 (这里的APIC: 冒号是必须的)
# APIC:Cover -> APIC(encoding=3, mime=u'image/png', type=3, desc=u'Cover', data='图片数据')
# TIT2 -> 标题
# TXXX:Tagging time -> 打标签的时间
# TRCK -> 曲目序号
# TPE1 -> 作家
# TALB -> 专辑名称
# TRCK=音轨 格式:N/M, 其中 N 为专集中的第 N 首,M 为专辑中共 M 首,N 和 M 为 ASCII 码表示的数字
# TYER=年代 是用 ASCII 码表示的数字
# TCON=类型 直接用字符串表示
# COMM=备注 格式:"eng\0 备注内容",其中 eng 表示备注所使用的自然语言

# ==> 成功 (使用mutagen的mp3模块)
# from mutagen.mp3 import MP3
# audio = MP3("song2.mp3")
# print audio.info.length, audio.info.bitrate
# print audio.pprint()

# ==> 成功 (更改/显示歌曲的作者标题等信息, 支持中文, 但是windows资源管理器中不显示)
# from mutagen.easyid3 import EasyID3
# tag = EasyID3('song2.mp3')
# tag['artist'] = [u'我是作者啦']
# tag['title'] = [u'hello 你好']
# tag["album"] = u"al"
# tag["date"] = u"2000"
# tag["tracknumber"] = u"1"
# tag["genre"] = u"g"
# tag.save()
# print tag
# print tag['title']
# # print EasyID3.valid_keys.keys() # 显示EasyID3支持的歌曲原信息
# print ''.join(tag['artist'])
# print ''.join(tag['title'])

# ==> 成功 (显示歌曲的ID3版本)
# from mutagen.id3 import ID3
# tag = ID3('song2.mp3')
# print tag.version

# ==> 成功 (显示歌曲所有的标签)
# from mutagen.mp3 import MP3
# from mutagen.id3 import ID3, APIC, error
# audio = MP3("song1.mp3")
# print audio.tags.keys()

# # ==> 成功 (将嵌入的封面图导出为图片)
# # http://stackoverflow.com/questions/6171565/how-do-i-read-album-artwork-using-python/6173176#6173176
# from mutagen import File
# file = File('song2.mp3') # mutagen can automatically detect format and type of tags
# artwork = file.tags['APIC:'].data # access APIC frame and grab the image
# with open('image.jpg', 'wb') as img:
#    img.write(artwork) # write artwork to new image


########################### Musicbrainzngs (MusicBrainz API) ################################
# 需要pip install musicbrainzngs
import musicbrainzngs
musicbrainzngs.set_useragent("solomonMusic", "0.1", "http://solomonxie.top/music")
result = musicbrainzngs.search_artists(artist="Big Bang", type="group", country="GB")
for artist in result['artist-list']: print artist['id'] +': '+ artist['name']
# print len(result['artist-list'])
# result = musicbrainzngs.search_release_groups("The Oslo Bowl")
# for album in result['release-group-list']: print album['title']









########################### beets (MusicBrainz's middleware) ################################
# 需要pip install beets
# 一般是在命令行操作的,需要将beet.exe加入环境变量或用beet.reg自动导入
# 不过在python中调用是另一种方法

