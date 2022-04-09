from flask import *
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
import DB

# Timeout duration in seconds for IP:
post_timeout = 60

public = Flask(__name__)
public.wsgi_app = ProxyFix(public.wsgi_app, x_for=1, x_host=1)

@public.route('/', methods=['GET'])
def index():
    entries = DB.getMessages()
    entries.reverse()

    return render_template('index.html', entries=entries)

@public.route('/guestbook', methods=['POST'])
def guestbook():
    tmp = request.form

    if ('username' in tmp and tmp.get('username') != '') and canPlace(request):
        DB.newMessage(tmp.get('username'), tmp.get('message')[:325], tmp.get('website'))
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] New Post from {request.remote_addr}")
    
    return redirect(url_for('index'))

def canPlace(request):
    global post_timeout

    ip = request.remote_addr
    last_post = DB.getLastPost(ip)

    if len(last_post) > 0:
        last_post = datetime.strptime(last_post[0][1], '%Y-%m-%d %H:%M:%S')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        
        diff = now - last_post

        if diff.total_seconds() <= post_timeout:
            return False
    
    DB.setLastPost(ip)
    return True