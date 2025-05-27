import pika, json, tempfile, os
from bson.objectid import ObjectId 
import moviepy.editor 

def start(message, fs_videos, fs_mp3s, channel): 
  message = json.loads(message)

  # empty temp file
  tf = tempfile.NamedTemporaryFile()
  # video contents 
  out = fs_videos.get(ObjectId(message["video_fid"]))

  #add video file contents to empty file 
  tf.write(out.read())

  # create audio from temp video file
  audio = moviepy.editor.VideoFileClip(tf.name).audio
  tf.close()

  # write audio to the file 
  tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
  audio.write_audiofile(tf_path)

  # save the audio file to mongo
  f = open(tf_path, "rb") # 'rb' for reading the file
  data = f.read()
  fid = fs_mp3s.put(data)
  f.close()
  os.remove(tf_path)

  # Updating the message 
  message["mp3_fid"] = str(fid)

  # Creating a new queue (mp3 queue) for this message 

  try: 
      channel.basic_publish(
         exchange="", 
         routing_key=os.environ.get("MP3_QUEUE"), 
         body = json.dumps(message), 
         properties = pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
         ),
      )
  except Exception as err:
     fs_mp3s.delete(fid)
     return "Fail to publish message"