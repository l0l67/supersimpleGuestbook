from flask import *
import DB

public = Flask(__name__)

@public.route('/', methods=['GET'])
def index():
    entries = DB.getMessages()
    entries.reverse()
    
    return render_template('index.html', entries=entries)

@public.route('/guestbook', methods=['POST'])
def guestbook():
    tmp = request.form
    if 'username' in tmp and tmp.get('username') != '':
        DB.newMessage(tmp.get('username'), tmp.get('message')[:325], tmp.get('website'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    public.run(port=80)
