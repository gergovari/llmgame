[app]
title = ChatGPT Clone
package.name = chatgpt_clone
package.domain = org.yourname
source.dir = .
source.include_exts = py,kv,txt
version = 0.1

requirements = python3,kivy,kivymd,pyttsx3

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (str) Presplash of the application
#android.presplash_color = #FFFFFF

# (list) Permissions
#android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
#android.api = 30

# (int) Minimum API your APK will support.
#android.minapi = 24
